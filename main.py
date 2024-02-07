import os
import discord
from discord.ext import commands
import json

# config and main.py updated

green = "\033[1;32m"
white = "\033[1;37m" 
color = 0x979797

#using prefix.txt instead of loading from json so that i can change the prefix during runtime and rerun the file to save changes
prefix = open("src/prefix.txt","r").read()  
configfile = open('src/config.json')
data = json.load(configfile)
token = data["token"]
dmlog_channel = data["dmlog_channel"]
owner = data["owner"]
say_channel = data["saychannel"]
reminder_channel = data["reminder_channel"]
bot_access = data["botaccess"]
ownerid = data["owner"]
koalamodlog= data["modlogs"]
koalalog = data["logchannel"]

afkvalue = False
deb = False

koala = commands.Bot(command_prefix=prefix, intents = discord.Intents.all(), help_command=None)
no_access_embed = discord.Embed(title="Koala Error", description="You cannot run the given command.", color=color)
deleted_message = None
deleted_message_author = None
afkmessage = None

help_menu = discord.Embed(description = """
- DOWNLOAD LINKS
`sb, prevsb, wizzer, vcbot, botsource, koalahook`

- BOT COMMANDS
`note, github <accountname/repo>, tenor <gifid>, find <@user>, snipe, embed [msg]`

- MOD COMMANDS
`kick @user reason, ban @user reason, warn <userid>, editwarn <userid> <amount>, checkwarns <userid>, purge <amount>`
""",color=color)

bot_config = discord.Embed(title = "", description = """
### Bot Admin Commands
shutdown = shutdown the bot
listen = RPC listen
watch = RPC watch
play = RPC play
stream = RPC streaming
dm (@abc) (msg) = DM user
updateprefix (prefix) = Update Bot Prefix
reboot = Reboot the bot

### Owner Only
todo 
afk
exc
pingtgl
""",color=color)

def restartbot():   #restart function cuz i need it
    os.system("clear || cls")
    os.system("py main.py || python main.py")

@koala.event
async def on_member_join(member):
   await koala.get_channel(koalalog).send(f"[+] {member.mention} has joined")

@koala.event
async def on_member_remove(member):
   await koala.get_channel(koalalog).send(f"[-] {member.mention} has left")

# DM + AUTOMOD (SORTA)
@koala.event
async def on_message(message):
    # LOG EVERY SINGLE MESSAGE IN THE ENTIRE SERVER LMFAO
    # if message.content == "":
    #     pass
    # else:
    #     embed = discord.Embed(title="Message", description=f"<@{message.author.id}> said `{message.content}` in <#{message.channel.id}>", color=color)
    #     await koala.get_channel(messagelogs).send(embed=embed)

    if isinstance(message.channel, discord.DMChannel):
        embed = discord.Embed(title="DM", description=f"<@{message.author.id}> dmed me '{message.content}'")
        await koala.get_channel(dmlog_channel).send(embed=embed)

    elif "tools" in message.content or "scripts" in message.content:
        if message.author.id != koala.user.id:
            id = message.channel.id #maybe idk
            await message.reply("The tools that Koala use in his videos are either publlic or they are not public. The public ones can be found on his [github](https://github.com/infamous-koala).")
        else:
            pass

    elif f"<@{koala.user.id}>" in message.content:
        if message.author.id != koala.user.id:
            await message.reply(f"Hello <@{message.author.id}>, my prefix is {prefix}. Try running `{prefix}help`")
    
    elif f"<@{owner}>" in message.content:
        if message.author.id != koala.user.id:
            if afkvalue == True:
                embed = discord.Embed(description=f"Owner is afk", color=color)
                await message.reply(f"{afkmessage}", embed=embed)
            else:
                pass
        else:
            pass
    else:
         pass
    await koala.process_commands(message)

@koala.event
async def on_message_delete(message):
    global deleted_message
    global deleted_message_author
    deleted_message=message.content
    deleted_message_author=message.author.id
    embed = discord.Embed(title="Delete", description=f"Message deleted in <#{message.channel.id}> by <@{message.author.id}>. Content: `{message.content}`", color=color)
    await koala.get_channel(koalalog).send(embed=embed)

