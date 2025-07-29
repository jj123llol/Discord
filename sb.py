'''

to get started install discord.py-self, and uwuipy

if you use any code from here, credit me!!
iused discord.py docs!

'''

import discord, os, time, asyncio, random, requests, json
from uwuipy import Uwuipy



print("---[[[[  loading, wait until done. ]]]]---\n\n\n")
if not os.path.exists("token.txt"):
    token = input("token: ")
    with open("token.txt", "w") as f:
        f.write(token)
    
with open("token.txt", "r") as f:
    token = f.read()
 
global settings
if not os.path.exists("Settings.json"):
    settings = {
        "prefix": ".",
        "others_allowed": True,
        "watching": [],
        "whitelisted": [],
        "afk": {},
        "consent": True
    }
    with open("Settings.json", "w") as f:
        json.dump(settings, f, indent=4)

async def Update_Settings():
    global prefix, others_allowed, watching, whitelisted, afk, consent
    time.sleep(.1)
    settings = {
        "prefix": prefix,
        "others_allowed": others_allowed,
        "watching": watching,
        "whitelisted": whitelisted,
        "afk": afk,
        "consent": consent
    }
    with open("Settings.json", "w") as f:
        json.dump(settings, f, indent=4)
        
with open("Settings.json", "r") as f:
    settings = json.load(f)
  
global prefix, others_allowed, loaded, watching, whitelisted, spam_ping, cmdlists, bot_runner, afk, consent
prefix, others_allowed = settings["prefix"], settings["others_allowed"]
afk = settings["afk"]
loaded, spam_ping = False, False
watching = settings["watching"]
whitelisted = settings["whitelisted"]
bot_runner, consent = "", settings["consent"]
cmds = {}
cmdlists = {}

async def getImg(url):
    if os.path.exists("temp.png"):
        os.remove("temp.png")
    img_data = requests.get(url).content
    with open('temp.png', 'wb') as file:
        file.write(img_data)
    file = discord.File("temp.png")
    return file
    
    
async def getGif(url):
    if os.path.exists("temp.gif"):
        os.remove("temp.gif")
    img_data = requests.get(url).content
    with open('temp.gif', 'wb') as file:
        file.write(img_data)
    file = discord.File("temp.gif")
    return file

async def tick():
    unix = time.time()
    unix = str(unix)
    unix = unix.split(".")[0]
    return int(unix)
    
async def dateToTime(date):
   unix = date.timestamp()
   unix = str(unix)
   unix = unix.split(".")[0]
   return int(unix)
   

class cmdlist:
    async def update(self):
        temp_list = []
        for cmd in cmds:
            temp_list.append(cmds[cmd]["list"])
        temp_list = temp_list[self.minn:self.maxx]
        self.comds = "\n".join(temp_list)
        await self.message.edit(self.comds + "\n\n react ▶️ or ◀️ or ❌")
    async def start(self, channel):
        global cmdlists
        self.message = await channel.send("loading..")
        self.minn = 0
        self.maxx = 5
        await self.update()
        cmdlists[self.message] = self
        return self.message
    async def next(self):
        self.minn = self.minn + 5
        self.maxx = self.maxx + 5
        if self.minn > len(cmds):
            self.minn = 0
            self.maxx = 5
        await self.update()
        
    async def back(self):
        self.minn = self.minn - 5
        self.maxx = self.maxx - 5
        if self.minn < 0:
            self.minn = 0
            self.maxx = 5
        await self.update()
        
    async def delete(self):
        await self.message.delete()
        del cmdlists[self.message]

def addcmd(name, level, lis):
    def decorator(func):
        cmds[name] = {
            "func": func,
            "level": level,
            "list": lis
        }
        return func
    return decorator
    
async def waitForReaction(emote, target, msg):
    global consent
    if consent == False:
        return True
    def check(reaction, user):
        return user.id == target.id and str(reaction.emoji) == emote and msg == reaction.message

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        return False
    else:
        return True
            
            
@addcmd("ping", 1, "ping")
async def ping(msg, message, self):
    await message.reply(f"hello, <@{message.author.id}>. pong!")

