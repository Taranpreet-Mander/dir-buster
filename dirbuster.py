"""
dir-buster - a simple web directory / file brute-forcer.

it takes a base url and a wordlist, requests base/word for each word, and tells
you which ones exist (based on the http status code). this is how you find hidden
pages / folders / backups on a web server during a pentest (think /admin, /backup,
/.git, robots.txt etc).

  ====================================================================
   ONLY run this against systems you OWN or have WRITTEN PERMISSION to
   test. brute-forcing someone elses site is illegal and also just rude.
   i use it on my own lab boxes / deliberately-vulnerable VMs (DVWA etc).
  ====================================================================

usage:
    python dirbuster.py http://localhost:8000
    python dirbuster.py http://10.0.0.5 -w wordlists/common.txt -x php,txt -t 40
"""
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# status codes that usually mean "something is here" (2xx, redirects, auth-required)
INTERESTING = {200, 204, 301, 302, 307, 308, 401, 403, 405}


def build_paths(words, extensions):
    seen = set()  # avoid dupes, e.g. word "config.php" + word "config" + ext "php"
    for w in words:
        w = w.strip().strip("/")
        if not w or w.startswith("#"):
            continue
        candidates = [w] + [f"{w}.{ext}" for ext in extensions]
        for c in candidates:
            if c not in seen:
                seen.add(c)
                yield c


def check(base, path, timeout, follow):
    url = f"{base}/{path}"
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=follow)
    except requests.RequestException:
        return None
    if r.status_code in INTERESTING:
        size = len(r.content)
        return r.status_code, path, size
    return None


def main():
    ap = argparse.ArgumentParser(description="simple web directory/file brute-forcer")
    ap.add_argument("url", help="base url, e.g. http://localhost:8000 (ONLY targets you're allowed to test)")
    ap.add_argument("-w", "--wordlist", default="wordlists/common.txt", help="wordlist file")
    ap.add_argument("-x", "--extensions", default="", help="extensions to also try, comma separated e.g. php,txt,bak")
    ap.add_argument("-t", "--threads", type=int, default=20, help="threads (default 20)")
    ap.add_argument("--timeout", type=float, default=5.0, help="request timeout seconds (default 5)")
    ap.add_argument("--no-follow", action="store_true", help="don't follow redirects (show the 301/302 instead)")
    args = ap.parse_args()

    base = args.url.rstrip("/")
    extensions = [e.strip().lstrip(".") for e in args.extensions.split(",") if e.strip()]

    try:
        with open(args.wordlist) as f:
            words = f.readlines()
    except FileNotFoundError:
        print(f"[!] wordlist not found: {args.wordlist}")
        sys.exit(1)

    paths = list(build_paths(words, extensions))
    print(f"[*] target : {base}")
    print(f"[*] words  : {len(words)}  (+{len(extensions)} extensions = {len(paths)} requests)")
    print("[*] reminder: only test targets you are authorised to test!\n")

    found = []
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        futures = [pool.submit(check, base, p, args.timeout, not args.no_follow) for p in paths]
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                code, path, size = res
                print(f"  [{code}] /{path}  ({size} bytes)")
                found.append(res)

    print(f"\n[*] done. {len(found)} interesting path(s) found.")


if __name__ == "__main__":
    main()
