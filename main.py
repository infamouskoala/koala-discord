import discord
from discord.ext import commands
import requests
import asyncio
import os

green = "\033[1;32m"
white = "\033[1;37m" 
color = 0x979797
owner = 1157733927100883035
dmlog_channel = 1183314766647791747
say_channel = 1145005935262171196
bot_id = 1161234902973415434
reminder_channel = 1162723176598478878
prefix = open("prefix.txt","r").read()
token = input("bot token: ")
koala = commands.Bot(command_prefix=prefix, intents = discord.Intents.all(), help_command=None)
bot_access = [1153710913103343729, 1157733927100883035]
no_access_embed = discord.Embed(title="Koala Error", description="You cannot run the given command.", color=color)

help_menu = discord.Embed(title = "DOWNLOAD LINKS", description = """
- sb = latest selfbot version
- prevsb = download older selfbot versions
- wizzer = koala wizzer status
- vcbot = koala vcbot link
- botsource = koala bot source code
- koalahook = koala hook repository
""",color=color)

help_menu2 = discord.Embed(title = "BOT COMMANDS", description = """
- note = send a message in <#1145005935262171196>
- github [post `https://github.com/`] = gthub finder 
- tenor [post `https://tenor.com/view/`] = embed tenor gifs 
- youtube [post `https://youtube.com/`] = embed youtube links
- botconfig = [OWNER ONLY]
""",color=color)
bot_config = discord.Embed(title = "BOT CONFIG", description = "shutdown,\nlisten,\nwatch,\nplay,\nstream,\ndm @ msg,\ntodo,\nupdateprefix (prefix)[If left null, the bot will run without prefix. Magic!]\nreboot",color=color)

def restartbot():   #restart function cuz i need it
    os.system("clear || cls")
    os.system("py main.py || python main.py")


# DM + AUTOMOD (SORTA)
@koala.event
async def on_message(message):
    if message.content == "" or message.author.id == koala.user.id:
        pass
    elif "koala sb" in message.content:
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
    elif f"<@{bot_id}>" in message.content:
        if message.author.id != bot_id:
            await message.reply(f"Hello <@{message.author.id}>, my prefix is {prefix}. Try running `{prefix}help`")

    else:
         await koala.get_channel(dmlog_channel).send(f"<@{message.author.id}> said `{message.content}` in my DMs.")
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
    await ctx.reply("download the script [here](https://github.com/infamouskoala/koalavc) or search koala's [github account](https://github.com/infamous-koala)")

@koala.command()
async def tenor(ctx, text):
    await ctx.reply(f"> Embeded tenor gif\nhttps://tenor.com/view/{text}")

@koala.command()
async def botsource(ctx):
    await ctx.reply("The bot is an opensrc project, you can download the files [here](https://github.com/infamouskoala/koala-discord) (or here is the link: https://github.com/infamouskoala/koala-discord). Make sure to star the repo :koala::heart:")

@koala.command()
async def updateprefix(ctx, *,prefix):
    if ctx.author.id in bot_access:
        file = open("prefix.txt", "w")
        writer = file.write(prefix)
        file.close()
        await ctx.reply(f"Prefix has been updated to {prefix}, restarting bot..")
        restartbot()
    else:
        await ctx.reply(embed=no_access_embed)

@koala.command()
async def koalahook(ctx):
    await ctx.reply("https://github.com/infamouskoala/koalahook") 

@koala.command()
async def youtube(ctx, *,text):
    await ctx.reply(f"> YouTube Embed \nhttps://youtube.com/{text}")

@koala.command()
async def reboot(ctx):
    if ctx.author.id in bot_access:
        await ctx.reply("KoalaNode is restarting..")
        restartbot()
        await ctx.send("KoalaNodes are back online!")
    else:
         await ctx.send(embed=no_access_embed)

koala.run(token)
