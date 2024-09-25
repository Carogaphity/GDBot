import os, time, asyncio

import discord

class gameState:
    def __init__(self):
        self.level = None
        self.clicked = None
game_states = {}

intents = discord.Intents.default()
intents.message_content = True


import logging

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

bot = discord.Bot(intents=intents)

all_types = {
    discord.IntegrationType.user_install, discord.IntegrationType.guild_install
}

emoji_dict = {
    "🟦": "<:air:1287839395117793310>",
    ".": "<:air:1287839395117793310>",
    "^": "<:spike:1287839420422029423>",
    "🔺": "<:spike:1287839420422029423>",
    "⬛": "<:block:1287839435584438445>",
    "-": "<:block:1287839435584438445>",
    "🟧": "<:cube1:1287839451296305293>",
    "%": "<:cube1:1287839451296305293>",
    "🏁": ":pause_button:",
    "*": ":pause_button:",

    "C":"<:cube_p:1287839465087176819>",
    "🟢":"<:cube_p:1287839465087176819>",
    "B":"<:ball_p:1287839479612309536>",
    "🔴":"<:ball_p:1287839479612309536>",
    "W":"<:wave_p:1287839491393847387>",
    "🔵":"<:wave_p:1287839491393847387>",
    "U":"<:ufo_p:1287839503846867026>",
    "🟠":"<:ufo_p:1287839503846867026>",
}


gm_dict = {
    '<:cube_p:1287839465087176819>': 'Cube', 
    '<:ball_p:1287839479612309536>': 'Ball', 
    '<:wave_p:1287839491393847387>': 'Wave',
    '<:ufo_p:1287839503846867026>': 'Ufo',
    }




async def create_level(level: discord.Attachment, ctx: discord.ApplicationContext):

    global emoji_dict

    try:
        loadingmsg = await ctx.send("Reading level...")

        level = await level.read()
        level = level.decode('utf-8')
        game_states[ctx.author.id].level = level


    except Exception as e:
        await loadingmsg.delete()
        await ctx.respond(f"Error loading level. \n{e}", ephemeral=True)
        return
    await loadingmsg.edit("Read level successfully!")
    try:
    # Splits the level into rows
        rows = level.strip().split("\n")

        # Creates a list of lists, where each sublist is a row of emojis (string of chr)
        await loadingmsg.edit("Reading grid...")
        chr_list = []
        for string in rows:
            string.strip()
            spritelist = [emoji_dict[char] for char in string]
            chr_list.append(list(spritelist))
    except Exception as e:
        await loadingmsg.delete()
        await ctx.respond(f"Failed to load map.\n`{e}`", ephemeral=True)
        return
    await loadingmsg.edit("Read grid successfully!")
    await asyncio.sleep(0.3)
    await loadingmsg.delete()
    


    # Finds player spawn position
    p_pos = [1, 1]
    try:
        for row in chr_list:
            if "<:cube1:1287839451296305293>" in row:
                p_pos = [row.index("<:cube1:1287839451296305293>"), chr_list.index(row)]
            chr_list[p_pos[0]][p_pos[1]] = "<:air:1287839395117793310>"

            # return list of lists and player's default position

    except IndexError: return chr_list,[1,1]
    return chr_list, p_pos


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_reaction_add(reaction, user):
    global game_states

    # Ignore reactions from the bot itself
    if user == bot.user:
        return


    # Check if the reaction is related to an ongoing game
    if user.id in game_states:
        # Check if the reaction is the jump reaction
        if str(reaction.emoji) == "\U0001F53C":

            # Set the jump variable in the game state
            game_states[user.id].clicked = True

            # Remove the reaction so the user can react again
            await reaction.remove(user)



