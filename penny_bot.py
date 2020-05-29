import discord
from discord.ext.commands import Bot
import random

# imports for gif content
import giphy_client
from giphy_client.rest import ApiException

# tokens and bot prefix
discord_token = 'NzE1NTYxODU4MDg1NDIxMDU3.Xs_ERA.rkZ9Y2A4zKEIEpcGdYJy5a5cSVU'
giphy_token = 'UVkPW7wTQHcJrAJpCMAoyGdsCKfvXDKd'
bot = Bot(command_prefix='!')
api_instance = giphy_client.DefaultApi()


class DiscordClient(discord.Client):
    @bot.event
    async def on_ready(self):
        print("Login as")
        print(self.user)
        print("-------")

    async def on_message(self, message):
        # Whenever a user other than bot says "hi"
        if message.author != self.user:
            if message.content == 'hi':
                await message.channel.send('Hi there!!! ' + message.author.mention)
            elif message.content == 'hello':
                await message.channel.send('Hello :) ' + message.author.mention)
            elif message.content == 'hey':
                await message.channel.send(message.author.mention + 'Hey yourself :D')
            elif message.content == 'bye':
                await message.channel.send(message.author.mention + ' May the force be with you')
            elif message.content == "good bye":
                await message.channel.send(message.author.mention + ' Live long and prosper')


client = DiscordClient()
client.run(discord_token)


# @bot.event
# async def on_ready():
#     print("Login as")
#     print(bot.user.name)
#     print("-------")


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
    ]

    await ctx.send(random.choice(response))


@bot.command(name='8ball', description='Predict your future with my advanced AI ^[0-0]^ ')
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

bot.run(discord_token)
