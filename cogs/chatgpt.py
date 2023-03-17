import discord
from discord.ext import commands
import openai 
import io
import aiohttp
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], name="ask-gpt")
    async def askgpt(self, ctx, question: str): 

        await ctx.defer()
        
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [ 
                {"role": "system", "content": "You are a helpful assistant which will answer questions given."},
                {"role": "user", "content": question}
            ]
        ) 

        answer = response["choices"][0]["message"]["content"]
        title = question if len(question) < 200 else question[:200] + "..."
        embed = discord.Embed(title=title, description=answer, color=discord.Color.blurple())
        
        await ctx.followup.send(embed=embed)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], name="ask-karen")
    async def askkaren(self, ctx, question: str):
            
            await ctx.defer()
            
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [ 
                    {"role": "system", "content": "You will rudely, aggressively, and sarcastically answer questions given."},
                    {"role": "user", "content": question}
                ]
            ) 
    
            answer = response["choices"][0]["message"]["content"]
            title = question if len(question) < 200 else question[:200] + "..."
            embed = discord.Embed(title=title, description=answer, color=discord.Color.blurple())
            
            await ctx.followup.send(embed=embed)#

    # @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], name="dalle")
    # async def dalle(self, ctx, prompt: str): 
         
    #     await ctx.defer()
        
    #     images = openai.Image.create(
    #         prompt=prompt,
    #         n=4,
    #         size="512x512",
    #     )

    #     files = []

    #     async with aiohttp.ClientSession() as session:
    #         for image in images["data"]:
    #             async with session.get(image["url"]) as resp:
    #                 if resp.status == 200:
    #                     files.append(discord.File(io.BytesIO(await resp.read()), filename='image.png'))      

    #     await ctx.followup.send(f"**{prompt}**", files=files)
        

def setup(bot):
    bot.add_cog(ChatGPT(bot))