import discord 
from discord.ext import commands
import requests
from datetime import datetime
import random
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.cache = { 
            "launch": { 
                "cache": None,
                "time": None
            }
        }

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def avatar(self, ctx, member: discord.Member = None):
        
        user = member or ctx.author
        embed = discord.Embed(title=f"{user.name}'s avatar", color=discord.Color.blurple())
        embed.set_image(url=user.display_avatar.url)
        if user != ctx.author:
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

        await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def hex(self, ctx, hex: str): 
        if hex.startswith("#"):
            hex = hex[1:]
        if len(hex) != 6:
            await ctx.respond("Invalid hex code!")
            return
        try:
            int(hex, 16)
        except ValueError:
            await ctx.respond("Invalid hex code!")
            return
        embed = discord.Embed(title=f"Hex: #{hex}", color=int(hex, 16))
        embed.set_image(url=f"https://dummyimage.com/600x400/{hex}/000000&text=%20")
        await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def launch(self, ctx): 

        # check if the cache is valid and is not older than 5 minutes
        if self.bot.cache["launch"]["cache"] and self.bot.cache["launch"]["time"] > datetime.now().timestamp() - 300: 

            upcoming = self.bot.cache["launch"]["cache"]


            if upcoming == "No upcoming launches":
                await ctx.respond("No upcoming launches")
                return
            
        else:

            upcoming = requests.get("https://ll.thespacedevs.com/2.0.0/launch/upcoming/?status=1") 
            upcoming = upcoming.json()
            
            upcoming = upcoming["results"][0] 
            upcoming = requests.get(f"https://ll.thespacedevs.com/2.0.0/launch/{upcoming['id']}/")
            upcoming = upcoming.json()

            self.bot.cache["launch"]["cache"] = upcoming
            self.bot.cache["launch"]["time"] = datetime.now().timestamp()


        mission_name = upcoming["mission"]["name"]
        misson_description = upcoming["mission"]["description"]
        status = upcoming["status"]["name"]
        launch_date = upcoming["net"]
        launch_date = datetime.strptime(launch_date, "%Y-%m-%dT%H:%M:%SZ")
        launch_date = str(launch_date.timestamp()).split(".")[0]

        video = upcoming["vidURLs"][0]["url"] if upcoming["vidURLs"] else None 

        embed_description = f"{misson_description}\n\nStatus: {status}\nLift off <t:{launch_date}:R>"
        if video:
            embed_description += f"\n\n[Watch the launch]({video})"

        embed = discord.Embed(title=f'{mission_name} on <t:{launch_date}:F>', description=embed_description, color=discord.Color.blurple())
        
        await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def rr(self, ctx): 

        message = await ctx.respond("Opening the chamber.")
        await asyncio.sleep(0.5)
        bullet = random.randint(1, 6)
        await message.edit(content=f"Loading the bullet..")
        await asyncio.sleep(0.5)
        chamber = random.randint(1, 6)
        await message.edit(content=f"Spinning the chamber...")
        await asyncio.sleep(0.5)
        msg = "<a:PepeGun:533822706144116752> FIRE...! "

        if bullet == chamber:
            msg += "**\*\*BANG\*\***, you're dead.\n"
            timeout_time = random.randint(1, 15)
            
            if timeout_time < 3:
                msg += f"Don't worry, I have quick revive, I'll have you back up in {timeout_time} minutes."
            elif timeout_time < 5:
                msg += f"Hang on, let me just {random.choice(['use in plain sight', 'get this nuke', 'throw a monkey bomb', 'throw a lil arnie'])} and I'll be back in {timeout_time} minutes."
            elif timeout_time < 10:
                msg += f"Shoot, I need to kill these zombies first before I can revive you, I'll be back in {timeout_time} minutes."
            elif timeout_time < 15:
                msg += f"...Why are you across the map? I'll get to you in {timeout_time} minutes."
            else: 
                msg += f"Honestly, you're kind of a liability, you can join back in next round, I'm not reviving you."

            await message.edit(content=msg)
            await ctx.author.timeout(timeout_time * 60, reason="You died in a game of Russian Roulette.")

        else:
            msg += f"**CLICK**, you're alive, {random.choice(['luckily', 'unfortunately', 'for now...', 'unless we just live in a simulation, then are we actually alive to begin with?', 'UwU', 'thank the lord', 'now do it again'])}."
        

    




        


def setup(bot):
    bot.add_cog(Fun(bot))