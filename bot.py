import discord, quiz, random, os, asyncio
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
        verse_key = quiz.get_random_verse_key()
        url = quiz.get_audio(random.randint(1, 13), verse_key)
        glyph = quiz.get_verse_glyph(verse_key)
        print(url)
        async with ctx.typing():
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=url))
        await ctx.send(f"```{glyph} ({verse_key})```")
    except:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='quran.quiz.surah_name_from_audio_verse_all', help='To play a random verse from the Quran and ask the user to guess the surah name')
async def quran_quiz_1(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    
    verse_key = quiz.get_random_verse_key()
    chapter_number = verse_key.split(':')[0]
    chapter_number = int(chapter_number)
    audio_url = quiz.get_audio(random.randint(1, 13), verse_key)
    glyph = quiz.get_verse_glyph(verse_key)
    correct_answer = quiz.get_chapter_name_from_verse_key(verse_key)
    
    invalid_answers = []
    invalid_sequence = [x for x in range(chapter_number - 4, chapter_number + 4) if x != chapter_number]
    
    for i in invalid_sequence:
        if i > 1 and i < 115:
            print(i)
            invalid_answers.append(quiz.get_chapter_name_from_verse_key(i))
    choices = random.sample(random.sample(invalid_answers, 3) + [correct_answer], 4)
    ans_index = choices.index(correct_answer)
    user_ans = ""
    
    async with ctx.typing():
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=audio_url))
        await ctx.send(f"> {glyph}\n is from which surah? \n A. {choices[0]}\n B. {choices[1]}\n C. {choices[2]}\n D. {choices[3]}")

    def is_correct(m):
        return m.author == ctx.author

    try:
        user_ans = await bot.wait_for("message", check=is_correct, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("oops timeout!")
        
    if user_ans.content.lower() == ['a','b','c','d'][ans_index].lower():
        await ctx.send("Correct!")
        if voice_channel.is_playing():
            await voice_channel.stop()
        await quran_quiz_1(ctx)
    else:
        await ctx.send("Wrong!")
        
@bot.command(name='quran.quiz.surah_name_from_verse_audio_juz', help='To play a random verse from the Quran and ask the user to guess the surah name')
async def quran_quiz_2(ctx, juz = 30, qari = 7):
    server = ctx.message.guild
    voice_channel = server.voice_client
    
    verse_data = quiz.get_random_verse_data_from_juz(juz, qari)
    verse_key = verse_data['verse_key']
    chapter_number = verse_key.split(':')[0]
    chapter_number = int(chapter_number)
    audio_url = verse_data['audio']['url']
    glyph = quiz.get_verse_glyph(verse_key)
    correct_answer = quiz.get_chapter_name_from_verse_key(verse_key)
    
    invalid_answers = []
    invalid_sequence = [x for x in range(chapter_number - 4, chapter_number + 4) if x != chapter_number]
    
    for i in invalid_sequence:
        if i > 1 and i < 115:
            invalid_answers.append(quiz.get_chapter_name_from_verse_key(i))
    choices = random.sample(random.sample(invalid_answers, 3) + [correct_answer], 4)
    ans_index = choices.index(correct_answer)
    user_ans = ""
    
    async with ctx.typing():
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=audio_url))
        # await ctx.send(f"> {glyph}\n is from which surah? \n A. {choices[0]}\n B. {choices[1]}\n C. {choices[2]}\n D. {choices[3]}")
        await ctx.send(f"Listen, that audio is from which surah? \n A. {choices[0]}\n B. {choices[1]}\n C. {choices[2]}\n D. {choices[3]}\n or type `stop` to stop the quiz")

    def is_correct(m):
        return m.author == ctx.author

    try:
        user_ans = await bot.wait_for("message", check=is_correct, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("oops timeout!")
        
    if user_ans.content.lower() == ['a','b','c','d'][ans_index].lower():
        await ctx.send("Correct!")
        if voice_channel.is_playing():
            await voice_channel.stop()
        await quran_quiz_2(ctx, juz, qari)
    elif user_ans.content.lower() == "stop".lower():
        await ctx.send("Stopped!")
    else:
        await ctx.send(f"Wrong! {correct_answer}")
        if voice_channel.is_playing():
            await voice_channel.stop()
        await quran_quiz_2(ctx, juz, qari)
        
@bot.command(name='quran.quiz.next_verse', help='To play a random verse from the Quran and ask the user to guess the next verse')
async def quran_quiz_3(ctx, juz = 30, qari = 7):
    server = ctx.message.guild
    voice_channel = server.voice_client
    
    verse_data = quiz.get_random_verse_data_from_juz(juz, qari)
    verse_key = verse_data['verse_key']
    chapter_number = verse_key.split(':')[0]
    verse_number = verse_key.split(':')[1]
    verse_number = int(verse_number) + 1
    audio_url = verse_data['audio']['url']
    correct_answer = quiz.get_verse_glyph(f"{chapter_number}:{verse_number}")
    
    invalid_answers = []
    invalid_sequence = [x for x in range(verse_number - 4, verse_number + 4) if x != verse_number and x != verse_number - 1]
    
    for i in invalid_sequence:
        try:
            invalid_answers.append(quiz.get_verse_glyph(f"{chapter_number}:{i}"))
        except:
            pass
        
    prob = random.randint(1, 2)
    
    if prob == 1:
        choice = random.sample(invalid_answers, 1)
        ans = 'b'
    else:
        choice = [correct_answer]
        ans = 'a'
    
    user_ans = ""
    
    async with ctx.typing():
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=audio_url))
        # await ctx.send(f"> {glyph}\n is from which surah? \n A. {choices[0]}\n B. {choices[1]}\n C. {choices[2]}\n D. {choices[3]}")
        await ctx.send(f"Dengarkan, apakah ayat dibawah terletak setelah ayat yang didengar? \n {choice} \n A. Benar\n B. Salah\n or type `stop` to stop the quiz")

    def is_correct(m):
        return m.author == ctx.author

    try:
        user_ans = await bot.wait_for("message", check=is_correct, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("oops timeout!")
        
    if user_ans.content.lower() == ans.lower():
        await ctx.send("Correct!")
        if voice_channel.is_playing():
            await voice_channel.stop()
        await quran_quiz_3(ctx, juz, qari)
    elif user_ans.content.lower() == "stop".lower():
        await ctx.send("Stopped!")
    else:
        await ctx.send("Wrong!")
        if voice_channel.is_playing():
            await voice_channel.stop()
        await quran_quiz_3(ctx, juz, qari)
    
    

bot.run(os.getenv('BOT_TOKEN'))  
# Don't reveal your bot token, regenerate it asap if you do