@addcmd("insult", 1, "insult @someone")
async def insult(msg, message, self):
    for mention in message.mentions:
        insults = ["smells bad", "looks bad", "is a horrible friend"]
        await message.channel.send(f"<@{mention.id}> " + insults[random.randint(0, len(insults)-1)])
    
        
@addcmd("compliment", 1, "compliment @someone")
async def compliment(msg, message, self):
    for mention in message.mentions:
        comps = ["looks good", "smells good", "is a good friend", "is pretty"]
        await message.channel.send(f"<@{mention.id}> " + comps[random.randint(0, len(comps)-1)])
    
        
@addcmd("afk", 1, "afk (reason)")
async def afkz(msg, message, self):
    global afk
    if str(message.author.id) in afk:
        await message.reply("no longer afk")
        del afk[str(message.author.id)]
        await Update_Settings()
        return ""
    unix = str(await tick())
    msg = " ".join(msg)
    msg = msg + f"\nafking since: <t:{unix}:R>"
    afk[str(message.author.id)] = msg
    await message.reply(f"afking for {msg}")
    await Update_Settings()

@addcmd("unafk", 1, "unafk")
async def unafk(msg, message, self):
    global afk
    try:
        del afk[message.author.id]
        await message.reply("afk off")
        await Update_Settings()
    except:
        await message.reply("failed")

@addcmd("disclaimer", 1, "disclaimer")        
async def disclaimer(msg, message, seld):
    await message.reply("this is not a selfbot, im manually replying")

@addcmd("setprefix", 2, "setprefix (prefix)")  
async def setprefix(msg, message, self):
    global prefix
    prefix = msg[0]
    await message.edit(f"prefix changed to `{prefix}`")
    await Update_Settings()

    
@addcmd("ghostping", 1, "ghostping @someone")            
async def ghostping(msg, message, self):
    mentions = message.mentions
    try:
        await message.delete()
    except:
        await message.reply("cant delete msg")
    for mention in mentions:
        sent = await message.channel.send(f"<@{mention.id}> ping!")
        time.sleep(1)
        await sent.delete()
       

@addcmd("sex", 1, "sex @someone")              
async def sex(msg, message, self):
    for mention in message.mentions:
        new_msg = await message.channel.send(f"<@{mention.id}>, do you wanna have sex with <@{message.author.id}>? react with 👍 if yes. no reaction within 30 seconds means no.")
        consent = await waitForReaction('👍', mention, new_msg)
        if consent == False:
            await message.reply(f'rizz-quirements not met, <@{message.author.id}> has no rizz!:broken_heart:')
            await new_msg.delete()
        else:
            await message.reply(f' <@{message.author.id}> sucessfully fucked <@{mention.id}>!:tongue:')
            await new_msg.delete()
            
@addcmd("date", 1, "date @someone")              
async def date(msg, message, self):
    for mention in message.mentions:
        new_msg = await message.channel.send(f"<@{mention.id}>,  <@{message.author.id}> asks you on a date! do you agree? react with 👍 if yes. no reaction within 30 seconds means no.")
        consent = await waitForReaction('👍', mention, new_msg)
        if consent == False:
            await message.reply(f'rizz-quirements not met, <@{message.author.id}> has no rizz!:broken_heart:')
            await new_msg.delete()
        else:
            await message.reply(f' <@{message.author.id}> sucessfully had a date with <@{mention.id}>:rose:!')
            await new_msg.delete()
  
            
@addcmd("cuddle", 1, "cuddle @someone")           
async def cuddle(msg, message, self):
    for mention in message.mentions:
        new_msg = await message.channel.send(f"<@{mention.id}>,  <@{message.author.id}> asks you to cuddle! do you agree? react with 👍 if yes. no reaction within 30 seconds means no.")
        consent = await waitForReaction('👍', mention, new_msg)
        if consent == False:
            await message.reply(f'rizz-quirements not met, <@{message.author.id}> has no rizz!:broken_heart:')
            await new_msg.delete()
        else:
            await message.reply(f' <@{message.author.id}> and <@{mention.id}> cuddled! :people_hugging::heart:!')
            await new_msg.delete()         
                 
                           
