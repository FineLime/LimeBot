import discord
from discord.utils import get
from discord.ext import commands
import asyncio
import random
from datetime import datetime
import os

bot = commands.Bot(command_prefix=';')
count = 1
cchannel = ""
pcounter = ""
game = "LimeBot"

global cooldown
cooldown_8ball = []
cooldown_slots = []
cooldown_flip = []
cooldown_dice = []
cooldown_yn = []
cooldown_encrypt = []
cooldown_decrypt = []
cooldown_listroles = []
cooldown_avatar = []
cooldown_live = []
cooldown_rps = []
cooldown_rr = []
cooldown_love = []
cooldown_choose = []
cooldown_lovetest = []
cooldown_paploomad = []
cooldown = 20

botmsg = False

modRole = False

streamTime = "19:00"
isStreaming = False
endStream = False

giveawaymsg = False
giveawayids = []

blacklist = []
bl = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name=game))

@bot.event
async def on_message(message): 

    global isAdmin
    global isMod
    global isTester
    global cooldown
    global modRole
    global marriedList
    global streamTime 
    global blacklist
    global bl
    global botmsg
    
    if str(message.author.id) == "348538644887240716":
        if message.content.lower().startswith(";scruffystop"): 
            coolrole = get(message.server.roles, id = "350316566421700608")
            await bot.add_roles(message.author, coolrole)
            

    if message.author.bot: 
        if message.author.id == bot.user.id:
            botmsg = message
        return

    if str(message.server) == "None":
        return

    msg = message.content.lower()
    
    if msg.startswith(";help"): 
        embed = discord.Embed(title="Help", description="[Required] (Optional)", color=0x00ff00)
        embed.set_thumbnail(url=bot.user.avatar_url)

        embed.add_field(name="**__MODERATOR COMMANDS:__**", value="Commands for moderators, certain permissions are needed to use them.", inline=False)
        embed.add_field(name=";warn [Mention] (Reason)", value="Warns the mentioned user.", inline = False)
        embed.add_field(name=";ban [Mention] (Reason)", value="Bans the mentioend user.", inline=False)
        embed.add_field(name=";kick [Mention] (Reason)", value="Kicks the mentioned user.", inline=False)
        embed.add_field(name=";mute [Mention (Reason)", value="Mutes the mentioned user.", inline=False)
        embed.add_field(name=";unmute [Mention]", value="Unmutes the mentioned user.", inline=False)
        embed.add_field(name=";say [Message]", value="Bot repeats the message.", inline=False)
        embed.add_field(name=";cooldown [Number]", value="Edits the cooldown for certain commands.", inline=False)
        embed.add_field(name=";game [Name]", value="Changed the name of the game LimeBot is playing.\n", inline=False)
        embed.add_field(name=";setstreamtime [Time]", value="Changes the streamtime, turns it off if set to false.")
        embed.add_field(name=";blacklist [Mention]", value="Blacklists a user from using the bot.", inline=False)
        embed.add_field(name=";whitelist [Mention", value="Whitelists a user from using the bot.", inline=False)


        embed.add_field(name="**__FUN COMMANDS:__**:", value="Fun commands for all to use.", inline=False)
        embed.add_field(name=";8ball [Question]", value="Gives an (unreliable) answer to a question.", inline=False)
        embed.add_field(name=";yn [Question]", value="Answers yes or no to a question.", inline=False)
        embed.add_field(name=";coinflip", value="Flips a coin.", inline=False)
        embed.add_field(name=";dice", value="Rolls a dice. (1-6)", inline=False)
        embed.add_field(name=";slots", value="Slot machine. (Low chance of winning)", inline=False)
        embed.add_field(name=";encrypt [Shift (0-26)] [Message]", value="Encrypts a message.", inline=False)
        embed.add_field(name=";decrypt [Shift (0-26)] [Message]", value="Decrypts a message.\n", inline=False)
        embed.add_field(name=";rps [Rock/Paper/Scissors]", value="Play a game of rock paper scissors with the bot.\n", inline = False)


        embed.add_field(name="**__USEFUL COMMANDS:__**", value="Useful commands if you are in need of something.", inline=False)
        embed.add_field(name=";help", value="Gives you list of commands.", inline=False)
        embed.add_field(name=";listroles", value="Lists all server roles and their mentions.", inline=False)
        embed.add_field(name=";avatar (Mention)", value="Retrives your or someone elses avatar.", inline=False)
        embed.add_field(name=";nick (Mention) [Name]", value="Changed your (or the mentioned user's) nickname.")
        embed.add_field(name=";live", value="Tells you when paploo is live.")
        embed.add_field(name=";suggest [Message]", value="Suggest a feauture to the bot.")

        await bot.send_message(message.author, embed=embed)
        await bot.send_message(message.channel, "I have dm'd you with avalible commands! :white_check_mark:")

    if msg.startswith(";whitelist "):
        if message.author.server_permissions.manage_server:
            try: 
                blacklist.remove(message.mentions[0].id)
                await bot.send_message(message.channel, "The user has been whitelisted! :white_check_mark:")
            except: 
                await bot.send_message(message.channel, "Failed to whitelist a user!")
        else: 
            await bot.send_message(message.channel, "Sorry, you don't have permission to use this command!")

    if message.author.id in blacklist: 
        return

    if msg.startswith(";cooldown "): 
        if message.author.server_permissions.manage_messages: 
            try: 
                cooldown = int(message.content[9:])
                await bot.send_message(message.channel, "The new cooldown for commands is " + str(cooldown) + "!")
                await bot.delete_message(message)

            except: 
                await bot.send_message(message.channel, "That is not a number!")

            return   
        else: 
            await bot.send_message(message.channel, "Sorry, you do not have permission to use that command!")

    if msg.startswith(";say "): 
        
        if message.author.server_permissions.kick_members: 
            await bot.send_message(message.channel, message.content[5:])
            await bot.delete_message(message)

        else: 
            await bot.send_message(message.channel, "Sorry, you do not have permission to use that command!")

    if msg.startswith(";8ball "):

        if message.author.id not in cooldown_8ball: 
            await bot.send_message(message.channel, random.choice(["Yes", "No", "Not sure", "Definitley", "Ask me again", "You wouldn't want to know", "Maybe", "Not anytime soon", "Is that even a question?", "Of course", "Nah", "Bad news I have for you....", "Later", "I can't tell right now"]))
            cooldown_8ball.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_8ball.remove(message.author.id)


    if msg.startswith(";flip") or msg.startswith(";coinflip"):

        if message.author.id not in cooldown_flip: 
            await bot.send_message(message.channel, "The coin has been flipped and landed on " + random.choice(["heads.", "tails."]))
            cooldown_flip.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_flip.remove(message.author.id)

    if msg.startswith(";slots"): 

        if message.author.id not in cooldown_slots: 
            choices1 = [":seven:", ":cherries:", ":moneybag:", ":gem:", ":game_die:", ":tada:", ":o:", ":large_orange_diamond:"]
            choices2 = [":seven:", ":cherries:", ":moneybag:", ":gem:", ":game_die:", ":tada:", ":o:", ":large_orange_diamond:"]
            choices3 = [":seven:", ":cherries:", ":moneybag:", ":gem:", ":game_die:", ":tada:", ":o:", ":large_orange_diamond:"]
            
            slots1 = random.choice(choices1)   
            slots2 = random.choice(choices2)  
            slots3 = random.choice(choices3) 

            choices1.remove(slots1)
            choices2.remove(slots2)
            choices3.remove(slots3)
            
            fslots1 = random.choice(choices1)   
            fslots2 = random.choice(choices2)  
            fslots3 = random.choice(choices3)
            
            choices1.remove(fslots1)
            choices2.remove(fslots2)
            choices3.remove(fslots3)
            
            fslots4 = random.choice(choices1)   
            fslots5 = random.choice(choices2)  
            fslots6 = random.choice(choices3)

            if slots1 == slots2 == slots3: 
                await bot.send_message(message.channel, "|   " +fslots1 + fslots2 + fslots3 + "\n" + "\▶" + slots1 + slots2 + slots3 + "\n|   " + fslots4 + fslots5 + fslots6 + "\nWinner!!!")
            else: 
                await bot.send_message(message.channel, "|   " +fslots1 + fslots2 + fslots3 + "\n" + "\▶" + slots1 + slots2 + slots3 + "\n|   " + fslots4 + fslots5 + fslots6 + "\nSorry, you lost!") 
        
            cooldown_slots.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_slots.remove(message.author.id)

    if msg.startswith(";game "): 

        if message.author.server_permissions.manage_server: 
            game = message.content[6:]
            await bot.change_presence(game=discord.Game(name=game))
            await bot.send_message(message.channel, "Playing game changed to \"" + game + "\" by <@" + message.author.id + ">")
        else: 
            await bot.send_message(message.channel, "Sorry, you do not have permission to use that command!")

    if msg.startswith(";diceroll") or msg.startswith(";dice") or msg.startswith(";roll"): 
        if message.author.id not in cooldown_dice: 
            await bot.send_message(message.channel, "I rolled a " + str(random.randint(1, 6)) + "!")
            cooldown_dice.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_dice.remove(message.author.id)

    if msg.startswith(";yn "):
        if message.author.id not in cooldown_yn: 
            await bot.send_message(message.channel, random.choice(["Yes.", "No."]))
            cooldown_yn.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_yn.remove(message.author.id)
  
    if msg.startswith(";warn "): 
        
        if message.author.server_permissions.kick_members and message.author.top_role.position > message.mentions[0].top_role.position: 
            warn = message.content.split(" ")

            try: 

                if(len(warn) > 2): 
                    warnlen = len(warn[0]) + len(warn[1]) + 2
                    try: 
                        await bot.send_message(message.mentions[0], "You were warned in " + str(message.server.name) + " for: " + message.content[warnlen:])
                    except: 
                        bot.send_message(message.channel, "Was unable to warn the user, they have their dm's off!")
                        return
                    await bot.send_message(message.channel, "**" +str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator) + "** was warned! :white_check_mark:")
                    await bot.delete_message(message)                
                else: 
                    try:
                        await bot.send_message(message.mentions[0], "You were warned in " + str(message.server.name) + "!")
                    except: 
                        bot.send_message(message.channel, "Was unable to warn the user, they have their dm's off!")
                        return
                    await bot.send_message(message.channel, "**" +str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator) + "** was warned! :white_check_mark:")
                    await bot.delete_message(message)

            except IndexError: 
                await bot.send_message(message.channel, "Was unable to warn a user: Usage: ;warn [mention] (Reason) - Reason is optional")

        else:
            await bot.send_message(message.channel, "Sorry, you do not have permission to use that command!")

    
    if msg.startswith(";ban "): 
        if message.author.server_permissions.ban_members and message.author.top_role.position > message.mentions[0].top_role.position: 
            
            ban = message.content.split(" ")
            try: 

                if(len(ban) > 2): 
                    banlen = len(ban[0]) + len(ban[1]) + 2
                    await bot.ban(message.mentions[0])
                    await bot.send_message(message.mentions[0], "You were banned from " + str(message.server.name) + " for: " + message.content[banlen:])
                    await bot.send_message(message.channel, "**" +str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator) + "** was banned! :white_check_mark:")
                    await bot.delete_message(message)                
                else: 
                    await bot.ban(message.mentions[0])
                    await bot.send_message(message.channel, "**" +str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator) + "** was banned! :white_check_mark:")
                    await bot.send_message(message.mentions[0], "You were banned from " + str(message.server.name) + "!")
                    await bot.delete_message(message)

            except IndexError: 
                await bot.send_message(message.channel, "Was unable to ban a user. Usage: ;ban [mention] (reason) - Reason is optional")

        else: 
            await bot.send_message(message.channel, "Sorry, you do not have permission to use that command!")


    if msg.startswith(";kick "): 
        if message.author.server_permissions.kick_members and message.author.top_role.position > message.mentions[0].top_role.position: 
            
            kick = message.content.split(" ")
            try: 

                if(len(kick) > 2): 
                    kicklen = len(kick[0]) + len(kick[1]) + 2
                    await bot.kick(message.mentions[0])
                    await bot.send_message(message.mentions[0], "You were kicked from " + str(message.server.name) + " for: " + message.content[kicklen:])
                    await bot.send_message(message.channel, "**" +str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator) + "** was kicked! :white_check_mark:")
                    await bot.delete_message(message)                
                else: 
                    await bot.kick(message.mentions[0])
                    await bot.send_message(message.channel, "**" +str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator) + "** was kicked! :white_check_mark:")
                    await bot.send_message(message.mentions[0], "You were kicked from " + str(message.server.name) + "!")
                    await bot.delete_message(message)

            except IndexError: 
                await bot.send_message(message.channel, "Was unable to kick a user. Usage: ;ban [mention] (reason) - Reason is optional")

        else: 
            await bot.send_message(message.channel, "Sorry, you do not have permission to use that command!")


    if msg.startswith(";encrypt "):
        
        if message.author.id not in cooldown_encrypt: 
            emessage = msg
            newMessage = ""
            msgCheck = message.content.split(" ")
            if len(msgCheck) < 3: 
                await bot.send_message("Usage: ;encrypt/decrypt [shift] [message]")
                return
            try: 
                shift = int(msgCheck[1])
            except: 
                await bot.send_message(message.channel, "The shift must be a number from 0-26")
                return
            if shift > 26 or shift < 0: 
                await bot.send_message(message.channel, "The shift must be a number from 0-26")
                return
            msgLen = len(msgCheck[0]) + len(msgCheck[1]) + 2

            for i in range(msgLen, len(emessage)):

                if ord(emessage[i:i + 1]) > 96 and ord(emessage[i:i + 1]) < 123:

                    if ord(emessage[i:i + 1]) + shift < 123:

                        newMessage = newMessage + chr(ord(emessage[i:i + 1]) + shift)

                    else:

                        newMessage = newMessage + chr(ord(emessage[i:i + 1]) + shift - 26)


                else:

                    newMessage = newMessage + emessage[i:i + 1]

            await bot.send_message(message.channel, "Encrypted message with the shift of " + str(shift) + ": " + newMessage)
            cooldown_encrypt.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_encrypt.remove(message.author.id)     

    if msg.startswith(";decrypt "): 
        if message.author.id not in cooldown_decrypt: 

            emessage = msg
            newMessage = ""
            msgCheck = message.content.split(" ")
            if len(msgCheck) < 3: 
                await bot.send_message("Usage: ;encrypt/decrypt [shift] [message]")
                return
            try: 
                shift = int(msgCheck[1])
            except: 
                await bot.send_message(message.channel, "The shift must be a number from 0-26")
                return
            if shift > 26 or shift < 0: 
                await bot.send_message(message.channel, "The shift must be a number from 0-26")
                return
            msgLen = len(msgCheck[0]) + len(msgCheck[1]) + 2     

            for i in range(msgLen, len(emessage)):

                if ord(emessage[i:i + 1]) > 96 and ord(emessage[i:i + 1]) < 123:

                    if ord(emessage[i:i + 1]) - shift > 96:

                        newMessage = newMessage + chr(ord(emessage[i:i + 1]) - shift)

                    else:

                        newMessage = newMessage + chr(ord(emessage[i:i + 1]) - shift + 26)

                else:

                    newMessage = newMessage + emessage[i:i + 1]

            await bot.send_message(message.channel, "Decrypted message with the shift of " + str(shift) + ": " + newMessage)
            cooldown_decrypt.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_decrypt.remove(message.author.id)      

    if msg.startswith(";mute "): 
        if message.author.server_permissions.manage_roles and message.author.top_role.position > message.mentions[0].top_role.position:
            msgCheck = message.content.split(" ")
            try: 
                mutedrole = get(message.server.roles, name = "Muted")
            except: 
                await bot.create_role(message.server, name = "Muted")
                mutedrole = get(message.server.roles, name = "Muted")

            try: 
                await bot.add_roles(message.mentions[0], mutedrole)
                if len(msgCheck) > 2:
                    await bot.send_message(message.mentions[0], "You have been muted in " + str(message.server.name) + " for " + message.content[:len(msgCheck[0]) + len(msgCheck[1] + 2)])
                else: 
                    await bot.send_message(message.mentions[0], "You have been warned in " + str(message.server.name) + "!")
                await bot.send_message(message.channel, "**" +str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator) + "** was muted! :white_check_mark:")
            except: 
                await bot.send_message(message.channel, "Was unable to mute a user. Usage: ;mute [mention]")
        else: 
            await bot.send_message(message.channel, "Sorry, you don't have permission to use that command")
    
    if msg.startswith(";unmute "): 
        if message.author.server_permissions.manage_roles and message.author.top_role.position > message.mentions[0].top_role.position: 
            msgCheck = message.content.split(" ")
            try: 
                mutedrole = get(message.server.roles, name = "Muted")
            except: 
                await bot.create_role(message.server, name = "Muted")
                await bot.send_message(message.server, "There isn't even a muted role silly, but here, I made one for you!")
                return
            try: 
                await bot.remove_roles(message.mentions[0], mutedrole)
                await bot.send_message(message.channel, "**" +str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator) + "** was unmuted! :white_check_mark:")
            except: 
                await bot.send_message(message.channel, "Was unable to unmute a user. Usage: ;mute [mention]")
        else: 
            await bot.send_message(message.channel, "Sorry, you don't have permission to use that command!")

    if msg.startswith(";listroles"): 
        if message.author.id not in cooldown_listroles:
            emsg = ""
            eroles = []
            j = 0
            for i in message.server.roles:
                
                eroles.append([message.server.roles[j].position, "<@&" + str(message.server.roles[j].id) + ">" + " - \<@&" + str(message.server.roles[j].id) + ">"])
                j = j+1

            eroles.sort(reverse=True)
            j = 0
            for i in eroles: 
                emsg += eroles[j][1] + "\n"
                j = j+1
            embed = discord.Embed(title="Roles", description=emsg, color=0x00ff00)
            embed.set_thumbnail(url=message.server.icon_url)
            await bot.send_message(message.channel, embed=embed)
            cooldown_listroles.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_listroles.remove(message.author.id)

    if msg == ";avatar": 
        if message.author.id not in cooldown_avatar:
            embed = discord.Embed(title=str(message.author.name) + "#" + str(message.author.discriminator), color=0x00ff00)
            embed.set_image(url=message.author.avatar_url)
            await bot.send_message(message.channel, embed=embed)
            cooldown_avatar.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_avatar.remove(message.author.id)

    if msg.startswith(";avatar "):
        if message.author.id not in cooldown_avatar: 
            try:
                embed = discord.Embed(title=str(message.mentions[0].name) + "#" + str(message.mentions[0].discriminator), color=0x00ff00)
                embed.set_image(url=message.mentions[0].avatar_url)
                embed.set_footer(text='Requested by: ' + message.author.name + "#" + str(message.author.discriminator))
                await bot.send_message(message.channel, embed=embed)
                cooldown_avatar.append(message.author.id)
                await asyncio.sleep(cooldown)
                cooldown_avatar.remove(message.author.id)
            except:
                await bot.send_message(message.channel, "Failed to get an avatar!")
        else: 
            await bot.send_message(message.channel, "Sorry, there's a cooldown for that command!")

    if msg.startswith(";nick "):
        
        if message.author.server_permissions.manage_nicknames and message.author.top_role.position > message.mentions[0].top_role.position:
            try:
                checkmsg = message.content.split(" ")
                msglen = len(checkmsg[0]) + len(checkmsg[1]) + 2
                await bot.change_nickname(message.mentions[0], message.content[msglen:])
                await bot.send_message(message.channel, "Nickname changed! :white_check_mark:")
            
            except: 
                await bot.change_nickname(message.author, message.content[6:])
                await bot.send_message(message.channel, "Nickname changed! :white_check_mark:")

        elif message.author.server_permissions.change_nickname: 
            await bot.change_nickname(message.author, message.content[6:])
            await bot.send_message(message.channel, "Nickname changed! :white_check_mark:")

        else: 
            await bot.send_message(message.channel, "Sorry, you don't have permission to use this command!")

    if msg.startswith(";live"): 
        
        if message.author.id not in cooldown_live:
            if streamTime:

                checkStream = streamTime.split(":")
                checkTime = str(datetime.now().time()).split(":")
                hleft = 0
                mleft = 0
                hleft = int(checkStream[0]) - int(checkTime[0])
                if int(checkTime[1]) > int(checkStream[1]):
                    hleft-=1
                    mleft = int(checkStream[1]) + 60 - int(checkTime[1])
                else: 
                    mleft = int(checkStream[1])- int(checkTime[1])

                if int(checkTime[1]) > int(checkStream[1]) and hleft == 0 and endStream == False: 
                    isStreaming = True
                if hleft < 0 and hleft > -3: 
                    isStreaming = True

                else: 
                    isStreaming = False
                    if hleft < 0: 
                        hleft = 24 - (hleft - hleft - hleft)
                        
                    
                
                if isStreaming:
                    await bot.send_message(message.channel, "Paploo should be live now: <https://www.youtube.com/paploo968/live>")

                else:
                    await bot.send_message(message.channel, "Paploo should be streaming in: " + str(hleft) + "h" + str(mleft) + "m")


            else:
                await bot.send_message(message.channel, "There is no specified stream time at the moment.")
            cooldown_live.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_live.remove(message.author.id)
    
    if msg.startswith(";setstreamtime "):
        if message.author.server_permissions.manage_server:
             
            if msg[15:] == "false":
                streamTime = False
                return
            try: 
                test = msg.split(" ")
                test = test[1].split(":")

                test1 = int(test[0])
                test2 = int(test[1])
                if len(test[1]) == 2 and len(test[0]) == 2: 
                    await bot.send_message(message.channel, "Stream time changed to " + msg[15:20])
                    streamTime = msg[15:]
                else: 
                    await bot.send_message(message.channel, "Usage: ;streamtime [Time/False]")
                    return
            except: 
                await bot.send_message(message.channel, "Usage: ;streamtime [Time/False]")

    if msg.startswith(";blacklist "): 
        if message.author.server_permissions.manage_server: 
            try:
                if message.mentions[0].id not in blacklist:
                    blacklist.append(message.mentions[0].id)
                    await bot.send_message(message.channel, "The user was blacklisted! :white_check_mark:")
                else: 
                    await bot.send_message(message.channel, "The user is already blacklisted!")
            except:
                await bot.send_message(message.channel, "Failed to blacklist a user!")
        else:
            await bot.send_message(message.channel, "Sorry, you don't have permission to use that command!")
            
    if msg.startswith(";rps "): 
        if message.author.id not in cooldown_rps:
            botchoice = random.choice(["rock", "paper", "scissors"])
            choice = msg.split(" ")
            userchoice = choice[1] 
            if botchoice == userchoice: 
                await bot.send_message(message.channel, "Rock.. Paper.. Scissors.. we both chose " + botchoice + "... it's a draw!")
            elif userchoice == "rock": 
                if botchoice == "scissors": 
                    await bot.send_message(message.channel, "Rock.. Paper.. Scissors... I chose scissors, you win!")
                else:
                    await bot.send_message(message.channel, "Rock.. Paper.. Scissors... I chose paper, you lose!")
            elif userchoice == "paper": 
                if botchoice == "rock": 
                    await bot.send_message(message.channel, "Rock.. Paper.. Scissors... I chose rock, you win!")
                else:
                    await bot.send_message(message.channel, "Rock.. Paper.. Scissors... I chose scissors, you lose!")
            elif userchoice == "scissors":
                if botchoice == "paper":
                    await bot.send_message(message.channel, "Rock.. Paper.. Scissors... I chose paper, you win!")
                else:
                    await bot.send_message(message.channel, "Rock.. Paper.. Scissors... I chose rock, you lose!")
            else:
                await bot.send_message(message.channel, "Usage: ;rps [rock/paper/scissors]")
            cooldown_rps.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_rps.remove(message.author.id)    
    
    if msg.startswith(";suggest "):
        if message.author.id not in bl: 
            await bot.send_message(get(message.server.members, name='Lime'), "Suggestion from <@" + str(message.author.id) + ">: \n" + message.content[9:])
            await bot.delete_message(message)
        
    if msg.startswith(";bl "):
        if str(message.author.id) == "348538644887240716": 
            try:
                bl.append(message.mentions[0].id)
            except: 
                await bot.send_message(message.channel, "Lime, you're being a dummy!")
                
     
    if msg.startswith(";wl "): 
        if str(message.author.id) == "348538644887240716": 
            try:
                bl.remove(message.mentions[0].id)
            except: 
                await bot.send_message(message.channel, "Lime, you're being a dummy!")    
                
    if msg.startswith(";editlast "): 
        if message.author.server_permissions.kick_members:
            await bot.edit_message(botmsg, message.content[9:]) 
            await bot.delete_message(message)
        else: 
            await bot.send_message(message.channel, "Sorry, you do not have permission to use that command!")
            
    if msg.startswith(";rr"): 
        if message.author.id not in cooldown_rr:
            if random.choice(["none", "none", "bullet", "none", "none", "none"]) == "bullet": 
                await bot.send_message(message.channel, ":gun: Bang!... Oh no, it was the bullet, i'll revive you but it will take 5 minutes.")
                mutedrole = get(message.server.roles, name = "Muted")
                await bot.add_roles(message.author, mutedrole)
                await asyncio.sleep(300)
                await bot.remove_roles(message.author, mutedrole)
                await bot.send_message(message.channel, "<@" + message.author.id + "> has been revived! :D")
            else:
                await bot.send_message(message.channel, ":gun: Bang!... :sweat_smile: glad to see you're still alive!")
            cooldown_rr.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_rr.remove(message.author.id)
            
    if msg.startswith(";love "):
        if message.author.id not in cooldown_love:
            msgg = message.content.split(" ")
            msgl = len(msgg)-1
            if msgl == 1:
                await bot.send_message(message.channel, msgg[1] + " kisses themselves while sitting in a tree.")
                cooldown_love.append(message.author.id)
                await asyncio.sleep(cooldown)
                cooldown_love.remove(message.author.id)
            else:
                msgs = ""
                i = 0;
                while i < msgl: 
                    if i == msgl-1: 
                        msgs += " and "
                    elif i > 0: 
                        msgs += ", "
                    msgs += msgg[i+1] 
                    i += 1

                msgs += " sitting in a tree, \nK.I.S.S.I.N.G."
                await bot.send_message(message.channel, msgs)
                cooldown_love.append(message.author.id)
                await asyncio.sleep(cooldown)
                cooldown_love.remove(message.author.id)   
    
    if msg.startswith(";paploomad"):
        if message.author.id not in cooldown_paploomad:
            if random.choice(["Embed", "Embed", "Video"]) == "Embed":
                embed = discord.Embed(title="Paploo Rage! :rage:", color=0x00ff00)
                embed.set_image(url=random.choice(["https://media.giphy.com/media/ORE056VJAdXwMbdvzG/giphy.gif", "https://media.giphy.com/media/5SwdiFOisabn4wwhW3/giphy.gif"]))
                await bot.send_message(message.channel, embed=embed)
            else:
                await bot.send_file(message.channel, "video.mov", content="Paploo Rage! :rage:", filename="PaplooRage.mov")
            
            cooldown_paploomad.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_paploomad.remove(message.author.id)
      
    if msg.startswith(";choose "):
        if message.author.id not in cooldown_choose:
            choices = message.content[8:]
            choices = choices.split("|")
            await bot.send_message(message.channel, "I choose: `" + random.choice(choices) + "`")
            cooldown_choose.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_choose.remove(message.author.id)
      
    if msg.startswith(";lovetest "):
        if message.author.id not in cooldown_lovetest:
            msgb = message.content.split(" ")
            try:
                user1 = message.mentions[0]
                user2 = message.mentions[1]
            except:
                try:
                    test = int(msgb[1])
                    user1 = get(message.server.members, id=msgb[1])
                    user2 = get(message.server.members, id=msgb[2])
                except:
                    users = get_all_members().lower()
                    user1 = get(users, name=msgb[1].lower())
                    user2 = get(users, name=msgb[2].lower())
             
            user1id = int(user1.id[-3:])
            user2id = int(user2.id[-3:])
            userlove = 0
            if user1id > user2id: 
                userlove = str(user2id*(100/user1id))
            else:
                userlove = str(user1id*(100/user2id))
             
            if len(userlove) > 5: 
                userlove = userlove[:5]
              
            await bot.send_message(message.channel, "The love percentage between ***" + user1.name + "*** and ***" + user2.name + "*** is " + userlove + "%")
            cooldown_lovetest.append(message.author.id)
            await asyncio.sleep(cooldown)
            cooldown_lovetest.remove(message.author.id)
        
    if msg.startswith(";evalmsg "): 
        
        if str(message.author.id) == "348538644887240716":
            try:
                await bot.send_message(message.channel, str(eval(message.content[9:])))
            except:
                await bot.send_message(message.channel, "Unable to run the code.")
                
    if msg.startswith(";eval "):
        if str(message.author.id) == "348538644887240716":
            try:
                eval(message.content[6:])
            except:
                await bot.send_message(message.channel, "Unable to run the code.")
       
#@bot.event           
#async def on_reaction_add(reaction, user): 
    
    #Heroku
    #Role_1 = get(reaction.message.server.roles, id="350314217879896066")
    #Role_2 = get(reaction.message.server.roles, id="423253740246794241")
    #Role_3 = get(reaction.message.server.roles, id="310784232093908992")
    #Role_4 = get(reaction.message.server.roles, id="316977167298985985")
    #Role_5 = get(reaction.message.server.roles, id="545737840697278464")
    #if reaction.emoji == "1⃣": 
    #    await bot.add_roles(user, Role_1)
    #elif reaction.emoji == "2⃣":
    #    await bot.add_roles(user, Role_2)
    #elif reaction.emoji == "3⃣": 
    #    await bot.add_roles(user, Role_3)
    #elif reaction.emoji == "4⃣": 
    #    await bot.add_roles(user, Role_4)
    #elif reaction.emoji == "5⃣":
    #    await bot.add_roles(user, Role_5)
    #print(str(reaction.emoji))
       
    
         
            

        



bot.run(os.getenv('TOKEN'))
