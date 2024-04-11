# GDBot

Hello! This is the README for GDBot, containing everything a casual user needs to know. If you want the [documentation](https://github.com/Carogaphity/Geometry-Dash-through-Discord/blob/main/documentation.md), you're in the wrong place. This bot is a simple discord bot to be able to play levels inside of discord. This is going to quickly go over everything you need to know.

#### Commands
All of these commands will assume you are using the default prefix, which is `GD-`. If you change the prefix, run these same commands but change `GD-` to whatever your prefix is.

##### `GD-loadLevel`
This one is very important. Run this command with a .txt file attached to your message containing your level in order to load a level to play. You can get these .txt files from the official [discord](https://discord.gg/T8tJf3Zbq5), or make them yourself with the [level editor](https://github.com/Carogaphity/Geometry-Dash-through-Discord/blob/main/converter.html). 
**In order to use the level editor, simply download the html and double click it in your file manager to open it in your browser. A slightly more in depth explanation of the level editor is in the documentation.**

##### `GD-play`
Once you've loaded a level with `GD-loadLevel`, this command should, in theory, let you play the level. I'm a 15 year old writing spaghetti code though, so for all I know someone else has my token by now.

##### `GD-changePrefix`
Lets you change the prefix that is used before every command from `GD-` to something else. I don't know why you would want to do this, but I guess you can.

##### `GD-help`
Displays an explanation of each of the commands, and is probably what sent you here in the first place!

### Info and FAQ

Q: Why is the bot offline?
**A: Either the bot is in early enough development I haven't figured out how to keep it running consistently yet, or the bot is down. In which case, go spam me in the #bot-down channel in the discord server.**

Q: My level won't load!
**A: Did you put the level in a .txt file? Did you spell the command correctly? Do you have a player model and a finish in the level? Did you add a character the bot doesn't recognize to your txt file?**

Q: The level editor sucks!
**A: Yep, it does. I hate writing HTML and avoid it at all costs. Write a better one if it bothers you that much :)**

Q: There's so much latency!
**A: I'm working on it, okay? Inherently, any form of interaction will take a hot second to be processed by the bot. I'll keep searching for a way to make it better, but we might get stuck with one frame of latency. In which case, do you want a higher gamespeed or lower latency? Your choice, buddy.**

Q: Are you ever going to implement hold gamemodes? (Ship, Robot, etc) What about Swingcopter?
**A: Nope. Tell me how you expect me to implement hold detection when the game is controlled by reactions. As for swingcopter, I think I'd rather die than learn parabola math :)**