@addcmd("blow", 1, "blow @someone")              
async def vloe(msg, message, self):
    for mention in message.mentions:
        new_msg = await message.channel.send(f"<@{mention.id}>, do you wanna be blown by <@{message.author.id}>? react with 👍 if yes. no reaction within 30 seconds means no.")
        consent = await waitForReaction('👍', mention, new_msg)
        if consent == False:
            await message.reply(f'rizz-quirements not met, <@{message.author.id}> has no rizz!:broken_heart:')
            await new_msg.delete()
        else:
            await new_msg.edit("processing..")
            imgs = [
            "https://raw.githubusercontent.com/jj123llol/Discord/refs/heads/main/Screenshot_20250724-001001-813.png",
            "https://raw.githubusercontent.com/jj123llol/Discord/refs/heads/main/Screenshot_20250724-012440-666.png"
            ]
            picture = await getImg(imgs[random.randint(0, len(imgs)-1)])
            try:
                await message.reply(f' <@{message.author.id}> sucessfully sucked off <@{mention.id}>!', file=picture)
            except:
                await message.reply(f' <@{message.author.id}> sucessfully sucked off <@{mention.id}>!')
            await new_msg.delete()
            
            
@addcmd("cat", 1, "cat")
async def cat(msg, message, self):
    msg = await message.channel.send("sending..(time depends on internet)")
    cat = await getImg("https://cataas.com/cat")
    await message.reply("Meow :cat:!", file=cat)
    await msg.delete()

@addcmd("multicat", 1, "multicat")
async def multicat(msg, message, self):
    msg = await message.channel.send("sending..this may take a minute.. (time depends on internet)")
    cats = []
    i = 0
    while i != 10:
        i = i + 1
        cats.append(await getImg("https://cataas.com/cat"))
    try:
        await message.reply("Meow :cat:!", files=cats)
    except:
        await message.reply("failed to send!")
    await msg.delete()
    
@addcmd("catgif", 1, "catgif")
async def catgif(msg, message, self):
    msg = await message.channel.send("sending..(time depends on internet)")
    cat = await getGif("https://cataas.com/cat/gif")
    try:
        await message.reply("Meow :cat:!", file=cat)
    except:
        await message.reply("failed to send!")
    await msg.delete()
    
@addcmd("currentsong", 1, "currentsong")
async def currentsong(msg, message, self):
    mention = None
    if len(message.mentions) > 0:
        mention = message.mentions[0].id     
    if mention != None:
        id = mention
    else:
        id = message.author.id
    person = None
    try:
        person = await message.channel.guild.fetch_member(id)
    except:
        person = self.get_relationship(id)
    if id == self.user.id:
        person = self
    if person == None:
        await message.reply("failed to get activity")
        return ""
    activitities = person.activities
    found = False
    for activ in activitities:
        if str(activ) == "Spotify":
            found = True
            artists = ", ".join(activ.artists)
            await message.reply(activ.album_cover_url)
            await message.channel.send(f"Album: {activ.album}\nSong: {activ.title}\nUrl: [tap/click me!]({activ.track_url})\nArtists: {artists}\nDuration: {str(activ.duration).split(".")[0]}\nStart: <t:{str(await dateToTime(activ.start))}:R>\nEnd: <t:{str(await dateToTime(activ.end))}:R>")
    if found == False:
        await message.reply("failed to find spotify activity")
        
@addcmd("gif", 1, "gif (img)")
async def gif(msg, message, self):
    msg = await message.reply("give us a second!")
    try:
        attach = message.attachments[0]
        file = await getGif(attach.url)
        await message.reply(files=[file])
        await msg.delete()
    except:
        await msg.edit("failed!")
    
