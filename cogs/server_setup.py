import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

class Server_Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_roles=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def autorole_add(self, ctx, role: discord.Role):

        data = await self.bot.db.fetch("SELECT role_id FROM controlpanel_autorole WHERE guild_id = $1", ctx.guild.id)

        if role.id in data:
            return await ctx.respond(f"{role.mention} is already in the autorole list.")

        await self.bot.db.execute("INSERT INTO controlpanel_autorole (guild_id, role_id) VALUES ($1, $2)", ctx.guild.id, role.id)
        await ctx.respond(f"Added {role.mention} to the autorole list.")

    @has_permissions(manage_roles=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def autorole_remove(self, ctx, role: discord.Role):
        
        data = await self.bot.db.fetch("SELECT role_id FROM controlpanel_autorole WHERE guild_id = $1", ctx.guild.id)

        if role.id not in data:
            return await ctx.respond(f"{role.mention} is not in the autorole list.")
        
        await self.bot.db.execute("DELETE FROM controlpanel_autorole WHERE guild_id = $1 AND role_id = $2", ctx.guild.id, role.id)
        await ctx.respond(f"Removed {role.mention} from the autorole list.")

    @has_permissions(manage_roles=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def autorole_list(self, ctx):

        data = await self.bot.db.fetch("SELECT role_id FROM controlpanel_autorole WHERE guild_id = $1", ctx.guild.id)

        if not data:
            return await ctx.respond("There are no autoroles.")

        roles = [ctx.guild.get_role(x[0]) for x in data]

        embed = discord.Embed(title="Autoroles", description="\n".join([x.mention for x in roles]))
        await ctx.respond(embed=embed)

    @has_permissions(manage_guild=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def welcome_channel(self, ctx, channel: discord.TextChannel):

        await self.bot.db.execute("UPDATE controlpanel_guild SET welcome_channel = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
        await ctx.respond(f"Set the welcome channel to {channel.mention}.")

    @has_permissions(manage_guild=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def welcome_message(self, ctx, *, message):
            
        await self.bot.db.execute("UPDATE controlpanel_guild SET welcome_message = $1 WHERE guild_id = $2", message, ctx.guild.id)
        await ctx.respond(f"Set the welcome message to {message}.") 

    @has_permissions(manage_guild=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def welcome_remove(self, ctx):

        await self.bot.db.execute("UPDATE controlpanel_guild SET welcome_message = NULL WHERE guild_id = $1", ctx.guild.id)
        await ctx.respond(f"Removed the welcome message.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
            
        welcome_data = await self.bot.db.fetchrow("SELECT welcome_channel, welcome_message FROM controlpanel_guild WHERE guild_id = $1", member.guild.id)
        autorole_data = await self.bot.db.fetch("SELECT role_id FROM controlpanel_autorole WHERE guild_id = $1", member.guild.id)

        if welcome_data['welcome_channel'] != None and welcome_data['welcome_message'] != None:
            channel = member.guild.get_channel(welcome_data['welcome_channel'])
            await channel.send(welcome_data['welcome_message'].replace("{user}", str(member.mention)).replace("{server}", str(member.guild.name)).replace("{member_count}", str(member.guild.member_count)))  

        if autorole_data:
            roles = [member.guild.get_role(x[0]) for x in autorole_data]
            await member.add_roles(*roles)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        await self.bot.db.execute("INSERT INTO controlpanel_guild (guild_id, access_token, refresh_token, welcome_channel, welcome_message, welcome_enabled, birthday_channel, birthday_message, logs_channel, logs_enabled, membercount_channel) VALUES ($1, NULL, NULL, NULL, NULL, False, NULL, NULL, NULL, False, NULL)", guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
            
        await self.bot.db.execute("DELETE FROM controlpanel_guild WHERE guild_id = $1", guild.id)
        await self.bot.db.execute("DELETE FROM controlpanel_autorole WHERE guild_id = $1", guild.id)
        await self.bot.db.execute("DELETE FROM controlpanel_birthday WHERE guild_id = $1", guild.id)
        await self.bot.db.execute("DELETE FROM controlpanel_reactionrole WHERE guild_id = $1", guild.id)
        await self.bot.db.execute("DELETE FROM controlpanel_reminder WHERE guild_id = $1", guild.id)


def setup(bot):
    bot.add_cog(Server_Setup(bot))