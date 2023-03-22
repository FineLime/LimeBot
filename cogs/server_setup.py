import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

class Server_Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_guild=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def logs_channel(self, ctx, channel: discord.TextChannel):

        await ctx.defer()
        async with self.bot.db.execute("SELECT * FROM controlpanel_guilds WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
            data = await cursor.fetchone()

        if data is None:
            async with self.bot.db.execute("INSERT INTO controlpanel_guilds (guild_id, logs_channel, access_token, refresh_token) VALUES (?, ?, ?, ?)", (ctx.guild.id, channel.id, None, None)) as cursor:
                await self.bot.db.commit()
        else:
            async with self.bot.db.execute("UPDATE controlpanel_guilds SET logs_channel = ? WHERE guild_id = ?", (channel.id, ctx.guild.id)) as cursor:
                await self.bot.db.commit()
        

    


def setup(bot):
    bot.add_cog(Server_Setup(bot))