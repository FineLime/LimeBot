import discord
from discord.ext import commands

class Member_Join(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     async with self.bot.db.execute("SELECT welcome_channel, welcome_message, welcome_enabled, autorole, member_count_channel FROM controlpanel_guilds WHERE guild_id = ?", (member.guild.id,)) as cursor:
    #         data = await cursor.fetchone()

    #     data = data[0]

    #     if data['welcome_enabled'] == 1: 
    #         channel = member.guild.get_channel(data['welcome_channel'])
    #         await channel.send(data['welcome_message'].replace("{user}", str(member.mention)).replace("{server}", str(member.guild.name)).replace("{member_count}", str(member.guild.member_count)))

    #     if data['autorole'] != None:
    #         role = member.guild.get_role(data['autorole'])
    #         await member.add_roles(role)

    #     if data['member_count_channel'] != None:
    #         channel = member.guild.get_channel(data['member_count_channel'])
    #         await channel.edit(name=f"Members: {member.guild.member_count}")
        
def setup(bot):
    bot.add_cog(Member_Join(bot))
        
