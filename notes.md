# notes

## what this is

a web content brute-forcer for learning pentesting. wanted to understand what
gobuster/dirb actually do so i built a tiny version.

## what i learned

- the whole trick is just the http STATUS CODE. 200 = exists, 404 = nope. but
  403 (forbidden) and 401 (needs auth) are interesting too - the path EXISTS,
  youre just not allowed in. so i include those.
- 301/302 redirects usually mean a folder (server redirects /admin -> /admin/).
  added --no-follow so you can see the redirect itself.
- threads make a big difference again (same as my port scanner). requests is
  blocking so a thread pool keeps it moving.
- had a dupe bug: if the wordlist has "config.php" AND i add "-x php", i'd request
  config.php twice. fixed it with a seen set in build_paths.

## careful / ethics

only on my own lab. a dir-buster hammers a server with hundreds/thousands of
requests - thats noisy and against real sites its illegal. testing it i just used
python -m http.server on a folder.

## todo
- recursion into found folders
- filter by size / hide status codes (real sites return 200 for everything via a
  catch-all, which floods the output)
- custom headers + cookies for authed scanning
