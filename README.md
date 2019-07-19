######Steals tiles from any tileserver that distributes them using {zyx} scheme (or {xyz}, anyway)
##### How to use this shit?
###### I hope you have installed python3.6?
- pip3 install requests
##### Try to type something like this:

`
python3 tilespider.py -u https://foo.server.com/tile --top 52.483 --bottom 44.056 --left 22.500 --right 40.430 --min-zoom
--max-zoom
`

⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⣿⣿⠻⢛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\
⣿⣿⣿⣿⣿⣿⣿⡻⡆⣤⡅⠁⠀⠀⢫⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿\
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣤⠀⠀⠀⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢻⣿⣿⣿⣿⣿⣿⣿⣿\
⡟⠿⢿⡿⢷⣍⣿⣿⣭⢿⣿⣧⠀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡟⠁⠀⠀⠉⠙⠛⠙⠻⢿⢿⣿\
⣇⣠⣸⡀⠋⠀⠀⣼⣿⢦⣿⣧⣼⣿⣿⣿⣿⣿⣿⡻⠛⠁⠀⠈⠁⠀⠀⠀⠀⠀⢀⣀⣤⣄⣾⣿\
⣿⣿⣿⣿⣄⣀⣰⣍⡻⢁⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣤⠴⠒⢢⣤⠤⢾⣴⢦⣚⣿⣿⣿⣿⣿\
⣿⣿⣿⣿⣧⣀⡀⠘⢋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣟⠈⠉⠊⢷⣾⣿⣿⣿⣿⣿⣿\
⣿⣿⣿⣿⣿⣷⣟⣿⣿⣿⣿⣿⣿⣿⣿⣟⣧⣜⣞⣟⣷⣽⣿⣿⣨⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿\
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⠿⠿⢿⣿⣿⣿⣿⣿⣟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣄⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⢿⣿⣿⣿⣿\
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣴⣿⣿⣿⣿

#####Have patience. That larger the scale, then more tiles you need to download, and sooner or later, the server will understand that you are not a human and will break the connection.
######You will have to pause and retry download missing tiles until everything is loaded

