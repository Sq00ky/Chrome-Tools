# Chrome-Tools
## Overview
Welcome to the repo. This repo will have a small amount of Chrome tools that can be used for DFIR, Hacking, Deception, whatever your heart desires. I originally started out with a goal of writing a proof of concept tool that could read Chrome browser histroy. It's pretty much an overcomplicated SQL statement that runs a SELECT * FROM URLS; in Chrome's SQLite database... But the next portion is a little bit more challenging -- I haven't seen anyone be able to inject browser history into Chrome, so that's what I'm pursuing next!

### Read Chrome History
This is pretty much a fancy database wrapper... Yeah... that's it. There's two arguments (both optional):
-d --database - Specify the database you would like to retrieve the browser history from. By default this will use ```C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\History```
-o --output - Specify if you would like the output file, by default this will print the text to the screen

<img src=https://i.imgur.com/kLhIDk8.png>

### Inject Chrome History

todo

### Inject Chrome Creds

This is, yet again, another fancy db wrapper that encrypts a given string (ex. P@ssw0rd123) and injects it into Google Chrome's saved credential database. The Chrome encryption process is relatively complicated; Google generates a 32-character random string that is encrypted using Microsoft's Data Protection API (DPAPI). This will decode it so it can be used as an encryption key. Google prefixes this key with DPAPI for some reason... It trims that, then generates a 12-byte IV/Nonce which is used to encrypt the password. The format looks roughly like so: 

v10 (A Google specific prefix)
12-byte random nonce/iv
encrypted AES256-GCM string

```v10\xc5\xaa\xa4~\xde\xfbx\xbfC@Sz\t,\x91\x84\x85\xfc\x9f\x15%F1\x85r```

From there, the full blob is injected into the ChromeDB. It's still very much a work-in-progress
<img src=https://i.imgur.com/Khn2yjv.png>

Yeah!

<img src=https://i.imgur.com/XU3KOgF.png>

Anyways, there's some minor issues that need to be fixed. I'll look into doing it at some point.

To do:
- Add parameter that takes password which can be used for master key decryption ...

