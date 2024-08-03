import discord
from discord.ext import commands
import re

class FixXLinks(commands.Cog): 

    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author.bot:
            return
          
        x_links = re.findall(r"https:\/\/x.com\/([a-zA-Z0-9_]+)\/status\/([0-9]+)", message.content) 

        if x_links:

            new_message = "I fixed those X links for you!"

            for x_link in x_links:
                user = x_link[0]
                status = x_link[1]
                fixed_link = f"https://fixvx.com/{user}/status/{status}"
                new_message += f"\n{fixed_link}"

        
            await message.channel.send(f"Hey, I fixed those X links for you! {new_message}")


def setup(bot):
    bot.add_cog(FixXLinks(bot))
