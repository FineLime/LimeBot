import discord
from discord.ext import commands
import os
import io 
import warnings
from stuff.patreon_only import tangerine_only, get_patreon_tier
import requests

#example of v3 stability api usage

# import requests

# response = requests.post(
#     f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
#     headers={
#         "authorization": f"Bearer sk-MYAPIKEY",
#         "accept": "image/*"
#     },
#     files={"none": ''},
#     data={
#         "prompt": "dog wearing black glasses",
#         "output_format": "jpeg",
#     },
# )

# if response.status_code == 200:
#     with open("./dog-wearing-glasses.jpeg", 'wb') as file:
#         file.write(response.content)
# else:
#     raise Exception(str(response.json()))


class Imagine(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.stability_key = os.environ.get('STABILITY_API_KEY')

    @tangerine_only()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], description="Generate an image from a prompt")
    async def imaginev3(self, ctx, prompt: str):
        """Generate an image from a prompt"""

        headers = {
            "authorization": f"Bearer {self.stability_key}", 
            "accept": "image/*"
        }

        data = {
            "prompt": prompt,
            "output_format": "jpeg"
        }

        await ctx.defer()

        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers=headers,
            files={"none": ''},
            data=data
        )

        if response.status_code == 200:
            await ctx.respond(file=discord.File(io.BytesIO(response.content), "image.jpeg"))
        else:
            await ctx.respond(f"An error occurred: {response.json()}", ephemeral=True)


        

    @imagine.error
    async def imagine_error(self, ctx, error):
        
        if error.__class__.__name__ == "CheckFailure":
            await ctx.respond("This command is only available to Tangerine Patrons.\nYou can become a patron at https://www.patreon.com/FineLime\n\nIf you are a patron, please make sure you have linked your Discord account to your Patreon account and have waited at least 5 minutes for the cache to update.", ephemeral=True)

    
    
                    

def setup(bot):
    bot.add_cog(Imagine(bot))
