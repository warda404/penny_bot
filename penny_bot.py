import discord
from discord.ext.commands import Bot
import random
import requests
from requests.exceptions import RequestException

# imports for gif content
import giphy_client
from giphy_client.rest import ApiException

# tokens and bot prefix
bot = Bot(command_prefix='!')
discord_token = 'NzE1NTYxODU4MDg1NDIxMDU3.Xs_ERA.rkZ9Y2A4zKEIEpcGdYJy5a5cSVU'
giphy_token = 'UVkPW7wTQHcJrAJpCMAoyGdsCKfvXDKd'
api_instance = giphy_client.DefaultApi()


@bot.event
async def on_ready():
    print("Login as")
    print(bot.user.name)
    print("-------")


# @bot.event
# async def on_message(message):
#     # Whenever a user other than bot says "hi"
#     if message.content.startsWith('Hi') or message.content.startsWith('hi') or message.content.startsWith('Hey') or message.content.startsWith('hey') or message.content.startsWith('Hello') or message.content.startsWith('hello'):
#         hi_responses = [' Hi!!!', ' Hello <3',
#                         ' Salutations! :)', ' Hey there ;)', ' Greetings!']
#         response = random.choices(hi_responses)
#         await message.channel.send(message.author.mention + response)
#     elif message.content.startsWith('Bye') or message.content.startsWith('bye') or message.content.startsWith('goodbye') or message.content.startsWith('good bye') or message.content.startsWith('Goodbye') or message.content.startsWith('Good bye') or message.content.startsWith('see ya') or message.content.startsWith('See ya') or message.content.startsWith('later') or message.content.startsWith('night') or message.content.startsWith('good night') or message.content.startsWith('goodnight'):
#         bye_responses = [' I\'ll miss you :(', ' May the force be with you',
#                          ' Live long and prosper', ' Blessings be upon you', ' Byeee ~', ' Good bye!', ' No, don\'t go!']
#         response = random.choices(bye_responses)
#         await message.channel.send(message.author.mention + response)
#
#     await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    await bot.change_presence(game=discord.Game(name='Hi %s' % (member)))
    await bot.send_message(member, "Hi %s, Welcome to the Spice Pantry! Enjoy your stay :)" % (member))


@bot.event
async def on_member_remove(member):
    await bot.change_presence(game=discord.Game(name='Bye %s' % (member)))


async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token,
                                                query, limit=30, rating='g')
        lst = list(response.data)
        gif = random.choices(lst)

        return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


@bot.command(name='penny', description='Grab my attention!')
async def penny(ctx):
    response = [
        'Yes?',
        'How\'s it going!',
        'Hmm?',
        '*what*',
        'Hello!',
        'Not now',
        'Hi!!!',
        'Hello <3',
        'Salutations! :)',
        'Hey there ;)',
        'Greetings!',
    ]

    await ctx.send(random.choice(response))


@bot.command(name='roll', description='Roll dice! May the odds be in your favour!')
async def roll(ctx):
    response = [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
    ]

    await ctx.send(random.choice(response))


@bot.command(name='8ball', description='Predict your future with my advanced AI ^[0-0]^')
async def magic_eight_ball(ctx):
    response = [
        'Without a doubt.',
        'Outlook good.',
        'Better not tell you now.',
        'Cannot predict now.',
        'My reply is no.',
        'Outlook not so good.',
        'Not a chance.',
        'Yes! A million times yes!',
        'Of course!',
        'Not in a million years.',
    ]

    await ctx.send(random.choice(response))


@bot.command(name='dance', description='〜(￣▽￣〜)(〜￣▽￣)〜')
async def dance(ctx):
    gif = await search_gifs('dance')
    await ctx.send('〜(￣▽￣〜)(〜￣▽￣)〜')
    await ctx.send(gif)


@bot.command(name='inspire', description='Get life advice from my friend, Inspirobot!')
async def inspire(ctx):
    # sends GET request to Inspirobot for image url response
    try:
        url = 'http://inspirobot.me/api?generate=true'
        params = {'generate': 'true'}
        response = requests.get(url, params, timeout=10)
        image = response.text
        await ctx.send(image)

    except RequestException:
        await ctx.send('Inspirobot is broken, there is no reason to live.')


bot.run(discord_token)
