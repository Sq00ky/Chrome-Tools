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
