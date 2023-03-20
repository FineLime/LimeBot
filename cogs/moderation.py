import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_messages=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def purge(self, ctx, amount: int):
        await ctx.respond(f"Purging {amount} messages...", ephemeral=True)
        await ctx.channel.purge(limit=amount)


    @has_permissions(manage_messages=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def purge_match(self, ctx, amount: int, *, match):
        deleted = 0
        async for message in ctx.channel.history(limit=amount):
            if match in message.content:
                await message.delete()
                deleted += 1
        await ctx.respond(f"Deleted {deleted} messages.")

    @has_permissions(manage_messages=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def purge_user(self, ctx, amount: int, user: discord.Member):
        deleted = 0
        async for message in ctx.channel.history(limit=amount):
            if message.author == user:
                await message.delete()
                deleted += 1
        await ctx.respond(f"Deleted {deleted} messages.")

    @has_permissions(manage_messages=True, kick_members=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def purge_kick_match(self, ctx, amount: int, match: str): 
        deleted = 0
        kicked = []
        async for message in ctx.channel.history(limit=amount):
            if match in message.content:
                await message.delete()
                deleted += 1
                if message.author not in kicked:
                    await message.author.kick()
                    kicked.append(message.author)
        await ctx.respond(f"Deleted {deleted} messages and kicked {len(kicked)} users.")

    @has_permissions(manage_messages=True, ban_members=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def purge_ban_match(self, ctx, amount: int, match: str):
        deleted = 0
        banned = []
        async for message in ctx.channel.history(limit=amount):
            if match in message.content:
                await message.delete()
                deleted += 1
                if message.author not in banned:
                    await message.author.ban()
                    banned.append(message.author)
        await ctx.respond(f"Deleted {deleted} messages and banned {len(banned)} users.")

    @has_permissions(ban_members=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def ban(self, ctx, user: discord.Member, reason: str = None):
        
        if user.top_role >= ctx.author.top_role:
            await ctx.respond("You cannot ban this user.")
            return
        
        await user.ban(reason=reason)
        await ctx.respond(f"Banned {user.name}.")

    @has_permissions(kick_members=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def kick(self, ctx, user: discord.Member, reason: str = None):
            
        if user.top_role >= ctx.author.top_role:
            await ctx.respond("You cannot kick this user.")
            return
            
        await user.kick(reason=reason)
        await ctx.respond(f"Kicked {user.name}.")

    @has_permissions(manage_messages=True)
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def warn(self, ctx, user: discord.Member, reason: str = None): 

        if user.top_role >= ctx.author.top_role:
            await ctx.respond("You cannot warn this user.")
            return
        
        await user.send(f"You have been warned in {ctx.guild.name} for {reason}.")
        await ctx.respond(f"Warned {user.name}.")

def setup(bot):
    bot.add_cog(Moderation(bot))
