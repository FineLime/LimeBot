import discord
from discord.ext import commands

def is_dev():
    def predicate(ctx):
        if str(ctx.author.id) in ["348538644887240716"]:
            return True
        return False
    return commands.check(predicate)

class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @is_dev()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def server_count(self, ctx):
        await ctx.respond(f"Server Count: {len(self.bot.guilds)}")

    @is_dev()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def server_list(self, ctx):
        await ctx.respond(f"Server List: {', '.join([guild.name for guild in self.bot.guilds])}")

    @is_dev()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def eval(self, ctx, *, code):
        code = code.strip("` ")
        try:
            exec(code)
        except Exception as e:
            await ctx.respond(f"```py\n{e}```", ephemeral=True)
            return
        
        await ctx.respond("Executed successfully", ephemeral=True)

    @is_dev()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def aeval(self, ctx, *, code):
        code = code.strip("` ")
        try:
            await exec(code)
        except Exception as e:
            await ctx.respond(f"```py\n{e}```", ephemeral=True)
            return
        
        await ctx.respond("Executed successfully", ephemeral=True)

    @is_dev()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def return_eval(self, ctx, *, code):
        code = code.strip("` ")
        try:
            result = eval(code)
        except Exception as e:
            await ctx.respond(f"```py\n{e}```", ephemeral=True)
            return
        
        await ctx.respond(f"{result}", ephemeral=True)

    @is_dev()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def return_aeval(self, ctx, *, code):
        code = code.strip("` ")
        try:
            result = await eval(code)
        except Exception as e:
            await ctx.respond(f"```py\n{e}```", ephemeral=True)
            return
        
        await ctx.respond(f"{result}", ephemeral=True)
        

def setup(bot):
    bot.add_cog(Dev(bot))