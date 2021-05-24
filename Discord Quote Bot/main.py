import discord
import nacl
import settings
import random
from discord.ext import commands
import logging
import time
import os
from pathlib import Path
from mutagen.mp3 import MP3
from threading import Timer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='//')
block = False


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    guild = discord.utils.get(bot.guilds, name=settings.SERVER_NAME)
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.after_invoke
async def delete_message(ctx):
    await ctx.message.delete()


@bot.command(name='join')
async def join(ctx):
    voice = ctx.author.voice

    if voice is None:
        await ctx.send(content="You are currently not connected to any voice channel.", delete_after=10.0)
        return -1

    await leave(ctx)

    channel = voice.channel
    await channel.connect(timeout=5.0)
    return 0


@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()


async def base_speak(ctx, quote=None, exact_quote=None):
    global block
    if block:
        return -1
    block = True

    if quote is None:
        await ctx.send(content='You must tell me what I am supposed to say.', delete_after=7.0)
        block = False
        return -1

    arr = os.listdir('Audio_recordings')
    if str(quote) not in arr:
        await ctx.send(content='Could not find quote directory ' + str(quote) + '.', delete_after=7.0)
        block = False
        return -1

    arr = os.listdir('Audio_recordings/' + str(quote))
    if exact_quote is not None:
        if str(exact_quote) + '.mp3' not in arr:
            await ctx.send(
                content='Could not find quote file ' + str(exact_quote) + ' in directory ' + str(quote) + '.',
                delete_after=7.0)
            block = False
            return -1

    else:
        f = open('Audio_recordings/' + str(quote) + '/record.txt', "r", encoding='utf-8')
        exact_quote = int(f.read())
        f.close()
        if str(exact_quote) + '.mp3' not in arr:
            await ctx.send(content='Sorry, but there seem to be no recordings available for quote ' + str(quote) + '.',
                           delete_after=7.0)
            block = False
            return -1

        f = open('Audio_recordings/' + str(quote) + '/record.txt', "w", encoding='utf-8')
        if str(exact_quote + 1) + '.mp3' not in arr:
            f.write(str(1))
        else:
            f.write(str(exact_quote + 1))
        f.close()

    return exact_quote


def unblock():
    global block
    block = False


@bot.command(name='speak')
async def speak(ctx, quote=None, exact_quote=None):
    result = await base_speak(ctx, quote, exact_quote)

    if result != -1:
        exact_quote = result
        quote_file = Path('Audio_recordings/' + str(quote) + '/' + str(exact_quote) + '.mp3')

        if ctx.voice_client is None:
            attempt = await join(ctx)
            if attempt == -1:
                #await ctx.send(content='I am currently not connected to any voice channel.', delete_after=7.0)
                global block
                block = False
                return

        ctx.voice_client.play(discord.FFmpegPCMAudio(executable=settings.ffmpeg_executable, source=quote_file))
        length = MP3(quote_file).info.length
        await ctx.send(content='Speaking...', delete_after=length)

        t = Timer(length, unblock)
        t.start()


@bot.command(name='website_speak')
async def website_speak(ctx, quote=None, exact_quote=None, *args):
    
    result = await base_speak(ctx, quote, exact_quote)

    if result != -1:
        exact_quote = result
        quote_file = Path('Audio_recordings/' + str(quote) + '/' + str(exact_quote) + '.mp3')

        p = vlc.MediaPlayer(quote_file)
        p.play()

        if ctx.voice_client is not None:
            ctx.voice_client.play(discord.FFmpegPCMAudio(quote_file))

        length = MP3(quote_file).info.length
        await ctx.send(content='Speaking...', delete_after=length)

        t = Timer(length, unblock)
        t.start()



@bot.command(name='all_quotes')
async def all_quotes(ctx, quote=None):
    text = '```\n'
    text += 'All quotes:\n'

    arr = os.listdir('Audio_recordings')
    i = 1
    while str(i) in arr:

        arr2 = os.listdir('Audio_recordings/' + str(i))
        j = 1
        text += str(i) + ': '
        while str(j) + '.mp3' in arr2:
            j += 1

        f = open('Audio_recordings/' + str(i) + '/transcript.txt', 'r', encoding='utf-8')
        if quote is not None and quote == str(i):
            if j == 2:
                text = ('```\n' + str(i) + ': ' + f.read())[:-1] + ' [' + str(j - 1) + ' quote] ```'
            else:
                text = ('```\n' + str(i) + ': ' + f.read())[:-1] + ' [' + str(j-1) + ' quotes] ```'
            await ctx.send(content=text)
            return

        if j == 2:
            text = (text + f.read())[:-1] + ' [' + str(j - 1) + ' quote] \n'
        else:
            text = (text + f.read())[:-1] + ' [' + str(j-1) + ' quotes] \n'

        if i == 30 and quote is None:
            text += '```'
            await ctx.send(content=text)
            text = '```\n'
        i += 1

    text += '```'

    if quote is None:
        await ctx.send(content=text)


@bot.command(name='quotes')
async def quotes(ctx):
    text = '```\n'
    text += 'Available quotes:\n'

    arr = os.listdir('Audio_recordings')
    i = 1
    while str(i) in arr:

        arr2 = os.listdir('Audio_recordings/' + str(i))
        j = 1
        while str(j) + '.mp3' in arr2:
            j += 1

        f = open('Audio_recordings/' + str(i) + '/transcript.txt', 'r', encoding='utf-8')

        if j == 2:
            text += str(i) + ': '
            text = (text + f.read())[:-1] + ' [' + str(j - 1) + ' quote] \n'
        if j >= 3:
            text += str(i) + ': '
            text = (text + f.read())[:-1] + ' [' + str(j-1) + ' quotes] \n'

        if i == 30:
            text += '```'
            await ctx.send(content=text)
            text = '```\n'
        i += 1

    text += '```'
    await ctx.send(content=text)


bot.run(settings.DISCORD_TOKEN)
