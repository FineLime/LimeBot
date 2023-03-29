import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

async def check_birthdays

class Birthday(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_guild=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def birthday_channel(self, ctx, channel: discord.TextChannel):
        await self.bot.db.execute("UPDATE controlpanel_guild SET birthday_channel = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
        await ctx.respond(f"Set the birthday channel to {channel.mention}.")

    @has_permissions(manage_guild=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def birthday_message(self, ctx, *, message):
        await self.bot.db.execute("UPDATE controlpanel_guild SET birthday_message = $1 WHERE guild_id = $2", message, ctx.guild.id)
        await ctx.respond(f"Set the birthday message to {message}.")

    @has_permissions(manage_guild=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def birthday_role(self, ctx, role: discord.Role):
        await self.bot.db.execute("UPDATE controlpanel_guild SET birthday_role = $1 WHERE guild_id = $2", role.id, ctx.guild.id)
        await ctx.respond(f"Set the birthday role to {role.mention}.")

    @has_permissions(manage_guild=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def birthday_remove(self, ctx):
        await self.bot.db.execute("UPDATE controlpanel_guild SET birthday_message = $1 WHERE guild_id = $2", None, ctx.guild.id)
        await ctx.respond("Removed the birthday settings.")

    
def setup(bot):
    bot.add_cog(Birthday(bot))