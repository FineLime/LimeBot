import discord 
from discord.ext import commands
import json 
import requests
import random 
from xml.etree import ElementTree
import os
from datetime import datetime

class NSFW(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.banned_tags = []
        self.e621_key = os.environ.get('E621_KEY')
        self.nsfw_cache = {
            "rule34": { 
            }, 
            "e621": {
            }
        }

    # @commands.is_nsfw()
    # @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    # async def rule34(self, ctx, tags: str): 

    #     tags = tags.replace(" ", "+")
    #     tags = tags.replace(",", "+")

    #     if "=" in tags:
    #         await ctx.respond("Invalid tags.", ephemeral=True)
    #         return
        
    #     if self.nsfw_cache["rule34"].get(tags): 

    #         # check if cache is less than 30 minutes old
    #         if (datetime.now() - self.nsfw_cache["rule34"][tags]["time"]).total_seconds() < 1800:
    #             print("cache")
    #             post = random.choice(self.nsfw_cache["rule34"][tags]["posts"])
    #             await ctx.respond(post.attrib["file_url"])
    #             return
            
    #     print("no cache")

    #     if tags in self.banned_tags:
    #         await ctx.respond("These tags contain banned content.", ephemeral=True)
    #         return
        
    #     await ctx.defer()
        
    #     url = f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=50&tags={tags}"
    #     request = requests.get(url)
        
    #     print(request.status_code)

    #     root = ElementTree.fromstring(request.content)

    #     if int(root.attrib["count"]) == 0:
    #         await ctx.followup.send("No results found.", ephemeral=True)
    #         return  
        
    #     post = random.choice(root)

    #     # check if post contains banned tags
    #     for banned_tag in self.banned_tags:
    #         if banned_tag in post.attrib["tags"]:
    #             await ctx.followup.send("These tags contain banned content.", ephemeral=True)
    #             return
            
    #     self.nsfw_cache["rule34"][tags] = {
    #         "time": datetime.now(),
    #         "posts": root
    #     }
            
    #     await ctx.followup.send(post.attrib["file_url"])

    # @commands.is_nsfw()
    # @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    # async def e621(self, ctx, tags: str):

    #     if "=" in tags:
    #         await ctx.respond("Invalid tags.", ephemeral=True)
    #         return
        
    #     tags = tags.replace(" ", "+")
    #     tags = tags.replace(",", "+")
        
    #     if self.nsfw_cache["e621"].get(tags):
                
    #             print("is in cache")
    
    #             # check if cache is less than 30 minutes old
    #             if (datetime.now() - self.nsfw_cache["e621"][tags]["time"]).total_seconds() < 1800:
    #                 post = random.choice(self.nsfw_cache["e621"][tags]["posts"])
    #                 await ctx.respond(post["file"]["url"])
    #                 return
                
        
    #     if tags in self.banned_tags:
    #         await ctx.respond("These tags contain banned content.", ephemeral=True)
    #         return

    #     await ctx.defer()
    #     headers = {"User-Agent": "LimeBot by FineLime"}
    #     params = f"tags={tags}&limit=50"
    #     auth = ("FineLime", self.e621_key)
    #     url = f"https://e621.net/posts.json?{params}"


    #     request = requests.get(url, headers=headers, auth=auth)
    #     posts = request.json()['posts']
        
    #     if len(posts) == 0:
    #         await ctx.followup.send("No results found.", ephemeral=True)
    #         return
        
    #     post = random.choice(posts)

    #     # check if post contains banned tags
    #     for banned_tag in self.banned_tags:
    #         if banned_tag in post["tags"]["general"]:
    #             await ctx.followup.send("These tags contain banned content.", ephemeral=True)
    #             return
            
    #     self.nsfw_cache["e621"][tags] = {
    #         "time": datetime.now(),
    #         "posts": posts
    #     }
            
    #     await ctx.followup.send(post["file"]["url"])

    # @e621.error
    # async def e621_error(self, ctx, error):
    #     if isinstance(error, commands.CheckFailure):
    #         await ctx.respond("This command can only be used in NSFW channels.", ephemeral=True)
    #     else: 
    #         print(error)
    #         await ctx.respond("An error occured.", ephemeral=True)

    # @rule34.error
    # async def rule34_error(self, ctx, error):
    #     if isinstance(error, commands.CheckFailure):
    #         await ctx.respond("This command can only be used in NSFW channels.", ephemeral=True)

    #     else: 
    #         print(error)
    #         await ctx.respond("An error occured.", ephemeral=True)
            
        

def setup(bot):
    bot.add_cog(NSFW(bot))