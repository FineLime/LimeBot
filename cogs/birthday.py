import discord 
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
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
    async def birthday(self, ctx, *, month: str, day: int):

        month = month.lower()

        match month:
            
            case "january" | "jan" | "1" | "01":
                month = "01"
            case "february" | "feb" | "2" | "02":
                month = "02"
            case "march" | "mar" | "3" | "03":
                month = "03"
            case "april" | "apr" | "4" | "04":
                month = "04"
            case "may" | "5" | "05":
                month = "05"
            case "june" | "jun" | "6" | "06":
                month = "06"
            case "july" | "jul" | "7" | "07":
                month = "07"
            case "august" | "aug" | "8" | "08":
                month = "08"
            case "september" | "sep" | "9" | "09":
                month = "09"
            case "october" | "oct" | "10":
                month = "10"
            case "november" | "nov" | "11":
                month = "11"
            case "december" | "dec" | "12":
                month = "12"
            case _:
                return await ctx.respond("Invalid month.", ephemeral=True)
            
        birthday = f"{month}-{day}"

        data = await self.bot.db.fetch("SELECT member_id, guild_id, birthday FROM controlpanel_birthday WHERE member_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if data:
            await self.bot.db.execute("UPDATE controlpanel_birthday SET birthday = $1 WHERE member_id = $2 AND guild_id = $3", birthday, ctx.author.id, ctx.guild.id)
            await ctx.respond(f"Updated your birthday to {birthday}.")
            return

        await self.bot.db.execute("INSERT INTO controlpanel_birthday (member_id, guild_id, birthday) VALUES ($1, $2, $3)", ctx.author.id, ctx.guild.id, birthday)
        await ctx.respond(f"Set your birthday to {birthday}.")

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def birthday_remove(self, ctx):

        data = await self.bot.db.fetch("SELECT member_id, guild_id, birthday FROM controlpanel_birthday WHERE member_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if not data:
            return await ctx.respond("You don't have a birthday set.", ephemeral=True)

        await self.bot.db.execute("DELETE FROM controlpanel_birthday WHERE member_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)
        await ctx.respond("Removed your birthday.")

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def birthday_info(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        data = await self.bot.db.fetch("SELECT member_id, guild_id, birthday FROM controlpanel_birthday WHERE member_id = $1 AND guild_id = $2", member.id, ctx.guild.id)

        if not data:
            return await ctx.respond("That member doesn't have a birthday set.", ephemeral=True)

        birthday = data[0]["birthday"]

        await ctx.respond(f"{member.mention}'s birthday is {birthday}.")

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def birthday_next(self, ctx): 

        data = await self.bot.db.fetch("SELECT member_id, guild_id, birthday FROM controlpanel_birthday WHERE guild_id = $1", ctx.guild.id)

        if not data:
            return await ctx.respond("No birthdays set for this server.", ephemeral=True)

        birthdays = []

        for birthday in data:
            date = birthday["birthday"]
            print(date)
            if datetime.now().strftime("%m-%d") <= date:
                print("append for next year")
                birthdays.append({ 
                    'member_id': birthday["member_id"],
                    'birthday': f"{int(datetime.now().strftime('%Y')) + 1}-{date}"
                })
            else:
                print("append for this year")
                birthdays.append({
                    'member_id': birthday["member_id"],
                    'birthday': f"{datetime.now().strftime('%Y')}-{date}"
                })

        birthdays = sorted(birthdays, key=lambda x: x['birthday'])

        embed = discord.Embed(title="Next Birthdays", color=discord.Color.blurple())

        for num, birthday in enumerate(birthdays):
            member = ctx.guild.get_member(birthday["member_id"])
            embed.add_field(name=f"{num + 1}. {member}", value=birthday["birthday"])

            if num == 10:
                break

        await ctx.respond(embed=embed)


        

    

    @tasks.loop(minutes=1)
    async def birthday_loop(self):

        db = self.bot.db

        birthdays = await db.fetch("SELECT member_id, guild_id, birthday, celebrated FROM controlpanel_birthday WHERE birthday = $1", datetime.now().strftime("%m-%d"))
        
        for birthday in birthdays:

            guild_id = birthday["guild_id"]
            member_id = birthday["member_id"]
            celebrated = birthday["celebrated"]

            if datetime.now().strftime("%Y") == celebrated:
                return
            
            

            guild = self.bot.get_guild(guild_id)
            member = guild.get_member(member_id)
            channel = guild.get_channel(await db.fetchval("SELECT birthday_channel FROM controlpanel_guild WHERE guild_id = $1", guild_id))
            message = await db.fetchval("SELECT birthday_message FROM controlpanel_guild WHERE guild_id = $1", guild_id)
            message = message.replace("{$user}", member.mention)

            await db.execute("UPDATE controlpanel_birthday SET celebrated = $1 WHERE member_id = $2 AND guild_id = $3", datetime.now().strftime("%Y"), member_id, guild_id)

            if not channel:
                return

            if not message:
                return
            
            embed = discord.Embed(title=f"It's {member.name}'{'s' if member.name[-1] != 's' else ''} birthday!", description=message, color=discord.Color.blurple())

            await channel.send(embed=embed)

    @birthday_loop.before_loop
    async def before_birthday_loop(self):
        await self.bot.wait_until_ready()


    
def setup(bot):
    bot.add_cog(Birthday(bot))