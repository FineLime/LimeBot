import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import default_permissions

class Reaction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    @default_permissions(manage_roles=True)
    async def add_reaction_role(self, ctx, message: discord.Message, role: discord.Role, emoji: str):

        data = await self.bot.db.fetch("SELECT role_id, emoji FROM controlpanel_reactionrole WHERE message_id = $1", message.id)

        if not data:
            try: 
                await message.add_reaction(emoji)
            except:
                await ctx.respond("Invalid emoji.", ephemeral=True)
                return
            
            await self.bot.db.execute("INSERT INTO controlpanel_reactionrole (guild_id, message_id, role_id, emoji) VALUES ($1, $2, $3, $4)", ctx.guild.id, message.id, role.id, str(emoji))
            await ctx.respond("Reaction role added.", ephemeral=True)

        elif role.id in [x[0] for x in data]:
            await ctx.respond("This role already exists for this message.", ephemeral=True)
        
        elif emoji in [x[1] for x in data]:
            await ctx.respond("This emoji already exists for this message.", ephemeral=True)

        else:
            
            try: 
                await message.add_reaction(emoji)
            except:
                await ctx.respond("Invalid emoji.", ephemeral=True)
                return
            
            await self.bot.db.execute("INSERT INTO controlpanel_reactionrole (guild_id, message_id, role_id, emoji) VALUES ($1, $2, $3, $4)", ctx.guild.id, message.id, role.id, str(emoji))
            await ctx.respond("Reaction role created.", ephemeral=True)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    @default_permissions(manage_roles=True)
    async def remove_reaction_role(self, ctx, message: discord.Message, role: discord.Role = None, emoji: str = None): 

        if not role and not emoji:
            await ctx.respond("You must provide a role or an emoji.", ephemeral=True)
            return
        
        if role: 
            await self.bot.db.execute("DELETE FROM controlpanel_reactionrole WHERE message_id = $1 AND role_id = $2", message.id, role.id)
            await ctx.respond("Reaction role removed.", ephemeral=True)

        if emoji:
            await self.bot.db.execute("DELETE FROM controlpanel_reactionrole WHERE message_id = $1 AND emoji = $2", message.id, emoji)
            await ctx.respond("Reaction role removed.", ephemeral=True)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    @default_permissions(manage_roles=True)
    async def clear_reaction_roles(self, ctx, message: discord.Message):

        await self.bot.db.execute("DELETE FROM controlpanel_reactionrole WHERE message_id = $1", message.id)
        await ctx.respond("Reaction roles cleared.", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        message_id = payload.message_id
        guild_id = payload.guild_id
        emoji = payload.emoji
        member = payload.member


        if member.bot:
            return

        if guild_id is None:
            return
        
        data = await self.bot.db.fetch("SELECT role_id, emoji FROM controlpanel_reactionrole WHERE message_id = $1", message_id)


        if not data:
            return
        
        for role_id, emoji_id in data:
            if emoji_id == str(emoji):
                role = discord.utils.get(member.guild.roles, id=role_id)
                await member.add_roles(role)
                return
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        message_id = payload.message_id
        guild_id = payload.guild_id
        emoji = payload.emoji
        member = discord.utils.get(self.bot.get_guild(guild_id).members, id=payload.user_id)


        if member.bot:
            return

        if guild_id is None:
            return
        
        data = await self.bot.db.fetch("SELECT role_id, emoji FROM controlpanel_reactionrole WHERE message_id = $1", message_id)


        if not data:
            return
        
        for role_id, emoji_id in data:
            if emoji_id == str(emoji):
                role = discord.utils.get(member.guild.roles, id=role_id)
                await member.remove_roles(role)
                return
            
    @add_reaction_role.error
    async def add_reaction_role_error(self, ctx, error):
        
        if isinstance(error, MissingPermissions):
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)
            return
        
        if isinstance(error, commands.BadArgument):
            await ctx.respond("Invalid message or role.", ephemeral=True)
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond("Missing required argument.", ephemeral=True)
            return
        
    @remove_reaction_role.error
    async def remove_reaction_role_error(self, ctx, error):

        if isinstance(error, MissingPermissions):
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)
            return
        
        if isinstance(error, commands.BadArgument):
            await ctx.respond("Invalid message or role.", ephemeral=True)
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond("Missing required argument.", ephemeral=True)
            return
        
    @clear_reaction_roles.error
    async def clear_reaction_roles_error(self, ctx, error):

        if isinstance(error, MissingPermissions):
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)
            return
        
        if isinstance(error, commands.BadArgument):
            await ctx.respond("Invalid message.", ephemeral=True)
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond("Missing required argument.", ephemeral=True)
            return
        

def setup(bot):
    bot.add_cog(Reaction(bot))