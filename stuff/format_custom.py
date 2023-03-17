import re

def format_custom_command_response(ctx, response):  

    ctx_message = ctx.content 
    response = response.replace('{$author}', ctx.author.mention)
    response = response.replace('{$author_id}', str(ctx.author.id))
    response = response.replace('{$author_name}', ctx.author.name)
    response = response.replace('{$author_discriminator}', ctx.author.discriminator)
    #response = response.replace('{$author_avatar}', ctx.author.avatar_url)
    response = response.replace('{$author_created_at}', str(ctx.author.created_at))
    response = response.replace('{$author_joined_at}', str(ctx.author.joined_at))
    response = response.replace('{$author_status}', str(ctx.author.status))
    response = response.replace('{$author_top_role}', ctx.author.top_role.mention)

    response = response.replace('{$channel}', ctx.channel.mention)
    response = response.replace('{$channel_id}', str(ctx.channel.id))
    response = response.replace('{$channel_name}', ctx.channel.name)
    response = response.replace('{$channel_created_at}', str(ctx.channel.created_at))
    response = response.replace('{$channel_topic}', ctx.channel.topic or 'None')
    response = response.replace('{$channel_type}', str(ctx.channel.type))

    response = response.replace('{$guild}', ctx.guild.name)
    response = response.replace('{$guild_id}', str(ctx.guild.id))
    response = response.replace('{$guild_name}', ctx.guild.name)
    #response = response.replace('{$guild_icon}', ctx.guild.icon_url)
    response = response.replace('{$guild_created_at}', str(ctx.guild.created_at))

    response = response.replace('{$guild_owner}', ctx.guild.owner.mention)
    response = response.replace('{$guild_owner_id}', str(ctx.guild.owner.id))
    response = response.replace('{$guild_owner_name}', ctx.guild.owner.name)
    response = response.replace('{$guild_owner_discriminator}', ctx.guild.owner.discriminator)
    #response = response.replace('{$guild_owner_avatar}', ctx.guild.owner.avatar_url)
    response = response.replace('{$guild_owner_created_at}', str(ctx.guild.owner.created_at))
    response = response.replace('{$guild_owner_joined_at}', str(ctx.guild.owner.joined_at))
    response = response.replace('{$guild_owner_status}', str(ctx.guild.owner.status))
    response = response.replace('{$guild_owner_top_role}', ctx.guild.owner.top_role.mention)

    response = response.replace('{$message_id}', str(ctx.id))
    response = response.replace('{$message}', ctx.content)

    args = re.findall(r'\{\$args\d\+?\}', response)
    split_args = ctx_message.split(' ')[1:]
    for arg in args:
        arg_number = arg[6:-1]
        if arg_number[-1] == '+':
            arg_number = arg_number[:-1]
            try:
                response = response.replace(arg, ' '.join(split_args[int(arg_number)-1:]))
            except IndexError:
                response = "This command requires argument " + arg_number + "."
        else:
            try:
                response = response.replace(arg, split_args[int(arg_number)-1])
            except IndexError:
                response = "This command requires argument " + arg_number + "."

    # randoms = re.findall(r'\{\$random (.+ \|\| )+.+\}', response)
    # for random in randoms:
    #     options = random[9:-1].split(' || ')
    #     response = response.replace(random, random.choice(options))

    # ifs = re.findall(r'\{\$if [.+] \!?(>|<|=) [.+] \".+\"}', response) 
    # for if_statement in ifs:

    #     condition = re.findall(r'[.+] \!?(>|<|=) [.+]', if_statement)[0]
    #     if_response = re.findall(r'\".+\"', if_statement)[-1]

    #     operator = condition.split(' ')[1]
    #     if operator == '=':
    #         if condition.split(' ')[0] == condition.split(' ')[2]:
    #             response = response.replace(if_statement, if_response)
    #         else:
    #             response = response.replace(if_statement, '')

    #     elif operator == '>':

    #         if int(condition.split(' ')[0]) > int(condition.split(' ')[2]):
    #             response = response.replace(if_statement, if_response)
    #         else:
    #             response = response.replace(if_statement, '')

    #     elif operator == '<':

    #         if int(condition.split(' ')[0]) < int(condition.split(' ')[2]):
    #             response = response.replace(if_statement, if_response)
    #         else:
    #             response = response.replace(if_statement, '')

    #     elif operator == '!=':

    #         if condition.split(' ')[0] != condition.split(' ')[2]:
    #             response = response.replace(if_statement, if_response)
    #         else:
    #             response = response.replace(if_statement, '')

    return response