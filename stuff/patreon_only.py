import patreon 
from discord.ext import commands
import os
from datetime import datetime
import requests

creator_access_token = os.environ.get("CREATOR_ACCESS_TOKEN")
api_client = patreon.API(creator_access_token)
campaign_id = os.environ.get("CAMPAIGN_ID")

cool_people = ["348538644887240716"]

patreon_cache = { 
    'patrons': None,
    'last_update': None
}

tiers = ['9638482', '9638654', '9638663']

def get_patreon_users():  

    if patreon_cache['last_update'] is not None and (datetime.now() - patreon_cache['last_update']).total_seconds() < 300:
        return patreon_cache['patrons']
    
    patrons = api_client.fetch_page_of_pledges(campaign_id, 200).json_data

    patreon_cache['patrons'] = patrons 
    patreon_cache['last_update'] = datetime.now()

    return patrons

def get_patreon_title(patron_id): 

    patrons = get_patreon_users()
    patron = [patron for patron in patrons['data'] if patron['relationships']['patron']['data']['id'] == patron_id] 

    if len(patron) == 0:
        return None
    
    patron = patron[0]  
    tier_id = patron['relationships']['reward']['data']['id']

    return tier_id

    
# Wrappers for patron only commands

def tangerine_only():
    def predicate(ctx):

        if str(ctx.author.id) in cool_people:
            return True

        patrons = get_patreon_users()
        
        patrons = [patron for patron in patrons['included'] if patron['type'] == 'user' and patron['attributes']['social_connections']['discord']['user_id'] == str(ctx.author.id)]

        if len(patrons) == 0:
            return False
        
        patron = patrons[0]
        tier_id = get_patreon_title(patron['id'])

        if tier_id is None:
            return False
        
        return tiers.index(tier_id) >= 0

    return commands.check(predicate)

def grapefruit_only():
    def predicate(ctx):

        if str(ctx.author.id) in cool_people:
            return True

        patrons = get_patreon_users()
        
        patrons = [patron for patron in patrons['included'] if patron['type'] == 'user' and patron['attributes']['social_connections']['discord']['user_id'] == str(ctx.author.id)]

        if len(patrons) == 0:
            return False
        
        patron = patrons[0]
        tier_id = get_patreon_title(patron['id'])

        if tier_id is None:
            return False
        
        return tiers.index(tier_id) >= 1

    return commands.check(predicate)

def lemon_only():
    def predicate(ctx):

        if str(ctx.author.id) in cool_people:
            return True

        patrons = get_patreon_users()
        
        patrons = [patron for patron in patrons['included'] if patron['type'] == 'user' and patron['attributes']['social_connections']['discord']['user_id'] == str(ctx.author.id)]

        if len(patrons) == 0:
            return False
        
        patron = patrons[0]
        tier_id = get_patreon_title(patron['id'])

        if tier_id is None:
            return False
        
        return tiers.index(tier_id) >= 2

    return commands.check(predicate)
    
