import discord
from discord.ext import commands
import openai 
import io
import aiohttp
import os
from stuff.patreon_only import grapefruit_only, lemon_only
from discord import Option

openai.api_key = os.environ.get('OPENAI_API_KEY')

ais = { 
    "Karen": "You will rudely, aggressively, and sarcastically answer questions given.",
    "Troll": "You will incorrectly answer questions given.",
    "lmgtfy": "You will respond with a link to letmegooglethat.com with the query paramater 'q' which is the question given and shortned if needed.\n\nExamples:\nUser: What is the meaning of life?\nBot: https://letmegooglethat.com/?q=What+is+the+meaning+of+life\n\nUser: I am getting an error 0a23defa0a2 when I run microsoft paint\nBot: https://letmegooglthat.com/?q=microsoft+paint+error+0a23defa0a2",
}

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

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], name="ask")
    async def ask(self, ctx, question: str, ai: Option(str, description="The AI to use", choices=[*ais])):

        await ctx.defer()
        
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [ 
                {"role": "system", "content": ais[ai]},
                {"role": "user", "content": question}
            ]
        ) 

        answer = response["choices"][0]["message"]["content"]
        title = question if len(question) < 200 else question[:200] + "..."
        embed = discord.Embed(title=title, description=answer, color=discord.Color.blurple())
        
        await ctx.followup.send(embed=embed)

    @lemon_only()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], name="gpt-4")
    async def gpt4(self, ctx, prompt: str):
        
        await ctx.defer()

        response = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = [
                {"role": "system", "content": "You are a helpful assistant which will answer questions given."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response["choices"][0]["message"]["content"]
        title = prompt if len(prompt) < 200 else prompt[:200] + "..."
        embed = discord.Embed(title=title, description=answer, color=discord.Color.blurple())

        await ctx.followup.send(embed=embed)

    @gpt4.error
    async def gpt4_error(self, ctx, error):
        if error.__class__.__name__ == "CheckFailure":
            await ctx.respond("This command is only available to Lemon Patrons.\nYou can become a patron at https://www.patreon.com/FineLime\n\nIf you are a patron, please make sure you have linked your Discord account to your Patreon account and have waited at least 5 minutes for the cache to update.", ephemeral=True)



def setup(bot):
    bot.add_cog(ChatGPT(bot))