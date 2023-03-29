import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

class Server_Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(Server_Setup(bot))