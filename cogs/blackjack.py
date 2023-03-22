import discord
from discord.ext import commands
import random
import math

def get_value(cards):

    value = 0
    aces = 0
    for card in cards:
        if card[0] == "A":
            value += 11
            aces += 1
        elif card[0] in ["J", "Q", "K"] or card[0:2] == "10":
            value += 10
        else:
            value += int(card[0])
    
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    
    return value

class BlackjackView(discord.ui.View):

    def __init__(self, cards, player, dealer, bet, bot, user_id):
        self.cards = cards
        self.player = player
        self.dealer = dealer
        self.bet = bet
        self.bot = bot
        self.user_id = user_id
        super().__init__()

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary)
    async def hit(self, button: discord.ui.Button, interaction: discord.Interaction):

        card = random.choice(self.cards)
        self.player['cards'].append(card)
        self.player['value'] = get_value(self.player['cards'])
        self.cards.remove(card)

        description = ""
        if self.player['value'] > 21:
            
            description += f"Dealer Cards:\n{' '.join(self.dealer['cards'])} ({self.dealer['value']})\n\n"
            description += f"Your Cards:\n{' '.join(self.player['cards'])} ({self.player['value']})\n\n"
            description += "You busted!"
            await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins - $1 WHERE member_id = $2 and guild_id = $3", self.bet, interaction.user.id, interaction.guild.id)
            await interaction.response.edit_message(embed=discord.Embed(title=f"{interaction.user.name}'s Blackjack", description=description, color=discord.Color.blurple()), view=None)
            return
        
        description += f"Dealer Cards:\n{self.dealer['cards'][0]} 🂠 (?)\n\n"
        description += f"Your Cards:\n{' '.join(self.player['cards'])} ({self.player['value']})\n\n"
        
        await interaction.response.edit_message(embed=discord.Embed(title=f"{interaction.user.name}'s Blackjack", description=description, color=discord.Color.blurple()), view=self)


    @discord.ui.button(label="Stand", style=discord.ButtonStyle.primary)
    async def stand(self, button: discord.ui.Button, interaction: discord.Interaction):

        while self.dealer['value'] < 17:
            card = random.choice(self.cards)
            self.dealer['cards'].append(card)
            self.dealer['value'] = get_value(self.dealer['cards'])
            self.cards.remove(card)
            
        description = ""
        description += f"Dealer Cards:\n{' '.join(self.dealer['cards'])} ({self.dealer['value']})\n\n"
        description += f"Your Cards:\n{' '.join(self.player['cards'])} ({self.player['value']})\n\n"
        if self.dealer['value'] > 21:

            description += "Dealer busted!"
            await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins + $1 WHERE member_id = $2 and guild_id = $3", self.bet, interaction.user.id, interaction.guild.id)

        elif self.dealer['value'] > self.player['value']:

            description += "Dealer won!"
            await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins - $1 WHERE member_id = $2 and guild_id = $3", self.bet, interaction.user.id, interaction.guild.id)

        elif self.dealer['value'] < self.player['value']:

            description += "You won!"
            await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins + $1 WHERE member_id = $2 and guild_id = $3", self.bet, interaction.user.id, interaction.guild.id)

        else:
                
            description += "It's a tie!"

        await interaction.response.edit_message(embed=discord.Embed(title=f"{interaction.user.name}'s Blackjack", description=description, color=discord.Color.blurple()), view=None)

    
    @discord.ui.button(label="Double", style=discord.ButtonStyle.primary)
    async def double(self, button: discord.ui.Button, interaction: discord.Interaction):

        self.bet *= 2
        card = random.choice(self.cards)
        self.player['cards'].append(card)
        self.player['value'] = get_value(self.player['cards'])
        self.cards.remove(card)

        description = ""
        if self.player['value'] > 21:
            
            description += f"Dealer Cards:\n{' '.join(self.dealer['cards'])} ({self.dealer['value']})\n\n"
            description += f"Your Cards:\n{' '.join(self.player['cards'])} ({self.player['value']})\n\n"
            description += "You busted!"
            await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins - $1 WHERE member_id = $2 and guild_id = $3", self.bet, interaction.user.id, interaction.guild.id)
            await interaction.response.edit_message(embed=discord.Embed(title=f"{interaction.user.name}'s Blackjack", description=description, color=discord.Color.blurple()), view=None)
            return
        
        while self.dealer['value'] < 17:
            card = random.choice(self.cards)
            self.dealer['cards'].append(card)
            self.dealer['value'] = get_value(self.dealer['cards'])
            self.cards.remove(card)

        description += f"Dealer Cards:\n{' '.join(self.dealer['cards'])} ({self.dealer['value']})\n\n"
        description += f"Your Cards:\n{' '.join(self.player['cards'])} ({self.player['value']})\n\n"
        if self.dealer['value'] > 21:

            description += "Dealer busted!"
            await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins + $1 WHERE member_id = $2 and guild_id = $3", self.bet, interaction.user.id, interaction.guild.id)
        
        elif self.dealer['value'] > self.player['value']:

            description += "Dealer won!"
            await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins - $1 WHERE member_id = $2 and guild_id = $3", self.bet, interaction.user.id, interaction.guild.id)

        elif self.dealer['value'] < self.player['value']:

            description += "You won!"
            await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins + $1 WHERE member_id = $2 and guild_id = $3", self.bet, interaction.user.id, interaction.guild.id)

        else:
                    
            description += "It's a tie!"

        await interaction.response.edit_message(embed=discord.Embed(title=f"{interaction.user.name}'s Blackjack", description=description, color=discord.Color.blurple()), view=None)

        
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.user_id:
            return True
        else:
            await interaction.response.send_message("This isn't your blackjack game!", ephemeral=True)
            return False
    
        
       

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def blackjack(self, ctx, bet: int = 0):

        if bet < 0: 
            await ctx.respond("You can't bet a negative amount of coins.")
            return
        
        result = await self.bot.db.fetchrow("SELECT coins FROM controlpanel_member WHERE member_id = $1 and guild_id = $2", ctx.author.id, ctx.guild.id)

        if not result:
            await ctx.respond("You don't have enough coins.")
            return
        
        balance = result['coins']

        if bet > balance:
            await ctx.respond("You don't have enough coins.")
            return

        cards = [
            "A\♥", "A\♦", "A\♣", "A\♠",
            "2\♥", "2\♦", "2\♣", "2\♠",
            "3\♥", "3\♦", "3\♣", "3\♠",
            "4\♥", "4\♦", "4\♣", "4\♠",
            "5\♥", "5\♦", "5\♣", "5\♠",
            "6\♥", "6\♦", "6\♣", "6\♠",
            "7\♥", "7\♦", "7\♣", "7\♠",
            "8\♥", "8\♦", "8\♣", "8\♠",
            "9\♥", "9\♦", "9\♣", "9\♠",
            "10\♥", "10\♦", "10\♣", "10\♠",
            "J\♥", "J\♦", "J\♣", "J\♠",
            "Q\♥", "Q\♦", "Q\♣", "Q\♠",
            "K\♥", "K\♦", "K\♣", "K\♠"
        ]
        
        dealer = { 
            "cards": [],
            "value": 0
        }
        player = {
            "cards": [],
            "value": 0
        }

        for i in range(2):
            card = random.choice(cards)
            dealer["cards"].append(card)
            cards.remove(card)

            card = random.choice(cards)
            player["cards"].append(card)
            cards.remove(card)

        dealer["value"] = get_value(dealer["cards"])
        player["value"] = get_value(player["cards"])

        embed = discord.Embed(title=f"{ctx.author.display_name}'s Blackjack", color=discord.Color.blurple())

        # Check for natural blackjack

        if dealer["value"] == 21 and player["value"] == 21:

            description = f"Dealer Cards:\n{dealer['cards'][0]} {dealer['cards'][1]}  ({dealer['value']})\n\n"
            description += f"{ctx.author.mention} Cards:\n{player['cards'][0]} {player['cards'][1]}  ({player['value']})\n\n"
            description += "It's a tie!\n"
            if bet > 0:
                description += f"You get your bet back ({bet} coins)"

            embed.description = description
            await ctx.respond(embed=embed)
            return 
                    
        elif dealer['value'] == 21: 

            description = f"Dealer Cards:\n{dealer['cards'][0]} {dealer['cards'][1]}  ({dealer['value']})\n\n"
            description += f"{ctx.author.mention} Cards:\n{player['cards'][0]} {player['cards'][1]}  ({player['value']})\n\n"
            description += "Dealer has a natural blackjack!\n"
            if bet > 0:
                description += f"You lose your bet ({bet} coins)"
                await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins - $1 WHERE member_id = $2 and guild_id = $3", bet, ctx.author.id, ctx.guild.id)

            embed.description = description
            await ctx.respond(embed=embed)
            return
        
        elif player['value'] == 21:

            description = f"Dealer Cards:\n{dealer['cards'][0]} {dealer['cards'][1]}  ({dealer['value']})\n\n"
            description += f"{ctx.author.mention} Cards:\n{player['cards'][0]} {player['cards'][1]}  ({player['value']})\n\n"
            description += "You have a natural blackjack!\n"
            if bet > 0:
                description += f"You win {math.floor(bet * 2.5)} coins"
                await self.bot.db.execute("UPDATE controlpanel_member SET coins = coins + $1 WHERE member_id = $2 and guild_id = $3", math.floor(bet * 2.5), ctx.author.id, ctx.guild.id)

            embed.description = description
            await ctx.respond(embed=embed)
            return
        
        description = f"Dealer Cards:\n{dealer['cards'][0]} 🂠  (?)\n\n"
        description += f"{ctx.author.mention} Cards:\n{player['cards'][0]} {player['cards'][1]}  ({player['value']})\n\n"
        if bet > 0:
            description += f"Bet: {bet} coins"

        embed.description = description
        message = await ctx.respond(embed=embed, view=BlackjackView(cards, player, dealer, bet, self.bot, ctx.author.id))


        
        

        


def setup(bot):
    bot.add_cog(Blackjack(bot))