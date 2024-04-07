import os, asyncio
from dotenv import load_dotenv

import discord



load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


game_states = {}

intents = discord.Intents.default()
intents.message_content = True


import logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client = discord.Client(intents=intents)

global cmd
cmd = 'GD '


def create_level():

	level = """
	🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🏁
	🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🏁
	🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🏁
	🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🏁
	🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🏁
	🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🏁
	🟦🟦🟧🟦🟦🔺🔺🟦🟦🟦⬛⬛⬛⬛🟦🟦🟦⬛⬛⬛⬛🟦🟦🟦🟦🟦🟦🏁
	⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🏁
	⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🏁
	"""
	# Splits the level into rows
	rows = level.strip().split('\n')

	# Creates a list of lists, where each sublist is a row of emojis (string of chr)
	chr_list = []
	for string in rows:
		chr_list.append(list(string))

	# Finds player spawn position
	p_pos = [1, 1]
	for row in chr_list:
		if '🟧' in row: p_pos = [row.index('🟧'), chr_list.index(row)]
		chr_list[p_pos[0]][p_pos[1]] = '🟦'

		#return list of lists and player's default position
	return chr_list, p_pos



@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_reaction_add(reaction, user):
    # Ignore reactions from the bot itself
    if user == client.user:
        return

    # Check if the reaction is related to an ongoing game
    if reaction.message.id in game_states:
        game_state = game_states[reaction.message.id]

        # Check if the reaction is the jump reaction
        if str(reaction.emoji) == 'U+D83C':
            # Set the jump variable in the game state
            game_state['p'] = 1

            # Remove the reaction so the user can react again
            await reaction.remove(user)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(cmd + 'play'):
        
        if message.author.id not in game_states:
            # If not, create a new game state
            game_states[message.author.id] = {
                'p': 0
            }
        

        board, player_pos = create_level()
        embed = discord.Embed(title='Geometry Dash', description=board, color=discord.Color.green())
        embed.add_field(name=f'Started by {message.author}', value='', inline=True)

        bot_message = await message.channel.send(embed=embed)
        await bot_message.add_reaction('U+D83C')

        play = True

        gs = game_states[message.author.id]
        
        jumped = 0

        while play:

            #Checks if the player has ground under them
            if board[player_pos[1] + 1][player_pos[0]] == '⬛':
                jumped = 0


            #If the player wants to jump and there's ground below them, jump.
            if gs['p'] and board[player_pos[1] + 1][player_pos[0]] == '⬛':
                player_pos[1] -= 1
                jumped = 1

            #If player is not on ground and is not jumping, moves player down
            if board[player_pos[1] + 1][player_pos[0]] != '⬛' and jumped == 0:
                player_pos[1] += 1

            #Checks if the player touches a flag
            if board[player_pos[1]][player_pos[0]] == '🏁':
                await message.channel.send('You win!')
                play = False
                game_states.remove(message.author.id)
                break

            #Checks if the player crashes
            elif board[player_pos[1]][player_pos[0]] in ['🔺', '⬛']:
                await message.channel.send('You lose!')
                play = False
                game_states.remove(message.author.id)
                break

            #Changes player's printed position
            board[player_pos[1]][player_pos[0]] = '🔶' if jumped != 0 else '🟧'


            #Checks how far along a jump is at
            if jumped == 1:
                jumped = 2
            elif jumped == 2:
                jumped = 0

            #Defines which parts of the level should be printed
            start_col = player_pos[0] - 2
            end_col = player_pos[0] + 4

            new_frame = ""
            for row in board:
                new_frame += ("".join(row[start_col:end_col]) + '\n')

            embed = discord.Embed(title="Geometry Dash", description=new_frame, color=discord.Color.green())

            await bot_message.edit(embed=embed)

            # Deletes old player model
            board[player_pos[1]][player_pos[0]] = '🟦'

            #Moves player on x-axis
            player_pos[0] += 1

            #Defines framerate
            await asyncio.sleep(0.5)

            
    
    elif message.content.startswith(cmd + 'changePrefix'):
        cmd = str(message.content).replace(cmd + 'changePrefix', "")
        message.channel.send(f'Prefix changed to {cmd}!')

client.run(TOKEN)