@koala.event
async def on_message_edit(message_before, message_after):
    embed = discord.Embed(title="Edit", description=f"<@{message_before.author.id}> edited a message in <#{message_before.channel.id}>, `{message_before.content}` to `{message_after.content}`", color=color)
    await koala.get_channel(koalalog).send(embed=embed)

@koala.event
async def on_command_error(ctx, error):
    if deb == True:
        await ctx.send(f"Bot Error: `{error}`")
    else: 
        pass

@koala.command()
async def help(ctx):
    try:
        await ctx.reply(embed=help_menu)
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
    embed = discord.Embed(title="Koala Userbot", description="v1.0: Release\nv1.5: v1 patched\n recode\n re v2: [download](https://www.mediafire.com/file/wnm6f0buu80v598/Koala_Selfbot_v2.zip/file)",color=color)
    await ctx.reply(embed=embed)
    
@koala.command()
async def sb(ctx):
    embed = discord.Embed(title="Koala Userbot", description=f"Hello <@{ctx.author.id}>, we are no longer in the mainstream botting com, you can read about it here: https://discord.com/channels/1095595243417649175/1095645247536648222/1157221000799326349\ndownload the selfbot by clicking [here](https://www.mediafire.com/file/wnm6f0buu80v598/Koala_Selfbot_v2.zip/file)", color=color)
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
         await koala.close()
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
	await ctx.reply("https://github.com/infamouskoala/Koala-Nuker")

@koala.command()
async def vcbot(ctx):
    await ctx.reply("download the script [here](https://github.com/infamouskoala/koalavc) or search koala's [github account](https://github.com/infamouskoala)")

@koala.command()
async def github(ctx ,text):
    message = text.replace("@","naughty boy :smirk: we have already found the bug and fixed it")
    await ctx.reply(f"> Found this: \nhttps://github.com/{message}")

@koala.command()
async def tenor(ctx, text):
    message = text.replace("@","naughty boy :smirk: we have already found the bug and fixed it")
    await ctx.reply(f"> Embeded tenor gif\nhttps://tenor.com/view/{message}")

@koala.command()
async def botsource(ctx):
    await ctx.reply("The bot is an opensrc project, you can download the files [here](https://github.com/infamouskoala/koala-discord) (or here is the link: https://github.com/infamouskoala/koala-discord). Make sure to star the repo :koala::heart:")

@koala.command()
async def updateprefix(ctx, *,prefix):
    if ctx.author.id in bot_access:
        file = open("src/prefix.txt", "w")
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
async def reboot(ctx):
    if ctx.author.id in bot_access:
        await ctx.reply("KoalaNode is restarting..")
        restartbot()
        await ctx.send("KoalaNodes are back online!")
    else:
         await ctx.send(embed=no_access_embed)

@koala.command()
async def afk(ctx, *, message):
    if ctx.author.id == owner:
        global afkvalue
        afkvalue = True
        global afkmessage
        afkmessage=message
        await ctx.reply("You're now afk!")
    else:
        await ctx.reply(embed=no_access_embed)

@koala.command()
async def unafk(ctx):
    if ctx.author.id == owner:
        global afkvalue
        afkvalue = False
        await ctx.reply("You're no longer afk!")
    else:
        await ctx.reply(embed=no_access_embed)

@koala.command()
async def purge(ctx, limit: int):
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=limit)
        await ctx.message.delete()
        await ctx.send(f'Purged {limit} messages.')
        await koala.get_channel(koalamodlog).send(f"[:wastebasket:] <@{ctx.author.id}> cleared {limit} messages in {ctx.channel}")
    else:
        await ctx.reply(":x: You don't have perms to perform this task")

@koala.command()
async def kick(ctx, member: discord.Member, *, reason):
    if ctx.message.author.guild_permissions.kick_members:
        if reason == "" or member == None:
            await ctx.reply("reason or member invalid, command usage:\n> kick @mention reason")
        else:
            await member.send(f'You have been kicked from {ctx.guild.name} for `{reason}`.')
            await member.kick(reason=reason)
            await ctx.send(f'Kicked {member.mention}')
            await koala.get_channel(koalamodlog).send(f"[:boot:] <@{ctx.author.id}> kicked {member} for `{reason}`")
    else:
        await ctx.reply(":x: You don't have perms to perform this task")

