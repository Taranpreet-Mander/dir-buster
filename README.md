# dir-buster

a simple web directory / file brute-forcer i wrote for learning web pentesting. you give it a url and a wordlist, and it checks which paths actually exist on the server by looking at the http status codes. this is how you find hidden pages, admin panels, backups, `.git` folders etc during a pentest.

basically a tiny version of gobuster / dirb / ffuf. built it to understand what those tools are doing.

## ⚠️ only test what you're allowed to

brute-forcing a website you don't own is illegal. use this only on:
- your own servers / VMs
- deliberately vulnerable practice boxes (DVWA, bWAPP, Juice Shop, HackTheBox/TryHackMe machines you're assigned)
- targets you have **written permission** to test

i run it against my own lab. don't point it at random sites.

## how it works

- for each word in the wordlist it requests `base_url/word` (and optional extensions like `.php`)
- if the status code looks interesting (200, 301/302, 401, 403, ...) it reports the path + response size
- uses threads so its reasonably fast
- 403/401 are shown too because "forbidden" still means the path *exists* - useful info

## usage

```bash
pip install -r requirements.txt
python dirbuster.py http://localhost:8000
python dirbuster.py http://10.0.0.5 -w wordlists/common.txt -x php,txt,bak -t 40
```

options:
- `-w` wordlist (default `wordlists/common.txt`)
- `-x` extra extensions to try, e.g. `php,txt,bak`
- `-t` threads (default 20)
- `--timeout` request timeout
- `--no-follow` don't follow redirects (show the 301/302 itself)

## example (against a local test server)

```
[*] target : http://localhost:8000
[*] words  : 50  (+2 extensions = 143 requests)

  [200] /config.php  (16 bytes)
  [200] /uploads  (5 bytes)
  [200] /robots.txt  (14 bytes)
  [200] /admin  (19 bytes)

[*] done. 5 interesting path(s) found.
```

i tested it by serving a folder with `python -m http.server` and it correctly found the paths i'd hidden in there.

## wordlist

`wordlists/common.txt` is a small starter list of common paths. real pentesting uses big lists like [SecLists](https://github.com/danielmiessler/SecLists) - just point `-w` at one of those.

## stuff i want to add

- [ ] recursion (when it finds a folder, scan inside it too)
- [ ] filter by response size / hide a specific status code (to cut noise from catch-all 200 pages)
- [ ] a proper progress counter
- [ ] custom headers / cookies (to scan authenticated areas)
- [ ] save results to a file

## note

learning project, works but basic. pairs with my [port-scanner](https://github.com/Taranpreet-Mander/port-scanner) as a little recon toolkit.

MIT license.
