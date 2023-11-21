import discord
from discord.ext import commands
import requests
import asyncio

green = "\033[1;32m"
white = "\033[1;37m" 
color = 0x979797
owner = 1157733927100883035
say_channel = 1145005935262171196
bot_id = 1161234902973415434
reminder_channel = 1162723176598478878
prefix = "$"
token = ""
koala = commands.Bot(command_prefix=prefix, intents = discord.Intents.all(), help_command=None)
bot_access = [1153710913103343729, 1157733927100883035]
no_access_embed = discord.Embed(title="Koala Error", description="You cannot run the given command.", color=color)

help_menu = discord.Embed(title = "DOWNLOAD LINKS", description = """
- sb = latest selfbot version
- prevsb = download older selfbot versions
- wizzer = koala wizzer status
- vcbot = koala vcbot link
""",color=color)

help_menu2 = discord.Embed(title = "BOT COMMANDS", description = """
- note = send a message in <#1145005935262171196>
- botconfig = [OWNER ONLY]
- github [query] = gthub finder
""",color=color)
bot_config = discord.Embed(title = "BOT CONFIG", description = "shutdown, listen, watch, play, stream, dm @ msg, todo",color=color)

@koala.event
async def on_message(message):
    if "koala sb" in message.content:
        if message.author.id != bot_id:
            id = message.channel.id #maybe idk
            await message.reply("https://discord.com/channels/1095595243417649175/1095645247536648222/1157221000799326349")
        else:
            pass
    elif "tools" in message.content or "scripts" in message.content:
        if message.author.id != bot_id:
            id = message.channel.id #maybe idk
            await message.reply("The tools that Koala use in his videos are either publlic or they are not public. The public ones can be found on his [github](https://github.com/infamous-koala).")
        else:
            pass
    else:
        pass
 
    await koala.process_commands(message)

@koala.command()
async def help(ctx):
    try:
        await ctx.reply(embed=help_menu)
        await ctx.reply(embed=help_menu2)
    except Exception as e:
        print(f"An error occurred: {e}")

@koala.command()
async def botconfig(ctx):
     await ctx.reply(embed=bot_config)

@koala.event
async def on_ready():
    print(f'{green}[+]{white} {koala.user} is online\nPrefix: {prefix}')

@koala.command()
async def prevsb(ctx):
    embed = discord.Embed(title="Koala SB", description="v1.0: Release\nv1.5: v1 patched\n[CURRENTLY DISCONTINUED]",color=color)
    await ctx.reply(embed=embed)
    
@koala.command()
async def sb(ctx):
    embed = discord.Embed(title="DISCONTINUED", description=f"Hello <@{ctx.author.id}> refer to this message for the reasons of the project being discontinued, https://discord.com/channels/1095595243417649175/1095645247536648222/1157221000799326349", color=color)
    await ctx.reply(embed=embed)

@koala.command()
async def say(ctx, *, text):
    if ctx.author.id in bot_access:
            message = ctx.message
            await message.delete()
            await ctx.send(text)
    else:
        await ctx.send(embed=no_access_embed)

@koala.command()
async def shutdown(ctx):
    if ctx.author.id in bot_access:
         await ctx.reply("> Shutdown innitiated...")
         await ctx.reply("Bot is going offline :koala: :zzz:")
         await koala.logout()
    else:
         await ctx.send(embed=no_access_embed)

@koala.command()
async def play(ctx, *, message):
    if ctx.author.id in bot_access:
        game = discord.Game(
            name=message
        )
        await koala.change_presence(activity=game)
        await ctx.reply(f"Koala is playing `{message}`")
    else:
         await ctx.send(embed=no_access_embed)

@koala.command()
async def listen(ctx, *, message):
    if ctx.author.id in bot_access:
        await koala.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, 
                name=message, 
            ))
        await ctx.reply(f"Koala is listening `{message}`")
    else:
         await ctx.send(embed=no_access_embed)

@koala.command()
async def watch(ctx, *, message):
    if ctx.author.id in bot_access:
        await koala.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name=message
            ))
        await ctx.reply(f'Koala is watching `{message}`')
    else:
         await ctx.send(embed=no_access_embed)

@koala.command()
async def stream(ctx, *, message): 
    if ctx.author.id in bot_access:
        await koala.change_presence(activity=discord.Streaming(name=message, url="https://twitch.tv/koala_from_mars")) 
        await ctx.reply(f'Koala is streaming `{message}`')
    else:
         await ctx.send(embed=no_access_embed)

@koala.command()
async def dm(ctx, member: discord.Member, *, message):
    if ctx.author.id in bot_access:
        channel = await member.create_dm()
        await channel.send(message)
        embed = discord.Embed(title="Koala DM", description=f"DM has been sent to {member}", color=color)
        await ctx.reply(embed=embed)
    else:
        await ctx.reply(embed=no_access_embed)  

@koala.command()
async def note(ctx, *, msg):
     embed = discord.Embed(title="MESSAGE", description=f"<@{ctx.author.id}> says `{msg}`")
     await koala.get_channel(say_channel).send(embed=embed)
     await ctx.reply(":koala::white_check_mark:")

@koala.command()
async def todo(ctx, *, msg):
     if ctx.author.id == owner:
        embed = discord.Embed(title="TO-DO", description=f"{msg}")
        await koala.get_channel(reminder_channel).send(f"<@{ctx.author.id}>", embed=embed)
        await ctx.reply(":koala::white_check_mark:")
     else:
         await ctx.reply(embed=no_access_embed)

@koala.command()
async def wizzer(ctx, aliases=["nuker"]):
     embed = discord.Embed(title="Koala wizzer", description="Not public :x:",color=color)
     await ctx.send(embed=embed)

@koala.command()
async def github(ctx , * , text):
    await ctx.reply(f"> Found this: \nhttps://github.com/{text}")

@koala.command()
async def vcbot(ctx):
    await ctx.reply(".")

koala.run(token)
