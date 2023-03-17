import discord
from discord.ext import commands
import os
import io 
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import aiohttp

class Imagine(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        os.environ["STABILITY_HOST"] = 'grpc.stability.ai:443'

        self.stability_api = client.StabilityInference(
            key= os.environ.get('STABILITY_API_KEY'),
            engine='stable-diffusion-v1-5'
        )

    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
    async def imagine(self, ctx, prompt: str):

        await ctx.defer()
        images = self.stability_api.generate(
            prompt=prompt,
            steps=30,
            cfg_scale=8.0,
            width=512,
            height=512,
            samples=4,
        )

        files = []
        for resp in images: 
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    image_bytes = io.BytesIO(artifact.binary)
                    files.append(discord.File(image_bytes, filename='image.png'))
            
        await ctx.followup.send(f"**{prompt}**", files=files)


                    

def setup(bot):
    bot.add_cog(Imagine(bot))
