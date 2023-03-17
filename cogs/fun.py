import discord 
from discord.ext import commands
import requests
from datetime import datetime

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

            upcoming = requests.get("https://ll.thespacedevs.com/2.0.0/launch/upcoming/") 
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

    




        


def setup(bot):
    bot.add_cog(Fun(bot))