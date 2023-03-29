import discord 
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime

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

    @tasks.loop(hours=24)
    async def birthday_loop(self):

        birthdays = await self.bot.db.fetch("SELECT member_id, guild_id, birthday FROM controlpanel_birthday WHERE birthday = $1", datetime.now().strftime("%m-%d"))
        
        for member_id, guild_id, birthday in birthdays:
            
            guild = self.bot.get_guild(guild_id)
            member = guild.get_member(member_id)
            channel = guild.get_channel(await self.bot.db.fetchval("SELECT birthday_channel FROM controlpanel_guild WHERE guild_id = $1", guild_id))
            message = await self.bot.db.fetchval("SELECT birthday_message FROM controlpanel_guild WHERE guild_id = $1", guild_id)
            role = guild.get_role(await self.bot.db.fetchval("SELECT birthday_role FROM controlpanel_guild WHERE guild_id = $1", guild_id))

            if not channel:
                return

            if not message:
                return

            await channel.send(message.format(member=member.mention))

    
def setup(bot):
    bot.add_cog(Birthday(bot))