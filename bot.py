import discord, quiz, random, os, asyncio
from dotenv import load_dotenv
from discord.ext import commands,tasks
from discord import app_commands

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>>', intents=intents)
FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=1"'
}


@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=836835374696628244))
    print("The bot is ready!")


# @bot.tree.command(name="number guess", description="Number guessing game commands", guild=discord.Object(id=836835374696628244))
# async def number_guess(interaction : discord.Interaction):

# @bot.tree.command(name="quran-quiz", description="Qur'an related quiz commands", guild=discord.Object(id=836835374696628244))
# @app_commands.choices(tipe=[
#     app_commands.Choice(name="guess chapter name from verse - audio", value=0),
#     app_commands.Choice(name="guess chapter name from verse - text", value=1),
#     app_commands.Choice(name="guess next verse from verse - audio", value=2),
#     app_commands.Choice(name="guess next verse from verse - text", value=3),
#     app_commands.Choice(name="guess previous verse from verse - audio", value=4),
#     app_commands.Choice(name="guess previous verse from verse - text", value=5),
#     ])
# async def quran_quiz(interaction : discord.Interaction, tipe : app_commands.Choice[int], juz : int = 30, qari : int = 3):
#     ctx = await bot.get_context(interaction)
#     # if choice name from value contains audio, then call the bot to join the voice channel
#     if tipe.name.endswith("audio"):
#         await join(ctx)

#     if tipe.value == 0:
#         await quran_quiz_0(ctx, juz, qari)
#     elif tipe.value == 1:
#         pass


@bot.command(name='quran.quiz.menu', help='To show the menu of the Quran quiz')
async def quran_menu(ctx):
    embed = discord.Embed(
        title="Quran Quiz Menu",
        description=
        "Akses perintah dengan mengetik perintah\n```perintah diantara [param] adalah opsional```",
        color=0x00ff00)
    embed.add_field(name="1. Guess chapter name from verse - audio",
                    value="```>>quran.quiz.0 audio [juz] [qari]```contoh: ```>>quran.quiz.0 audio 30 3```",
                    inline=False)
    embed.add_field(name="2. Guess chapter name from verse - text",
                    value="```>>quran.quiz.0 text [juz]```contoh: ```>>quran.quiz.0 text 30```",
                    inline=False)
    embed.add_field(name="3. Guess next verse from verse - audio",
                    value="```>>quran.quiz.1 audio [juz] [qari]```contoh: ```>>quran.quiz.1 audio 30 3```",
                    inline=False)
    embed.add_field(name="4. Guess next verse from verse - text",
                    value="```>>quran.quiz.1 text [juz]```contoh: ```>>quran.quiz.1 text 30```",
                    inline=False)
    await ctx.send(embed=embed)
    
    qari_embed = discord.Embed(
        title="Quran Reciter List",
        description="Daftar pembaca al-Quran",
        color=0x00ff00)
    qari_embed.add_field(name="1. AbdulBaset AbdulSamad", value="style: Mujawwad", inline=True)
    qari_embed.add_field(name="2. AbdulBaset AbdulSamad", value="style: Murattal", inline=True)
    qari_embed.add_field(name="3. Abdur-Rahman as-Sudais", value="style: -", inline=True)
    qari_embed.add_field(name="4. Abu Bakr al-Shatri", value="style: -", inline=True)
    qari_embed.add_field(name="5. Hani ar-Rifai", value="style: -", inline=True)
    qari_embed.add_field(name="6. Mahmoud Khalil Al-Husary", value="style: -", inline=True)
    qari_embed.add_field(name="7. Mishari Rashid al-`Afasy", value="style: -", inline=True)
    qari_embed.add_field(name="8. Mohamed Siddiq al-Minshawi", value="style: Mujawwad", inline=True)
    qari_embed.add_field(name="9. Mohamed Siddiq al-Minshawi", value="style: Murattal", inline=True)
    qari_embed.add_field(name="10. Sa`ud ash-Shuraym", value="style: -", inline=True)
    qari_embed.add_field(name="11. Mohamed al-Tablawi", value="style: -", inline=True)
    qari_embed.add_field(name="12. Mahmoud Khalil Al-Husary", value="style: Muallim", inline=True)
    qari_embed.set_footer(text="Source: https://alquran.cloud/api")
    
    await ctx.send(embed=qari_embed)
        


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(
            ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='play', help='To play song')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            voice_channel.play(
                discord.FFmpegPCMAudio(executable="ffmpeg", source=url))
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
        await ctx.send(
            "The bot was not playing anything before this. Use play_song command"
        )


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
            voice_channel.play(
                discord.FFmpegPCMAudio(executable="ffmpeg",
                                       source=url,
                                       **FFMPEG_OPTIONS))
        await ctx.send(f"```{glyph} ({verse_key})```")
    except:
        await ctx.send("The bot is not connected to a voice channel.")


