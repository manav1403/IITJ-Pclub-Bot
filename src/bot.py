import discord
import datetime
import utilities
import time


client = discord.Client()

symbol = '$'


@client.event
async def on_message(message):

    global symbol
    guild = message.channel.guild
    message.content = message.content.lower()
    if message.author == client.user:
        return

    if not message.content.startswith(symbol):
        utilities.update_user_msg_count(message.author.id)

    # Sends a message with the current time
    if message.content.startswith(symbol + 'time'):
        await message.channel.send(str(datetime.datetime.now()))

    # Set a new symbol for the bot
    elif message.content.startswith(symbol + 'set'):
        content = message.content.split()
        if len(content) <= 1:
            await message.channel.send(f'Please enter a symbol. Usage "{symbol}set <new symbol>"')
        else:
            symbol = content[1]
            await message.channel.send(f'The new symbol has been set to "{symbol}"')

    elif message.content.startswith(symbol + 'syncdb'):
        users = utilities.users
        for member in guild.members:
            if users.get(member.id) is None:
                utilities.add_user(member.id)

        await message.channel.send(f'There are {guild.member_count} members in the server. DataBase Sync Complete')

        # Start Prune Tasks for daily elimination
        while True:
            time.sleep(2)
            print('ll')

    elif message.content.startswith(symbol + 'prune'):
        # This estimates how many members will be pruned
        pruned_members = await message.guild.estimate_pruned_members(7)
        await message.channel.send(f'{pruned_members} members were pruned due to inactivity.')
        # await message.guild.prune_members(7) # Actually pruning members

    elif message.content.startswith(symbol + 'role'):
        content = message.content.split()
        if len(content) <= 1:
            await message.channel.send(f'Please specify a role. Usage "{symbol}role <name of role>"')
        else:
            role = content[1]
            user = message.author
            try:
                await user.add_roles(discord.utils.get(user.guild.roles, name=role))
                await message.channel.send(f'{message.author.mention} was given the role {role}')
            except Exception as e:
                await message.channel.send('Cannot assign role. Error: ' + str(e))

    elif message.content.startswith(symbol):  # A catchall.
        await message.channel.send('Hello This bot has been called v1.0.0')


client.run('')
