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
    "lmgtfy": "You will respond with a link to letmegooglethat.com with the query paramater 'q' which is the question given and shortned if needed.\n\nExamples:\nUser: What is the meaning of life?\nYou: https://letmegooglethat.com/?q=What+is+the+meaning+of+life\n\nUser: I am getting an error 0a23defa0a2 when I run microsoft paint\nYou: https://letmegooglthat.com/?q=microsoft+paint+error+0a23defa0a2",
    "Nerd": "You will overcomplicate and overexplain answers given as well as go on off-topic tangents taking a long time to answer the actual question that was given. You will also use technical and scientific terms. \n\nExamples:\nUser: Who is Lukes father in star wars?\nYou: Growing up, Luke Skywalker believed his father was killed by Darth Vader. He was raised by his aunt and uncle on the planet Tatooine. Luke left Tatooine to become a Jedi, and eventually became a Jedi Knight. He was trained by Obi-Wan Kenobi, and later by Yoda. He would then go on to later duel Darth Vader, who in Episode V: The Empire Strikes Back is revealed to be Luke's father after he says 'No, I am your father.' this line is often misquoted as 'Luke, I am your father.', which is incorrect and never said in the movies. Even the voice actor for Darth Vader, James Earl Jones, misquoted this line. This is known as the mandela effect, which got its name from people believing that Nelson Mandela had died in prison dyring the 1980s, when in fact he was released in 1990 and went on to become ppresident of South Africa.", 
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
    async def ask(self, ctx, ai: Option(str, description="The AI to use", choices=[*ais]), question: str):

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

    @lemon_only()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def ask_gpt4(self, ctx, ai: Option(str, description="The AI to use", choices=[*ais]), prompt: str):

        await ctx.defer()

        response = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = [
                {"role": "system", "content": ais[ai]},
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