@addcmd("avatar", 1, "avatar @someone")
async def avatar(msg, message, self):
    avatars = []
    msg = await message.reply("give us a second!")
    for mention in message.mentions:
        id = mention.id
        mention = await self.fetch_user_profile(mention.id)
        if mention.display_avatar == None:
            await message.reply(f"<@{id}> has no avatar")
            continue
        avatars.append(await mention.display_avatar.url.to_file())
    await msg.delete()
    try:
        await message.reply("",files=avatars)
    except:
        await message.reply("failed!")
    
@addcmd("multicatgif", 1, "multicatgif")
async def multicatgif(msg, message, self):
    msg = await message.channel.send("sending..this may take a minute.. (time depends on internet)")
    cats = []
    i = 0
    while i != 5:
        i = i + 1
        cats.append(await getGif("https://cataas.com/cat/gif"))
    try:
        await message.reply("Meow :cat:!", files=cats)
    except:
        await message.reply("failed")
    await msg.delete()

@addcmd("kill", 1, "kill @someone")
async def kill(msg, message, self):
    for mention in message.mentions:
        if mention.id == message.author.id:
            await message.channel.send(f"<@{mention.id}> but why?")
            continue
        new_msg = await message.channel.send(f"<@{mention.id}>, was killed by <@{message.author.id}>! :gun:")


@addcmd("timestamp", 1, "timestamp")
async def timestamp(msg, message, self):
    unix = str(await tick())
    await message.reply(f"<t:{unix}:R>")
    
@addcmd("watch", 2, "watch")
async def watch(msg, message, self):
    global watching
    channel = str(message.channel.id)
    await message.edit("watching channel..:eyes:")
    time.sleep(.5)
    await message.delete()
    watching.append(channel)
    await Update_Settings()

@addcmd("unwatch", 2, "unwatch")
async def unwatch(msg, message, self):
    global watching
    watching.remove(str(message.channel.id))
    await message.edit("no longer watching!")
    time.sleep(2)
    await message.delete()
    await Update_Settings()
    
@addcmd("lock", 2, "lock")
async def lock(msg, message, self):
    global others_allowed
    others_allowed = False
    await message.edit("locked! :lock: ")
    time.sleep(2)
    await message.delete()
    await Update_Settings()
    
@addcmd("unlock", 2, "unlock")
async def unlock(msg, message, self):
    global others_allowed
    others_allowed = True
    await message.edit("unlocked! :unlock:")
    time.sleep(2)
    await message.delete()
    await Update_Settings()
    

@addcmd("kiss", 1, "kiss @someone")
async def kiss(msg, message, self):
    for mention in message.mentions:
        await message.reply(f"<@{message.author.id}> kisses <@{mention.id}>! :kiss:")
        
@addcmd("hug", 1, "hug @someone")
async def hug(msg, message, self):
    for mention in message.mentions:
        await message.reply(f"<@{message.author.id}> hugs <@{mention.id}>! :people_hugging: ")



@addcmd("ppsize", 1, "ppsize @someone")
async def ppsize(msg, message, self):
    for mention in message.mentions:
        if mention.id == 1195825285866717215:
            size = "infinite"
        else:
            size = str(random.randint(0, 30))
            
        await message.reply(f"<@{mention.id}> has a pp size of " + size + " inches !")
         
         
@addcmd("gaymeter", 1, "gaymeter @someone")
async def gaymeter(msg, message, self):
    for mention in message.mentions:
        if mention.id == 1195825285866717215:
            gay = "0"
        else:
            gay = str(random.randint(0, 100))
            
        await message.reply(f"<@{mention.id}> is " + gay + "% gay!")
        

@addcmd("punch", 1, "punch @someone")
async def punch(msg, message, self):
    for mention in message.mentions:
        await message.reply(f"<@{message.author.id}> punched <@{mention.id}>! :punch:")
        
@addcmd("cmds", 1, "cmds")
async def cmdz(msg, message, self):
   cmdlistt = cmdlist()
   msg = await cmdlistt.start(message.channel)
   
   

@addcmd("whitelist", 2, "whitelist")
async def whitelist(msg, message, self):
    global whitelisted
    whitelisted.append(str(message.channel.id))
    await message.edit(f"channel whitelisted, do `{prefix}cmds` to get started!")
    await Update_Settings()
    
