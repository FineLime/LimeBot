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


        result = await self.bot.db.fetch("SELECT * FROM controlpanel_customcommand WHERE guild_id = $1 and name = $2", ctx.guild.id, command)

        if result:
            await ctx.respond("This command already exists")
            return
        
        await self.bot.db.execute("INSERT INTO controlpanel_customcommand (guild_id, name, response, permission) VALUES ($1, $2, $3, $4)", ctx.guild.id, command, response, 'everyone')

        await ctx.respond(f"Added command {command} successfully.")

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    @commands.has_permissions(manage_guild=True)
    async def removecommand(self, ctx, command):
        
        result = await self.bot.db.fetch("SELECT * FROM controlpanel_customcommand WHERE guild_id = $1 and name = $2", ctx.guild.id, command)

        if not result:
            await ctx.respond("This command does not exist")
            return
        
        await self.bot.db.execute("DELETE FROM controlpanel_customcommand WHERE guild_id = $1 and name = $2", ctx.guild.id, command)

        await ctx.respond(f"Removed command {command} successfully.")

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def customs_list(self, ctx): 

        cmds = await self.bot.db.fetch("SELECT name FROM controlpanel_customcommand WHERE guild_id = $1", ctx.guild.id)

        description = "".join([f"{cmd['name']}\n" for cmd in cmds]) if cmds else "No custom commands"

        embed = discord.Embed(title="Custom Commands", description=description, color=discord.Color.blurple())

        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        result = await self.bot.db.fetchrow("SELECT * FROM controlpanel_customcommand WHERE guild_id = $1 and name = $2", message.guild.id, message.content.split(" ")[0])

        if result:
            response = result[2]
            await message.channel.send(format_custom_command_response(message, response))
    

        

def setup(bot):
    bot.add_cog(CustomCommands(bot))