@koala.command()
async def ban(ctx, member: discord.Member, *, reason):
    if ctx.message.author.guild_permissions.ban_members:
        if reason == "" or member == None:
            await ctx.reply("reason or member invalid, command usage:\n> ban @mention reason")
        else:
            await member.send(f'You have been banned from {ctx.guild.name}. for `{reason}`.')
            await member.ban(delete_message_days=0,reason=reason)
            await ctx.send(f'Banned {member.mention}')
            await koala.get_channel(koalamodlog).send(f"[:hammer:] <@{ctx.author.id}> banned {member} for `{reason}`")
    else:
        await ctx.reply(":x: You don't have perms to perform this task")

@koala.command()
async def warn(ctx, user_id: int):
    if ctx.message.author.guild_permissions.manage_messages:
        user = koala.get_user(user_id)
        if not user:
            await ctx.reply(":koala::x: Invalid user ID.")
            return
        file_path = f"src/warns/{user_id}.txt"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                warnings = int(file.read().strip())
            warnings += 1
            with open(file_path, 'w') as file:
                file.write(str(warnings))
            await ctx.send(f"<@{user_id}> now has {warnings} warnings.")
            await ctx.get_channel(koalamodlog).send(f"[:speaking_head:]<@{ctx.author.id}> warned <@{user_id}>")
        else:
            with open(file_path, 'w') as file:
                file.write("1")
            await ctx.send(f"<@{user_id}> now has 1 warning.")
    else:
        await ctx.reply(":x: You don't have perms to perform this task")

@koala.command()
async def checkwarns(ctx, user_id: int):
    user = koala.get_user(user_id)
    if not user:
        await ctx.send(":koala::x: Invalid user ID")
        return
    file_path = f"src/warns/{user_id}.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            warnings = int(file.read().strip())
        await ctx.send(f"<@{user_id}> has {warnings} warnings.")
    else:
        await ctx.send(f"<@{user_id}> does not have any warnings.")

@koala.command()
async def editwarn(ctx, user_id: int, new_warnings: int):
    if ctx.message.author.guild_permissions.administrator:
        user = koala.get_user(user_id)
        if not user:
            await ctx.reply(":koala::x:Invalid user ID.")
            return
        file_path = f"src/warns/{user_id}.txt"
        if os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(str(new_warnings))
            await ctx.send(f"<@{user_id}> now has {new_warnings} warnings.")
            await ctx.get_channel(koalamodlog).send(f"[:speaking_head:]<@{ctx.author.id}> appended warnings for <@{user_id}> to {new_warnings}")

        else:
            await ctx.send(f"<@{user_id}> does not have any warnings.")
    else:
        await ctx.reply(":x: You don't have perms to perform this task")

@koala.command()
async def find(ctx, member: discord.Member):
    embed = discord.Embed(title="Person Finder", description=f"<@{ctx.author.id}> has found {member.mention}, they will now do nasty things to them :flushed:", color=color)
    await ctx.reply(embed=embed)

@koala.command()
async def snipe(ctx):
    embed = discord.Embed(title="Sniped Message", description=f"User: <@{deleted_message_author}>\ncontent: {deleted_message}", color=color)
    await ctx.reply(embed=embed)

@koala.command()
async def embed(ctx, *, description):
    embed = discord.Embed(title="Koala Bot Embed", description=f"{description}\nby <@{ctx.author.id}>", color=color)
    message = ctx.message
    await message.delete()
    await ctx.send(embed=embed)

@koala.command()
async def debug(ctx):
    if ctx.author.id in bot_access:
        global deb
        if deb == True:
            await ctx.reply("Debug is enabled, disabling now...")
            deb = False
        elif deb == False:
            await ctx.reply("Debug is disabled, enabling now...")
            deb = True
    else:
        await ctx.reply(embed=no_access_embed)

@koala.command()
async def exc(ctx, *, cmd):
    if ctx.author.id == ownerid:
        await ctx.reply("Remote execution started, waiting for the output...")
        exec(cmd)
        await ctx.send("Code executed :white_check_mark:")
    else:
        await ctx.reply(embed=no_access_embed)

koala.run(token)