@addcmd("unwhitelist", 2, "unwhitelist")
async def unwhitelist(msg, message, self):
    global whitelisted
    whitelisted.remove(str(message.channel.id))
    await message.edit("unwhitelisted")
    await Update_Settings()
    
@addcmd("spamping", 2, "spamping @someone")
async def spamping(msg, message, self):
    global spam_ping
    spam_ping = True
    if len(message.mentions) < 1:
        await message.edit("ping someone")
        time.sleep(2)
        await message.delete()
        return ""
    ping = message.mentions[0].id
    channel = message.channel
    await message.delete()
    while spam_ping == True:
        time.sleep(random.randint(1, 10))
        await channel.send(f"<@{ping}>")
        
@addcmd("unspamping", 2, "unspamping")
async def unspamping(msg, message, self):
    global spam_ping
    spam_ping = False
    await message.edit("turned off!")
    time.sleep(2)
    await message.delete()
    
@addcmd("gamble", 1, "gamble")
async def gamble(msg, message, self):
    num = random.randint(1, 2)
    if num == 1:
        await message.reply("winner!")
    else:
        await message.reply("fucking loser get good")
        
@addcmd("pie", 1, "pie")
async def pie(msg, message, self):
    num = random.randint(1, 2)
    if num == 1:
        await message.reply("eat up :pie:")
    else:
        await message.reply("oven exoloded:boom:")
        
@addcmd("8ball", 1, "8ball")
async def ball(msg, message, self):
    choices = [
    "likey", "outlook bad", "maybe", "yes", "no", "idfk man im js a ball"
    ]
    num = random.randint(0, len(choices)-1)
    await message.reply(choices[num])
        
@addcmd("nuke", 2, "nuke")
async def nuke(msg, message, self):
    await message.edit("woah! this command is dangerous. react :thumbsup: to confirm.")
    passed = await waitForReaction('👍', bot_runner, message)
    if passed == False:
        await message.edit("command aborted")
        time.sleep(2)
        await message.delete()
        return ""
    await message.delete()
    channels = []
    try:
        channels.append(await message.guild.create_text_channel("ant was here"))
    except:
        await message.channel.send("failed")
        return ""
    i = 0
    while i < 20:
        i = i + 1
        channels.append(await message.guild.create_text_channel("ant was here"))
        time.sleep(.5)
    for channel in channels:
        await channel.send("@everyone")
        
@addcmd("dm", 2, "dm @someone (msg)")
async def dm(msg, message, self):
    mention = message.mentions[0]
    msg.pop(0)
    msg = " ".join(msg)
    await message.delete()
    dm = await self.create_dm(mention)
    await dm.send(msg)
    
    
@addcmd("clone",2, "clone")
async def clone(msg, message, self):
    await message.edit("are you sure react :thumbsup: to confirm.?")
    consent = await waitForReaction('👍', self.user, message)
    if consent == False:
       await message.delete()
       return ""
    try:
        clone = await message.channel.clone()
        await clone.edit(position=message.channel.position)
        await message.channel.delete()
    except:
        await message.channel.send("failed")
        
        
        
@addcmd("spam", 2, "spam (msg)")
async def spam(msg, message, self):
    global spam_ping
    msg = " ".join(msg)
    spam_ping = True
    channel = message.channel
    await message.delete()
    while spam_ping == True:
        time.sleep(random.randint(1, 3))
        await channel.send(msg)
        
@addcmd("unspam", 2, "unspam")
async def unspam(msg, message, self):
    global spam_ping
    spam_ping = False
    await message.edit("turned off!")
    time.sleep(2)
    await message.delete()


@addcmd("banner", 1, "banner @someone")
async def banners(msg, message, self):
    banners = []
    msg = await message.reply("give us a second!")
    for mention in message.mentions:
        id = mention.id
        mention = await self.fetch_user_profile(mention.id)
        if mention.display_banner == None:
            await message.reply(f"<@{id}> has no display banner")
            continue
        banners.append(await mention.display_banner.to_file())
    await msg.delete()
    try:
        await message.reply("",files=banners)
    except:
        await message.reply("failed!")
        
