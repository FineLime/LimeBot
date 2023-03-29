import discord 
from discord.ext import commands

def is_lime():
    def predicate(ctx):
        return ctx.author.id == 348538644887240716
    return commands.check(predicate)

class Debug(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @is_lime()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def leave_guilds(self, ctx):
        for guild in self.bot.guilds:
            if guild.id == 234119683538812928 or guild.id == 1065746636275453972:
                continue
        await ctx.respond("Left all guilds.")

    @is_lime()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def eval(self, ctx, *, code):
        try:
            exec(code)
        except Exception as e:
            await ctx.respond(f"```{e}```")
            return
        await ctx.respond("Executed.")


def setup(bot):
    bot.add_cog(Debug(bot))