# @bot.command(
#     name='quran.quiz.0e',
#     help=
#     'To play a random verse from the Quran and ask the user to guess the surah name'
# )
# async def quran_quiz_0e(ctx):
#     server = ctx.message.guild
#     voice_channel = server.voice_client

#     verse_key = quiz.get_random_verse_key()
#     chapter_number = verse_key.split(':')[0]
#     chapter_number = int(chapter_number)
#     audio_url = quiz.get_audio(random.randint(1, 13), verse_key)
#     glyph = quiz.get_verse_glyph(verse_key)
#     correct_answer = quiz.get_chapter_name_from_verse_key(verse_key)

#     invalid_answers = []
#     invalid_sequence = [
#         x for x in range(chapter_number - 4, chapter_number + 4)
#         if x != chapter_number
#     ]

#     for i in invalid_sequence:
#         if i > 1 and i < 115:
#             print(i)
#             invalid_answers.append(quiz.get_chapter_name_from_verse_key(i))
#     choices = random.sample(
#         random.sample(invalid_answers, 3) + [correct_answer], 4)
#     ans_index = choices.index(correct_answer)
#     user_ans = ""

#     async with ctx.typing():
#         voice_channel.play(
#             discord.FFmpegPCMAudio(executable="ffmpeg",
#                                    source=audio_url,
#                                    **FFMPEG_OPTIONS))
#         await ctx.send(
#             f"> {glyph}\n is from which surah? \n A. {choices[0]}\n B. {choices[1]}\n C. {choices[2]}\n D. {choices[3]}"
#         )

#     def is_correct(m):
#         return m.author == ctx.author

#     try:
#         user_ans = await bot.wait_for("message", check=is_correct, timeout=60)
#     except asyncio.TimeoutError:
#         await ctx.send("oops timeout!")

#     if user_ans.content.lower() == ['a', 'b', 'c', 'd'][ans_index].lower():
#         await ctx.send("Correct!")
#         if voice_channel.is_playing():
#             await voice_channel.stop()
#         await quran_quiz_0e(ctx)
#     else:
#         await ctx.send("Wrong!")