@bot.slash_command(name="play", description="starts a level", integration_types=all_types)
async def play(
    ctx: discord.ApplicationContext,
    level: discord.Option(
        discord.Attachment, required=False, name="level", description="a text file containing a gdbot level. If not included, will use the most recent level you've loaded."
    ),
):
    
    global game_states
    if not ctx.author.id in game_states:
        game_states[ctx.author.id] = gameState()
    try:
        board, player_pos = await create_level(level if level else game_states[ctx.author.id].level, ctx)

        if not board or not player_pos:
            return
    except Exception as e:
        await ctx.respond(f"There was an error loading the level. Make sure you have a valid level. \n{e}", ephemeral=True)
        return
    
    new_frame = ""

    start_col = player_pos[0] - 2
    end_col = player_pos[0] + 4

    for row in board:
        new_frame += "".join(row[start_col:end_col]) + "\n"

    embed = discord.Embed(
        title="Geometry Dash", description=new_frame, color=discord.Color.green()
    )
    embed.add_field(name=f"Started by {ctx.author}", value="", inline=True)

    bot_message = await ctx.send(embed=embed)
    await bot_message.add_reaction("\U0001F53C")

    play = True
    gamemode = "Cube"

    gravity = 0
    jumped = 0


    while play:

        if gamemode == "Cube":
            # Checks if the player has ground under them``
            if (
                (game_states[ctx.author.id].clicked and board[player_pos[1] + 1][player_pos[0]]
                == "<:block:1287839435584438445>" and not gravity)
                or
                (board[player_pos[1] - 1][player_pos[0]] == "<:block:1287839435584438445>" and gravity)
            ):
                jumped = 0

            # If the player wants to jump and there's ground below them, jump.
            if (
                (game_states[ctx.author.id].clicked
                and board[player_pos[1] + 1][player_pos[0]]
                == "<:block:1287839435584438445>"
                and not gravity)
            ):
                player_pos[1] -= 1
                jumped = 1

            elif (board[player_pos[1] - 1][player_pos[0]]
                == "<:block:1287839435584438445>"
                and gravity
            ):
                player_pos[1] += 1
                jumped = 1
            game_states[ctx.author.id].clicked = False


        elif gamemode == "Ufo":

            if not gravity and game_states[ctx.author.id].clicked:
                player_pos -= 1
                jumped = 1
                game_states[ctx.author.id].clicked = False
            
            elif gravity and game_states[ctx.author.id].clicked:
                player_pos += 1
                jumped = 1
                game_states[ctx.author.id].clicked = False

        elif gamemode == "Ball":
            if (game_states[ctx.author.id].clicked and
                board[player_pos[1] + 1][player_pos[0]]
                == "<:block:1287839435584438445>"
                and not gravity) or (
                board[player_pos[1] - 1][player_pos[0]]
                == "<:block:1287839435584438445>"
                and gravity):

                gravity = not gravity
                game_states[ctx.author.id].clicked = False
        
        elif gamemode == "Wave":
            if game_states[ctx.author.id].clicked: gravity = not gravity; game_states[ctx.author.id].clicked = False

        # If player is not on ground and is not jumping, moves player down
        if (
            board[player_pos[1] + 1][player_pos[0]]
            != "<:block:1287839435584438445>"
            and jumped == 0 and not gravity
        ):
            player_pos[1] += 1

        elif (
            board[player_pos[1] - 1][player_pos[0]]
            != "<:block:1287839435584438445>"
            and jumped == 0 and gravity
        ):
            player_pos[1] -= 1

        # Checks if the player touches a flag
        if board[player_pos[1]][player_pos[0]] == ":pause_button:":
            embed = discord.Embed(
                title="Geometry Dash",
                description="**You win!**",
                color=discord.Color.green(),
            )
            embed.add_field(
                name=f"Started by {ctx.author.mention}", value="", inline=True
            )
            await bot_message.edit(embed=embed)
            await bot_message.remove_reaction("\U0001F53C", bot.user)
            play = False
            break

        # Checks if the player crashes
        elif board[player_pos[1]][player_pos[0]] in [
            "<:spike:1287839420422029423>",
            "<:block:1287839435584438445>",
        ]:
            embed = discord.Embed(
                title="Geometry Dash",
                description="**You lose!**",
                color=discord.Color.green(),
            )
            embed.add_field(
                name=f"Started by {ctx.author.mention}", value="", inline=True
            )
            await bot_message.edit(embed=embed)
            await bot_message.remove_reaction("\U0001F53C", bot.user)
            play = False
            del game_states[ctx.author.id]
            break

        #Checks if player needs to change gamemode
        elif board[player_pos[1]][player_pos[0]] in gm_dict:
            gamemode = gm_dict[board[player_pos[1]][player_pos[0]]]


        # Changes player's printed position
        if gamemode == "Cube":
        
            board[player_pos[1]][player_pos[0]] = (
                "<:cube2:1287839518388387852>"
                if jumped != 0
                else "<:cube1:1287839451296305293>"
            )

        elif gamemode == "Ufo": board[player_pos[1]][player_pos[0]] = "<:ufo1:1287839534310232139>"
        elif gamemode == "Ball": board[player_pos[1]][player_pos[0]] = "<:ball1:1287839548105166933>"

        elif gamemode == "Wave": board[player_pos[1]][player_pos[0]] = (
            "<:wave1:1287839560667238412>"
            if not gravity
            else "<:wave2:1287839572381925426>"
        )

        # Checks how far along a jump is at
        if jumped == 1:
            jumped = 2
        elif jumped == 2:
            jumped = 0

        # Defines which parts of the level should be printed
        start_col = player_pos[0] - 2
        end_col = player_pos[0] + 4

        new_frame = ""
        for row in board:
            new_frame += "".join(row[start_col:end_col]) + "\n"

        embed = discord.Embed(
            title="Geometry Dash",
            description=new_frame,
            color=discord.Color.green(),
        )
        embed.add_field(name=f"Started by {ctx.author.mention}", value="", inline=True)

        await bot_message.edit(embed=embed)

        # Deletes old player model
        board[player_pos[1]][player_pos[0]] = "<:air:1287839395117793310>"

        # Moves player on x-axis
        player_pos[0] += 1

        game_states[ctx.author.id].clicked = False

        # Defines framerate
        await asyncio.sleep(0.4)


@bot.slash_command(name="load_level", description="load a level from a text file.")
async def load_level(
    ctx: discord.ApplicationContext, 
    level: discord.Option(
        discord.Attachment,
        name="level", description="the level to import",
        required=True
    )):
    await create_level(level, ctx)

with open('bot.txt', 'r') as d:
    bot.run(d.read())
