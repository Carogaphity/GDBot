# __GDBot Documentation__

Hello! This is the documentation for a discord bot, GDBot, which allows you to play geometry dash levels in your discord server. It will contain a full rundown of each part of this bot, as well as some additional stuff.

```
Table of contents:

Commands
Level Editor
Hosting it yourself
```

### Commands
Currently, the bot has very few commands. This may or may not change over time, depending on how much I feel like implementing. The commands are as follows (default prefix is `GD-`)

- **[prefix] loadLevel [level]**
- **[prefix] play**
- **[prefix] changePrefix**
- **[prefix] help**

Most of these are self explanatory, though I should mention that `loadLevel` does require attaching a .txt file.

### GDBot Level Editor

This is a simple level editor designed for creating levels for my Geometry Dash discord bot. The editor allows you to place various types of sprites on a grid to design your levels. Here's a breakdown of its features:

##### Grid Interface

The main interface consists of a grid where you can place sprites. The grid is dynamically generated with 20 columns and 10 rows.

##### Sprite Selection

You can select different sprites using the toolbar buttons provided. Currently supported sprites are:
- Block
- Spike
- Ball Portal
- Wave Portal
- Cube Portal
- Finish
- Player

##### Rectangle Tool

The editor also includes a rectangle tool that allows you to fill a rectangular area with a selected sprite. This feature can be activated using the "Rectangle Tool" button in the toolbar.

##### Export Functionality

Once you've designed your level, you can export it as a text file. The exported file contains a representation of the level layout using characters corresponding to the sprites placed on the grid. Use the command GD-loadLevel with this text file to play your level in the bot!

##### Clear Grid

There's an option to clear the grid and remove all sprites, leaving empty space (air).

##### How to Use

- Click on a sprite button in the toolbar to select it.
- Click on a grid cell to place the selected sprite.
- Use the rectangle tool to fill a rectangular area with the selected sprite.
- Click the "Export" button to save your level as a text file to be used in `[prefix] loadLevel`


### Private Hosting
So, you're interested in hosting the bot yourself, huh? Maybe make some modifications that I can't get off my ass to go do? Well lucky for you, it's actually incredibly simple. Download main.py from the github repo, open it up in your IDE, and add a file called ".env". Inside of `.env`, put the line `DISCORD_TOKEN=` followed by your discord bot token **not in a string**. You can get your bot token from [here](https://discord.com/developers/). Then, just save the file, make sure all your dependencies are installed (`pip install discord`), and press run. Add your bot to your server, and it should come online :)