@bot.command(
    name='quran.quiz.0',
    help=
    'To play a random verse from the Quran and ask the user to guess the surah name'
)
async def quran_quiz_0(ctx, tipe, juz=30, qari=7):
    server = ctx.message.guild
    voice_channel = server.voice_client

    verse_data = quiz.get_random_verse_data_from_juz(juz, qari)
    verse_key = verse_data['verse_key']
    chapter_number = verse_key.split(':')[0]
    chapter_number = int(chapter_number)
    audio_url = verse_data['audio']['url']
    jumlah = quiz.get_glyph_image_from_verse_key(verse_key)
    
    correct_answer = quiz.get_chapter_name_from_verse_key(verse_key)

    invalid_answers = []
    invalid_sequence = [
        x for x in range(chapter_number - 4, chapter_number + 4)
        if x != chapter_number
    ]

    for i in invalid_sequence:
        if i > 1 and i < 115:
            invalid_answers.append(quiz.get_chapter_name_from_verse_key(i))
    choices = random.sample(
        random.sample(invalid_answers, 3) + [correct_answer], 4)
    ans_index = choices.index(correct_answer)
    user_ans = ""

    if tipe == 'audio':
        async with ctx.typing():
            voice_channel.play(
                discord.FFmpegPCMAudio(executable="ffmpeg",
                                       source=audio_url,
                                       **FFMPEG_OPTIONS))
            await ctx.send(
                f"Listen, that audio is from which surah? \n A. {choices[0]}\n B. {choices[1]}\n C. {choices[2]}\n D. {choices[3]}\n or type `stop` to stop the quiz"
            )
    elif tipe == 'text':
        for i in range(jumlah + 1):
            await ctx.send(file=discord.File(f'img/glyph{i}.png'))
        await ctx.send(
            f"> Verse above is from which surah? \n A. {choices[0]}\n B. {choices[1]}\n C. {choices[2]}\n D. {choices[3]}\n or type `stop` to stop the quiz"
        )

    def is_correct(m):
        return m.author == ctx.author

    try:
        user_ans = await bot.wait_for("message", check=is_correct, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("oops timeout!")

    if user_ans.content.lower() == ['a', 'b', 'c', 'd'][ans_index].lower():
        await ctx.send("Correct!")
        if tipe == 'audio':
            if voice_channel.is_playing():
                await voice_channel.stop()
        await quran_quiz_0(ctx, tipe, juz, qari)
    elif user_ans.content.lower() == "stop".lower():
        await ctx.send("Stopped!")
    else:
        await ctx.send(f"Wrong! {correct_answer}")
        if tipe == 'audio':
            if voice_channel.is_playing():
                await voice_channel.stop()
        await quran_quiz_0(ctx, tipe, juz, qari)


@bot.command(
    name='quran.quiz.1',
    help=
    'To play a random verse from the Quran and ask the user to guess the next verse'
)
async def quran_quiz_1(ctx, tipe, juz=30, qari=7):
    server = ctx.message.guild
    voice_channel = server.voice_client

    verse_data = quiz.get_random_verse_data_from_juz(juz, qari)
    verse_key = verse_data['verse_key']
    chapter_number = verse_key.split(':')[0]
    verse_number = verse_key.split(':')[1]
    verse_number = int(verse_number) + 1
    audio_url = verse_data['audio']['url']
    wrapper_soal = quiz.get_glyph_image_from_verse_key(f"{chapter_number}:{verse_number - 1}", filename='soal')
    wrapper_correct = quiz.get_glyph_image_from_verse_key(f"{chapter_number}:{verse_number}", filename='benar')
    
    invalid_sequence = [
        x for x in range(verse_number - 4, verse_number + 4)
        if x != verse_number and x != verse_number - 1
    ]

    for i in invalid_sequence:
        try:
            wrapper_wrong = quiz.get_glyph_image_from_verse_key(f"{chapter_number}:{i}", filename='salah')
            break
        except:
            pass

    prob = random.randint(1, 2)

    if prob == 1:
        choice = [wrapper_wrong, "salah"]
        ans = 'b'
    else:
        choice = [wrapper_correct, "benar"]
        ans = 'a'

    user_ans = ""

    if tipe == 'audio':
        async with ctx.typing():
            voice_channel.play(
                discord.FFmpegPCMAudio(executable="ffmpeg",
                                       source=audio_url,
                                       **FFMPEG_OPTIONS))
            await ctx.send("Dengarkan, ayat dibawah terletak setelah ayat yang didengar.")
            
            for i in range(choice[0] + 1):
                await ctx.send(file=discord.File(f'img/{choice[1]}{i}.png'))
                
            await ctx.send("A. Benar\nB. Salah\nor type `stop` to stop the quiz")
            
    elif tipe == 'text':
        for i in range(wrapper_soal + 1):
            await ctx.send(file=discord.File(f'img/soal{i}.png'))
        
        await ctx.send("lanjutannya adalah")
        
        for i in range(choice[0] + 1):
            await ctx.send(file=discord.File(f'img/{choice[1]}{i}.png'))
            
        await ctx.send("A. Benar\nB. Salah\nor type `stop` to stop the quiz")

    def is_correct(m):
        return m.author == ctx.author

    try:
        user_ans = await bot.wait_for("message", check=is_correct, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("oops timeout!")

    if user_ans.content.lower() == ans.lower():
        await ctx.send("Correct!")
        if tipe == 'audio':
            if voice_channel.is_playing():
                await voice_channel.stop()
        await quran_quiz_1(ctx, tipe, juz, qari)
    elif user_ans.content.lower() == "stop".lower():
        await ctx.send("Stopped!")
    else:
        await ctx.send("Wrong!")
        if tipe == 'audio':
            if voice_channel.is_playing():
                await voice_channel.stop()
        await quran_quiz_1(ctx, tipe, juz, qari)
    
@bot.command(
    name='quran.quiz.2',
    help=
    'To play a random verse from the Quran and ask the user to guess the next verse'
)
async def quran_quiz_2(ctx, tipe, chapter=1, qari=7):
    server = ctx.message.guild
    voice_channel = server.voice_client

    verse_data = quiz.get_random_verse_data_from_chapter(chapter, qari)
    verse_key = verse_data['verse_key']
    chapter_number = verse_key.split(':')[0]
    verse_number = verse_key.split(':')[1]
    verse_number = int(verse_number) + 1
    audio_url = verse_data['audio']['url']
    wrapper_soal = quiz.get_glyph_image_from_verse_key(f"{chapter_number}:{verse_number - 1}", filename='soal')
    wrapper_correct = quiz.get_glyph_image_from_verse_key(f"{chapter_number}:{verse_number}", filename='benar')
    
    invalid_sequence = [
        x for x in range(verse_number - 2, verse_number + 2)
        if x != verse_number and x != verse_number - 1
    ]

    for i in invalid_sequence:
        try:
            wrapper_wrong = quiz.get_glyph_image_from_verse_key(f"{chapter_number}:{i}", filename='salah')
            break
        except:
            pass

    prob = random.randint(1, 2)

    if prob == 1:
        choice = [wrapper_wrong, "salah"]
        ans = 'b'
    else:
        choice = [wrapper_correct, "benar"]
        ans = 'a'

    user_ans = ""

    if tipe == 'audio':
        async with ctx.typing():
            voice_channel.play(
                discord.FFmpegPCMAudio(executable="ffmpeg",
                                       source=audio_url,
                                       **FFMPEG_OPTIONS))
            await ctx.send("Dengarkan, ayat dibawah terletak setelah ayat yang didengar.")
            
            for i in range(choice[0] + 1):
                await ctx.send(file=discord.File(f'img/{choice[1]}{i}.png'))
                
            await ctx.send("A. Benar\nB. Salah\nor type `stop` to stop the quiz")
            
    elif tipe == 'text':
        for i in range(wrapper_soal + 1):
            await ctx.send(file=discord.File(f'img/soal{i}.png'))
        
        await ctx.send("lanjutannya adalah")
        
        for i in range(choice[0] + 1):
            await ctx.send(file=discord.File(f'img/{choice[1]}{i}.png'))
            
        await ctx.send("A. Benar\nB. Salah\nor type `stop` to stop the quiz")

    def is_correct(m):
        return m.author == ctx.author

    try:
        user_ans = await bot.wait_for("message", check=is_correct, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("oops timeout!")

    if user_ans.content.lower() == ans.lower():
        await ctx.send("Correct!")
        if tipe == 'audio':
            if voice_channel.is_playing():
                await voice_channel.stop()
        await quran_quiz_2(ctx, tipe, chapter, qari)
    elif user_ans.content.lower() == "stop".lower():
        await ctx.send("Stopped!")
    else:
        await ctx.send("Wrong!")
        if tipe == 'audio':
            if voice_channel.is_playing():
                await voice_channel.stop()
        await quran_quiz_2(ctx, tipe, chapter, qari)
        
@bot.command(
    name='quran.quiz.3',
    help=
    'To play a random verse from the Quran and ask the user to guess the next verse'
)
async def quran_quiz_3(ctx, chapter=1, qari=7):
    server = ctx.message.guild
    voice_channel = server.voice_client

    verse_data = quiz.get_random_verse_data_from_chapter(chapter, qari)
    verse_key = verse_data['verse_key']
    chapter_number = verse_key.split(':')[0]
    verse_number = verse_key.split(':')[1]
    verse_number = int(verse_number) + 1
    audio_url = verse_data['audio']['url']
    wrapper_soal, ans = quiz.get_uncompleted_glyph_image_from_verse_key(f"{chapter_number}:{verse_number - 1}", filename='soal')

    user_ans = ""

    # if tipe == 'audio':
    #     async with ctx.typing():
    #         voice_channel.play(
    #             discord.FFmpegPCMAudio(executable="ffmpeg",
    #                                    source=audio_url,
    #                                    **FFMPEG_OPTIONS))
    #         await ctx.send("Dengarkan, berapakah kata yang hilang di ayat tersebut?")

    #         await ctx.send("type a number or type `stop` to stop the quiz")
            
    # elif tipe == 'text':
    #     for i in range(wrapper_soal + 1):
    #         await ctx.send(file=discord.File(f'img/soal{i}.png'))
        
    #     await ctx.send("lanjutannya adalah")
        
    #     for i in range(choice[0] + 1):
    #         await ctx.send(file=discord.File(f'img/{choice[1]}{i}.png'))
            
    #     await ctx.send("A. Benar\nB. Salah\nor type `stop` to stop the quiz")

    for i in range(wrapper_soal + 1):
        await ctx.send(file=discord.File(f'img/soal{i}.png'))
    
    await ctx.send("Berapakah kata yang hilang di ayat tersebut?")
    await ctx.send("type a number or type `stop` to stop the quiz")
    
    def is_correct(m):
        return m.author == ctx.author

    try:
        user_ans = await bot.wait_for("message", check=is_correct, timeout=120)
    except asyncio.TimeoutError:
        await ctx.send("oops timeout!")

    if str(user_ans.content) == str(ans):
        response = discord.Embed(title="Correct!", color=0x00ff00)
        response.add_field(name="developer note", value="```belum bisa dibedakan antara tanda waqaf dan kata dalam qur'an, sehingga bisa saja yang dihilangkan adalah tanda waqafnya.```", inline=False)
        response.set_footer(text="missing word(s) attached.")
        img = discord.File('img/soalcropped.png', filename='soalcropped.png')
        response.set_image(url="attachment://soalcropped.png")
        await ctx.send(embed=response, file=img)
        # if tipe == 'audio':
        #     if voice_channel.is_playing():
        #         await voice_channel.stop()
        await quran_quiz_3(ctx, chapter, qari)
    elif user_ans.content.lower() == "stop".lower():
        await ctx.send("Stopped!")
    else:
        response = discord.Embed(title="Wrong!", description=f"```correct: {ans}```", color=0x00ff00)
        response.add_field(name="developer note", value="```belum bisa dibedakan antara tanda waqaf dan kata dalam qur'an, sehingga bisa saja yang dihilangkan adalah tanda waqafnya.```", inline=False)
        response.set_footer(text="missing word(s) attached.")
        img = discord.File('img/soalcropped.png', filename='soalcropped.png')
        response.set_image(url="attachment://soalcropped.png")
        await ctx.send(embed=response, file=img)
        # if tipe == 'audio':
        #     if voice_channel.is_playing():
        #         await voice_channel.stop()
        await quran_quiz_3(ctx, chapter, qari)

bot.run(os.environ.get('BOT_TOKEN'))  
# Don't reveal your bot token, regenerate it asap if you do