import discord
from discord.ext import commands
import random
import math
import datetime

class Currency(commands.Cog): 

    def __init__(self, bot):
        self.bot = bot
        self.cooldown = {}

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def balance(self, ctx, member: discord.Member = None):

        user = member or ctx.author
        async with self.bot.db.execute("SELECT * FROM controlpanel_guild WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
            result = await cursor.fetchone()
        if not result:
            async with self.bot.db.execute("INSERT INTO controlpanel_guild (guild_id, access_token, refresh_token) VALUES (?, ?, ?)", (ctx.guild.id, "null", "null")) as cursor:
                await self.bot.db.commit()
        
        guild = result[0]

        async with self.bot.db.execute("SELECT * FROM controlpanel_member WHERE member_id = ? and guild_id = ?", (user.id, guild)) as cursor:
            result = await cursor.fetchone()

        if not result:
            async with self.bot.db.execute("INSERT INTO controlpanel_member (member_id, guild_id, coins, xp, level) VALUES (?, ?, ?, ?, ?)", (user.id, guild, 0, 0, 1)) as cursor:
                await self.bot.db.commit()
            balance = 0
        else:
            balance = result[2]

        embed = discord.Embed(title=f"{user.name}'s balance", description=f"{balance} coins", color=discord.Color.blurple())
        embed.set_thumbnail(url=user.display_avatar.url)
        if user != ctx.author:
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

        await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def leaderboard(self, ctx):

        async with self.bot.db.execute("SELECT * FROM controlpanel_guild WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
            result = await cursor.fetchone()
        if not result:
            async with self.bot.db.execute("INSERT INTO controlpanel_guild (guild_id, access_token, refresh_token) VALUES (?, ?, ?)", (ctx.guild.id, "null", "null")) as cursor:
                await self.bot.db.commit()
            
        guild = result[0]

        async with self.bot.db.execute("SELECT member_id, coins FROM controlpanel_member WHERE guild_id = ? ORDER BY coins DESC", (guild,)) as cursor:
            result = await cursor.fetchall()

        if not result:
            embed = discord.Embed(title="Leaderboard", description="There are no coins to show", color=discord.Color.blurple())
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
            await ctx.respond(embed=embed)
            return
        
        embed = discord.Embed(title="Leaderboard", color=discord.Color.blurple())
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        text = ""
        for i in range(min(len(result), 10)):
            text += f"{i+1}. <@{result[i][0]}> - {result[i][1]} coins\n"

        embed.description = text
        await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def pay(self, ctx, member: discord.Member, amount: int):

        if member == ctx.author:
            embed = discord.Embed(title="Error", description="You can't pay yourself", color=discord.Color.blurple())
            await ctx.respond(embed=embed)
            return
        
        await ctx.defer()
        
        async with self.bot.db.execute("SELECT coins FROM controlpanel_member WHERE member_id = ? and guild_id = ?", (ctx.author.id, ctx.guild.id)) as cursor:
            result = await cursor.fetchone()
        
        if not result:
            embed = discord.Embed(title="Error", description="You don't have enough coins", color=discord.Color.blurple())
            await ctx.followup.send(embed=embed)
            return
        
        if result[0] < amount:
            embed = discord.Embed(title="Error", description="You don't have enough coins", color=discord.Color.blurple())
            await ctx.followup.send(embed=embed)
            return
        
        async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ? WHERE member_id = ? and guild_id = ?", (result[0] - amount, ctx.author.id, ctx.guild.id)) as cursor:
            await self.bot.db.commit()

        async with self.bot.db.execute("SELECT coins FROM controlpanel_member WHERE member_id = ? and guild_id = ?", (member.id, ctx.guild.id)) as cursor:
            result = await cursor.fetchone()

        if not result:
            async with self.bot.db.execute("INSERT INTO controlpanel_member (member_id, guild_id, coins, xp, level) VALUES (?, ?, ?, ?, ?)", (member.id, ctx.guild.id, amount, 0, 1)) as cursor:
                await self.bot.db.commit()
        
        else:
            async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ? WHERE member_id = ? and guild_id = ?", (result[0] + amount, member.id, ctx.guild.id)) as cursor:
                await self.bot.db.commit()

        embed = discord.Embed(title="Success", description=f"You have paid {member.mention} {amount} coins", color=discord.Color.blurple())
        await ctx.followup.send(embed=embed)

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def slots(self, ctx, bet: int): 

        if bet < 1:
            embed = discord.Embed(title="Error", description="You can't bet less than 1 coin", color=discord.Color.blurple())
            await ctx.respond(embed=embed)
            return

        # Check if the user has enough coins
        async with self.bot.db.execute("SELECT coins FROM controlpanel_member WHERE member_id = ? and guild_id = ?", (ctx.author.id, ctx.guild.id)) as cursor:
            result = await cursor.fetchone()

        if not result:
            embed = discord.Embed(title="Error", description="You don't have enough coins", color=discord.Color.blurple())
            await ctx.respond(embed=embed)
            return
        
        if result[0] < bet:
            embed = discord.Embed(title="Error", description="You don't have enough coins", color=discord.Color.blurple())
            await ctx.respond(embed=embed)
            return
        
        # Get the emojis
        emojis = [":apple:", ":cherries:", ":grapes:", ":lemon:", ":pear:", ":watermelon:", ":peach:", ":tangerine:", ":strawberry:"]

        rows = [
            [],
            [],
            []
        ]

        for i in range(3):
            
            emoji = random.choice(emojis)
            rows[i].append(emoji)
            emojis.remove(emoji)
            emoji = random.choice(emojis)
            rows[i].append(emoji)
            emojis.remove(emoji)
            emoji = random.choice(emojis)
            rows[i].append(emoji)

            emojis = [":apple:", ":cherries:", ":grapes:", ":lemon:", ":pear:", ":watermelon:", ":peach:", ":tangerine:", ":strawberry:"]

        description = ""
        description += f"|     {rows[0][0]}{rows[0][1]}{rows[0][2]}\n"
        description += f"\▶{rows[1][0]}{rows[1][1]}{rows[1][2]}\n"
        description += f"|     {rows[2][0]}{rows[2][1]}{rows[2][2]}\n\n"

        if rows[0][0] == rows[0][1] == rows[0][2] and rows[1][0] == rows[1][1] == rows[1][2] and rows[2][0] == rows[2][1] == rows[2][2]:

            description += f"MEGA WIN!\nYou won {bet * 1923} coins"
            async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ? WHERE member_id = ? and guild_id = ?", (result[0] + bet * 1923, ctx.author.id, ctx.guild.id)) as cursor:
                await self.bot.db.commit()

        elif rows[1][0] == rows[1][1] == rows[1][2] and (rows[0][0] == rows[0][1] == rows[0][1] or rows[2][0] == rows[2][1] == rows[2][2]): 

            description += f"HUGE WIN!\nYou won {bet * 264} coins"
            async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ? WHERE member_id = ? and guild_id = ?", (result[0] + bet * 264, ctx.author.id, ctx.guild.id)) as cursor:
                await self.bot.db.commit()

        elif rows[0][0] == rows[0][1] == rows[0][2] and rows[2][0] == rows[2][1] == rows[2][2]: 
             
            description += f"HUGE WIN!\nYou won {bet * 126} coins"
            async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ? WHERE member_id = ? and guild_id = ?", (result[0] + bet * 126, ctx.author.id, ctx.guild.id)) as cursor:
                await self.bot.db.commit()

        elif rows[1][0] == rows[1][1] == rows[1][1]: 

            description += f"WIN!\nYou won {bet * 91} coins"
            async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ? WHERE member_id = ? and guild_id = ?", (result[0] + bet * 91, ctx.author.id, ctx.guild.id)) as cursor:
                await self.bot.db.commit()

        elif rows[0][0] == rows[0][1] == rows[0][2] or rows[2][0] == rows[2][1] == rows[2][2]:

            description += f"WIN!\nYou won {bet * 46} coins"
            async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ? WHERE member_id = ? and guild_id = ?", (result[0] + bet * 46, ctx.author.id, ctx.guild.id)) as cursor:
                await self.bot.db.commit()

        else: 

            description += f"LOSE!\nYou lost {bet} coins"
            async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ? WHERE member_id = ? and guild_id = ?", (result[0] - bet, ctx.author.id, ctx.guild.id)) as cursor:
                await self.bot.db.commit()

        embed = discord.Embed(title=f"{ctx.author.name}'s slots", description=description, color=discord.Color.blurple())
        await ctx.respond(embed=embed)



        









    @commands.Cog.listener()
    async def on_message(self, message):

        user = message.author
        if user.bot:
            return
        
        if f'{user.id}-{message.guild.id}' in self.cooldown:
            if (datetime.datetime.now() - self.cooldown[f'{user.id}-{message.guild.id}']).total_seconds() < 60:
                return
        
        async with self.bot.db.execute("SELECT * FROM controlpanel_guild WHERE guild_id = ?", (message.guild.id,)) as cursor:
            result = await cursor.fetchone()
        guild = result[0]

        async with self.bot.db.execute("SELECT * FROM controlpanel_member WHERE member_id = ? and guild_id = ?", (user.id, guild)) as cursor:
            result = await cursor.fetchone()

        if not result:
            async with self.bot.db.execute("INSERT INTO controlpanel_member (member_id, guild_id, coins, xp, level) VALUES (?, ?, ?, ?, ?)", (user.id, guild, 0, 0, 1)) as cursor:
                await self.bot.db.commit()
            balance = 0
            xp = 0
            level = 1
        else:
            balance = result[2]
            xp = result[3]
            level = result[4]

        balance += random.randint(1, 10)
        xp += random.randint(10, 25)
        if xp >= int(100 * math.pow(level, 1.5)):
            xp -= int(100 * math.pow(level, 1.5))
            level += 1

        async with self.bot.db.execute("UPDATE controlpanel_member SET coins = ?, xp = ?, level = ? WHERE member_id = ? and guild_id = ?", (int(balance), int(xp), int(level), user.id, guild)) as cursor:
            await self.bot.db.commit()

        self.cooldown[f'{user.id}-{message.guild.id}'] = datetime.datetime.now()







def setup(bot):
    bot.add_cog(Currency(bot))
