import discord 
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime
import os 
import asyncpg

class Birthday(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.birthday_loop.start()

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

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def birthday(self, ctx, *, day: str, month: str):

        month = month.lower()

        match month:
            
            case "january" | "jan" | "1": 
                month = "01"
            case "february" | "feb" | "2":
                month = "02"
            case "march" | "mar" | "3":
                month = "03"
            case "april" | "apr" | "4":
                month = "04"
            case "may" | "5":
                month = "05"
            case "june" | "jun" | "6":
                month = "06"
            case "july" | "jul" | "7":
                month = "07"
            case "august" | "aug" | "8":
                month = "08"
            case "september" | "sep" | "9":
                month = "09"
            case "october" | "oct" | "10":
                month = "10"
            case "november" | "nov" | "11":
                month = "11"
            case "december" | "dec" | "12":
                month = "12"
            case _:
                return await ctx.respond("Invalid month.")
            
        birthday = f"{day}-{month}"

        data = await self.bot.db.fetch("SELECT member_id, guild_id, birthday FROM controlpanel_birthday WHERE member_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if data:
            await self.bot.db.execute("UPDATE controlpanel_birthday SET birthday = $1 WHERE member_id = $2 AND guild_id = $3", birthday, ctx.author.id, ctx.guild.id)
            await ctx.respond(f"Updated your birthday to {birthday}.")
            return

        await self.bot.db.execute("INSERT INTO controlpanel_birthday (member_id, guild_id, birthday) VALUES ($1, $2, $3)", ctx.author.id, ctx.guild.id, birthday)
        await ctx.respond(f"Set your birthday to {birthday}.")

    

    @tasks.loop(hours=12)
    async def birthday_loop(self):

        database = os.environ.get("DATABASE_URL")
        db = await asyncpg.create_pool(database, ssl="require")

        birthdays = await db.fetch("SELECT member_id, guild_id, birthday, celebrated FROM controlpanel_birthday WHERE birthday = $1", datetime.now().strftime("%d-%m"))
        
        for member_id, guild_id, birthday, celebrated in birthdays:

            if datetime.now().strftime("%Y") == celebrated:
                return

            guild = self.bot.get_guild(guild_id)
            member = guild.get_member(member_id)
            channel = guild.get_channel(await db.fetchval("SELECT birthday_channel FROM controlpanel_guild WHERE guild_id = $1", guild_id))
            message = await db.fetchval("SELECT birthday_message FROM controlpanel_guild WHERE guild_id = $1", guild_id)
            role = guild.get_role(await db.fetchval("SELECT birthday_role FROM controlpanel_guild WHERE guild_id = $1", guild_id))

            await db.execute("UPDATE controlpanel_birthday SET celebrated = $1 WHERE member_id = $2 AND guild_id = $3", datetime.now().strftime("%Y"), member_id, guild_id)

            if not channel:
                return

            if not message:
                return

            await channel.send(message.format(member=member.mention))

    
def setup(bot):
    bot.add_cog(Birthday(bot))