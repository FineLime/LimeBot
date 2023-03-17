import discord 
from discord.ext import commands
import math

class pollView(discord.ui.View):

    def __init__(self, timeout):
        super().__init__(timeout=timeout*60)
        self.voters = []

    @discord.ui.button(label="End Poll", style=discord.ButtonStyle.red, row=2) 
    async def end_poll(self, button: discord.ui.Button, interaction: discord.Interaction):

        if interaction.user.has_guild_permissions(manage_messages=True): 
            self.stop()
            await interaction.response.send_message("Poll ended.", ephemeral=True)
            await self.message.edit(view=None, embed=discord.Embed(title=self.message.embeds[0].title, description=f"{self.message.embeds[0].description} \n\n**Poll Ended**", color=discord.Color.blurple()))
        
        await interaction.response.send_message("Poll ended.", ephemeral=True)
        await interaction.message.edit(view=None, embed=discord.Embed(title=self.message.embeds[0].title, description=f"{self.message.embeds[0].description} \n\n**Poll Ended**", color=discord.Color.blurple()))
        self.stop()


class pollButton(discord.ui.Button):
    def __init__(self, label, row): 
        super().__init__(label=label, style=discord.ButtonStyle.blurple, custom_id=label, row=row)

    async def callback(self, interaction: discord.Interaction):
        
        if interaction.user.id in self.view.voters:
            await interaction.response.send_message("You have already voted on this poll.", ephemeral=True)
            return
        
        self.view.voters.append(interaction.user.id)
        await interaction.response.send_message(f"You have voted for {self.label}.", ephemeral=True)

        description = self.view.message.embeds[0].description.split("\n")
        for i, line in enumerate(description):
            if line.split(".")[1].split("(")[0].strip() == self.label:
                description[i] = f"{i+1}. {self.label} ({int(line.split('(')[1].split(')')[0])+1})"
                break

        #await self.view.message.edit(embed=discord.Embed(title=self.view.message.embeds[0].title, description="\n".join(description), color=discord.Color.blurple())) 
        await interaction.message.edit(embed=discord.Embed(title=self.view.message.embeds[0].title, description="\n".join(description), color=discord.Color.blurple()))


class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def poll(self, ctx, question: str, hours: int, option: str):

        options = option.split(" | ")
        if len(options) > 10:
            return await ctx.send("You can only have up to 10 options.")
        if len(options) < 2:
            return await ctx.send("You need at least 2 options.")
        
        view = pollView(timeout=hours) 
        for i, option in enumerate(options):
            view.add_item(pollButton(option, math.floor(i/5)))
        
        embed = discord.Embed(title=question, color=discord.Color.blurple())
        embed.description = "\n".join([f"{i+1}. {option} (0)" for i, option in enumerate(options)])

        await ctx.respond(embed=embed, view=view)
        
        

def setup(bot):
    bot.add_cog(Poll(bot))
