import discord
from discord.ext import commands
import re
from stuff.format_custom import format_custom_command_response

class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    @commands.has_permissions(manage_guild=True)
    async def addcommand(self, ctx, command, response: str): 

        async with self.bot.db.execute("SELECT * FROM controlpanel_customcommand WHERE guild_id = ? and name = ?", (ctx.guild.id, command)) as cursor:
            result = await cursor.fetchone()

        if result:
            await ctx.respond("This command already exists")
            return
        
        async with self.bot.db.execute("INSERT INTO controlpanel_customcommand (guild_id, name, response, permission) VALUES (?, ?, ?, ?)", (ctx.guild.id, command, response, 'everyone')) as cursor:
            await self.bot.db.commit()

        await ctx.respond(f"Added command {command} successfully.")

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    @commands.has_permissions(manage_guild=True)
    async def removecommand(self, ctx, command):
        
        async with self.bot.db.execute("SELECT * FROM controlpanel_customcommand WHERE guild_id = ? and name = ?", (ctx.guild.id, command)) as cursor:
            result = await cursor.fetchone()

        if not result:
            await ctx.respond("This command does not exist")
            return
        
        async with self.bot.db.execute("DELETE FROM controlpanel_customcommand WHERE guild_id = ? and name = ?", (ctx.guild.id, command)) as cursor:
            await self.bot.db.commit()

        await ctx.respond(f"Removed command {command} successfully.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        async with self.bot.db.execute("SELECT * FROM controlpanel_customcommand WHERE guild_id = ? and name = ?", (message.guild.id, message.content.split(" ")[0])) as cursor:
            result = await cursor.fetchone()

        if result:
            response = result[2]
            await message.channel.send(format_custom_command_response(message, response))
    

        

def setup(bot):
    bot.add_cog(CustomCommands(bot))