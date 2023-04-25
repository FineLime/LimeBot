import discord 
from discord.ext import tasks

async def get_guild(db, guild_id):

    guild = await db.execute("SELECT * FROM controlpanel_guild WHERE guild_id = ?", guild_id).fetchone()
    if not guild:
        await insert_guild(guild_id)
        guild = await db.execute("SELECT * FROM controlpanel_guild WHERE guild_id = ?", guild_id).fetchone()
    return guild

async def insert_guild(db, guild_id):

    await db.execute("INSERT INTO controlpanel_guild (guild_id, access_token, refresh_token, welcome_channel, welcome_message, birthday_channel, birthday_message, logs_channel, membercount_channel, welcome_enabled, logs_enabled) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)", guild_id, None, None, None, None, None, None, None, None, 0, 0)

async def delete_guild(db, guild_id):

    await db.execute("DELETE FROM controlpanel_member WHERE guild_id = $1", guild_id)
    await db.execute("DELETE FROM controlpanel_birthday WHERE guild_id = $1", guild_id)
    await db.execute("DELETE FROM controlpanel_guild WHERE guild_id = $1", guild_id)
    await db.execute("DELETE FROM controlpanel_customcommand WHERE guild_id = $1", guild_id)
    await db.execute("DELETE FROM controlpanel_quotes WHERE guild_id = $1", guild_id)
    await db.execute("DELETE FROM controlpanel_autorole WHERE guild_id = $1", guild_id)



