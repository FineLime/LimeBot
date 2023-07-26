import discord
from discord.ext import commands
import os
import io 
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import aiohttp
from stuff.patreon_only import tangerine_only, get_patreon_tier
from discord import Option

engines = [ 
    'v1.5',
    'v2.1',
    'sdxl-0.9',
    'sdxl-beta'
]

# Enum: 3d-model analog-film anime cinematic comic-book digital-art enhance fantasy-art isometric line-art low-poly modeling-compound neon-punk origami photographic pixel-art tile-texture 

styles = [ 
    '3d-model',
    'analog-film',
    'anime',
    'cinematic',
    'comic-book',
    'digital-art',
    'enhance',
    'fantasy-art',
    'isometric',
    'line-art',
    'low-poly',
    'modeling-compound',
    'neon-punk',
    'origami',
    'photographic',
    'pixel-art',
    'tile-texture'

]

class ImagineView(discord.ui.View):

    def __init__(self, bot, prompt, user, stability_api): 
        self.bot = bot
        self.prompt = prompt
        self.user = user
        self.stability_api = stability_api
        super().__init__()

    @discord.ui.select( 
        placeholder="Regenerate",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="v1.5", value="v1.5"),
            discord.SelectOption(label="v2.1", value="v2.1"),
            discord.SelectOption(label="sdxl-0.9", value="sdxl-0.9"),
            discord.SelectOption(label="sdxl-beta", value="sdxl-beta")
        ]
    )
    async def regenerate(self, select: discord.ui.Select, interaction: discord.Interaction):
        
        engine = select.values[0]
        await interaction.response.defer()
        images = self.stability_api[engine].generate(
            prompt=self.prompt,  
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
            
        await interaction.followup.send(files=files, view=ImagineView(self.bot, self.prompt, self.user, self.stability_api))

    async def interaction_check(self, interaction: discord.Interaction):

        if interaction.user.id == self.user:
            return True
        else:
            await interaction.response.send_message("You are not the owner of this interaction", ephemeral=True)
            return False




class Imagine(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        os.environ["STABILITY_HOST"] = 'grpc.stability.ai:443'
        self.stability_api = { 
            "v1.5": client.StabilityInference(
                key = os.environ.get('STABILITY_API_KEY'),
                engine='stable-diffusion-v1-5',
                verbose=True
            ),
            "v2.1": client.StabilityInference(
                key = os.environ.get('STABILITY_API_KEY'),
                engine='stable-diffusion-512-v2-1',
                verbose=True
            ),
            "sdxl-beta": client.StabilityInference(
                key = os.environ.get('STABILITY_API_KEY'),
                engine='stable-diffusion-xl-beta-v2-2-2',
                verbose=True
            ), 
            "sdxl-0.9": client.StabilityInference(
                key = os.environ.get('STABILITY_API_KEY'),
                engine='stable-diffusion-xl-1024-v0-9',
                verbose=True
            )

        }

    @tangerine_only()
    @commands.slash_command(guild_ids=[234119683538812928, 1065746636275453972], description="Generate an image from a prompt")
    async def imagine(self, ctx, prompt: str, engine: Option(str, description="The engine to use", choices=engines, required=False) = "v1.5", steps: int = 30, style: Option(str, description="The style to use", choices=styles, required=False) = None):

        if steps < 10: 
            await ctx.respond("You must generate at least 10 steps.", ephemeral=True)
            return

        await ctx.defer()

        tier = get_patreon_tier(ctx.author.id)
        if tier == 0 and steps > 30:
            await ctx.followup.send("Tangerines can only generate up to 30 steps. Subscribe to Grapefruit to generate up to 75 steps or Lemon to generate up to 150 steps.", ephemeral=True)
            return
        elif tier == 1 and steps > 75:
            await ctx.followup.send("Grapefruit can only generate up to 75 steps. Subscribe to Lemon to generate up to 150 steps.", ephemeral=True)
            return
        elif tier == 2 and steps > 150:
            await ctx.followup.send("150 is the maximum amount of steps.", ephemeral=True)
            return



        images = self.stability_api[engine].generate(
            prompt=prompt,  
            steps=steps,
            cfg_scale=8.0,
            width=512,
            height=512,
            samples=4,
            style_preset=style
        )

        files = []
        for resp in images: 
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    image_bytes = io.BytesIO(artifact.binary)
                    files.append(discord.File(image_bytes, filename='image.png'))
            
        await ctx.followup.send(f"**{prompt}**", files=files, view=ImagineView(self.bot, prompt, ctx.author.id, self.stability_api))

    @imagine.error
    async def imagine_error(self, ctx, error):
        
        if error.__class__.__name__ == "CheckFailure":
            await ctx.respond("This command is only available to Tangerine Patrons.\nYou can become a patron at https://www.patreon.com/FineLime\n\nIf you are a patron, please make sure you have linked your Discord account to your Patreon account and have waited at least 5 minutes for the cache to update.", ephemeral=True)

    
    
                    

def setup(bot):
    bot.add_cog(Imagine(bot))
