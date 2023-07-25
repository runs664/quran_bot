import discord, quiz, random, os
from dotenv import load_dotenv
from discord.ext import commands,tasks

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>>', intents=intents)

@bot.event
async def on_ready():
    print("The bot is ready!")
    
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")
    
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    
@bot.command(name='play', help='To play song')
async def play(ctx,url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=url))
        await ctx.send('**Now playing:** {}'.format(url))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
        
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
        
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")
        
# quran section
@bot.command(name='quran.random', help='To play a random verse from the Quran')
async def quran_random(ctx):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        url = quiz.get_audio(random.randint(1, 13), quiz.get_random_verse_key())
        async with ctx.typing():
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=url))
        await ctx.send('**Now playing:** {}'.format(url))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
    
bot.run(os.getenv('BOT_TOKEN'))  
# Don't reveal your bot token, regenerate it asap if you do