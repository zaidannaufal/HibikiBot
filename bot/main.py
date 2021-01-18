import discord
from discord.ext import commands
import os
# from dotenv import load_dotenv
# from pathlib import Path  # Python 3.6+ only

# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

client = commands.Bot(command_prefix= 'ne ')
token = os.getenv("DISCORD_BOT_TOKEN")
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Journey of Elaina"))
    print('Bot is ready.')

# load cogs dari command discord
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded')

#unload cogs dari command discord
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded')

#restart cogs biar ga ribet unload load
@client.command()
async def restart(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} restarted')
    
#looping buat load semua cogs saat run
for filename in os.listdir('./bot/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)#token))
# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as {0}!'.format(self.user))

#     async def on_message(self, message):
#         print('Message from {0.author}: {0.content}'.format(message))

# client = MyClient()