@addcmd("servericon",1,"servericon") 
async def servericon(msg, message,self):
    msg = await message.reply("give us a second!")
    try:
        file = await message.channel.guild.icon.to_file()
    except:
        await msg.edit("not a guild/no icon!")
        return ""
    try:
        await message.reply("",files=[file])
    except:
        await message.reply("failed!")
    await msg.delete()

@addcmd("uwuify",1,"uwuify (msg)") 
async def uwuify(msg, message,self):
    msg = " ".join(msg)
    uwu = Uwuipy()
    await message.reply(uwu.uwuify(msg))

 
@addcmd("lick",1,"lick @person") 
async def lick(msg, message,self):
    for mention in message.mentions:
        await message.reply(f"<@{message.author.id}> licked <@{mention.id}> :tongue:")
        
        
@addcmd("itemshop", 1, "itemshop")
async def itemshop(msf, message, self):
    await message.reply("https://www.fortnite.com/item-shop?lang=en-US")
    
    
@addcmd("consenton", 2, "consenton")
async def consenton(msf, message, self):
    global consent
    consent = True
    await message.reply("Consent on!")
    await Update_Settings()
    
@addcmd("consentoff", 2, "consentoff")
async def consentoff(msf, message, self):
    global consent
    consent = False
    await message.reply("Consent off!")
    await Update_Settings()
    
    
#######
class MyClient(discord.Client):
    async def on_message_edit(self, before, after):
        if before.author == self.user:
            return ""
        global watching
        if not str(before.channel.id) in watching:
            return ""
        authorid = before.author.id
        before_content = before.content
        after_content = after.content
        await before.channel.send(f"<@{authorid}> edited a message!\nBefore: {before_content}\nAfter: {after_content}")
        
    async def on_message_delete(self, message):
        if message.author == self.user:
            return ""
        global watching
        if not str(message.channel.id) in watching:
            return ""
        author = message.author
        content = message.content
        await message.channel.send(f"<@{author.id}> deleted: {content}")
        
        
     
    async def on_reaction_add(self, reaction, user):
        global cmdlists
        if reaction.message in cmdlists:
            if str(reaction.emoji) == '▶️':
                await cmdlists[reaction.message].next()
            elif str(reaction.emoji) == '◀️':
                await cmdlists[reaction.message].back()
            elif str(reaction.emoji) == '❌':
                await cmdlists[reaction.message].delete()
                
    async def on_guild_remove(self, guild):
        print(f"User was kicked from/left guild: {guild.name}")
        
    async def on_ready(self):
        global loaded, bot_runner
        bot_runner = self.user
        loaded = True
        try:
            os.system('clear')
        except:
            os.system('cls')
        print(f"---[[[[ fully loaded, {bot_runner.display_name}. Made by ant<3 ]]]]---")
        print(str(len(cmds))+" commands")

    async def on_message(self, message):
        global afk, prefix, loaded, others_allowed, whitelisted
        content = message.content
        if len(message.mentions) > 0:
            for mention in message.mentions:
                if str(mention.id) in afk and message.author != self.user:
                   await message.reply(f"<@{mention.id}> is afk for: " + afk[mention.id])
        if not content.startswith(prefix):
            return ""
        if self.user != message.author and others_allowed == False:
            return ""
        if others_allowed == True and self.user != message.author and not str(message.channel.id) in whitelisted:
            return ""
        try:
            msg = content.split()
            cmd = list(msg[0])
            msg.pop(0)
            for i in list(prefix):
                cmd.pop(0)
            cmd = "".join(cmd)
            if cmd in cmds:
                if cmds[cmd]["level"] == 2 and self.user != message.author:
                    await message.reply("missing perms")
                    return ""
                await cmds[cmd]["func"](msg, message, self)
        except Exception as e:
            print(e)
            

client = MyClient()
client.run(token)