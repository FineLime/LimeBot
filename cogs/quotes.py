import discord
from discord.ext import commands
from discord import Option, default_permissions
import random

class Quotes(commands.Cog): 

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], description="Quote a message")
    @default_permissions(manage_messages=True)
    async def addquote(self, ctx, message: Option(str, "What to quote?")):

        #check if any quotes exist
        data = await self.bot.db.fetch("SELECT quote_id FROM controlpanel_quotes WHERE guild_id = $1", ctx.guild.id)

        if not data:
            await self.bot.db.execute("INSERT INTO controlpanel_quotes (guild_id, quote_id, quote) VALUES ($1, 1, $2)", ctx.guild.id, message)
            await ctx.respond("Quote added.")
            return

        await self.bot.db.execute("INSERT INTO controlpanel_quotes (guild_id, quote_id, quote) VALUES ($1, (SELECT MAX(quote_id) FROM controlpanel_quotes WHERE guild_id = $1) + 1, $2)", ctx.guild.id, message)
        await ctx.respond("Quote added.")

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], description="Remove a quote")
    @default_permissions(manage_messages=True)
    async def removequote(self, ctx, quote_id: Option(int, "Quote ID")):

        await self.bot.db.execute("DELETE FROM controlpanel_quotes WHERE guild_id = $1 AND quote_id = $2", ctx.guild.id, quote_id)
        await ctx.respond("Quote removed.")

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], description="Get a quote")
    async def quote(self, ctx, quote_id: Option(int, "Quote ID") = None):

        if not quote_id:
            data = await self.bot.db.fetch("SELECT quote_id FROM controlpanel_quotes WHERE guild_id = $1", ctx.guild.id)
            quote_id = random.choice(data)['quote_id']

        data = await self.bot.db.fetchrow("SELECT quote FROM controlpanel_quotes WHERE guild_id = $1 AND quote_id = $2", ctx.guild.id, quote_id)

        if not data:
            await ctx.respond("Quote not found.", ephemeral=True)
            return

        await ctx.respond(f"Quote #{quote_id}: {data['quote']}")