import patreon 
from discord.ext import commands
import os
from datetime import datetime
import requests

creator_access_token = os.environ.get("CREATOR_ACCESS_TOKEN")
api_client = patreon.API(creator_access_token)
campaign_id = os.environ.get("CAMPAIGN_ID")


fields = {
    'patron_count': 'patron_count',
}
patrons = api_client.fetch_page_of_pledges(campaign_id, 200, fields=fields)


patreon_cache = { 
    'patrons': None,
    'last_update': None
}

fields = {
    'fields[tier]': 'title',
    'fields[member]': 'email'
}

titles = { 
    '9638482': 'Tangerine',
    '9638654': 'Grapefruit',
    '9638663': 'Lemon'
}

tiers = ['9638482', '9638654', '9638663']

member_id = "123456789"

url = f"https://api.patreon.com/oauth2/v2/campaigns/{campaign_id}/members?include=currently_entitled_tiers&fields[tier]=title&fields[member]=email"
member_url = f"https://api.patreon.com/oauth2/v2/members/{member_id}?include=currently_entitled_tiers&fields[tier]=title&fields[member]=email&fields[user]=social_connections"

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

    tier_name = titles[tier_id]

    return tier_id

    
# Wrappers for patron only commands

def tangerine_only():
    def predicate(ctx):

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
    
