import requests
import random, textwrap
from PIL import Image, ImageFont

def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]

def remove_random_character(phrase, n_remove):
    placeholder = random.sample(range(0, len(phrase)), n_remove)
    for num in placeholder:
        phrase = phrase[:num] + '_' + phrase[num + 1:]
    return phrase, sorted(placeholder, reverse=True)

# verse_key sections
def get_random_verse_key():
    url = "https://api.quran.com/api/v4/verses/random"
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers)
    verse_key = response.json()['verse']['verse_key']
    return verse_key

def get_audio(reciter : int, verse_key):
    url = f"https://api.quran.com/api/v4/recitations/{reciter}/by_ayah/{verse_key}"
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers)
    audio = response.json()['audio_files'][0]['url']
    
    if str(audio).startswith("mirrors.quranicaudio.com"):
        return "https://" + str(audio)
    else:
        return "https://verses.quran.com/" + str(audio)
    
def get_verse_glyph(verse_key, style="uthmani"):
    url = f"https://api.quran.com/api/v4/quran/verses/{style}"
    querystring = {"verse_key":verse_key}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()['verses'][0][f'text_{style}']

def get_chapter_name_from_verse_key(verse_key):
    id = str(verse_key).split(':')[0]
    url = f"https://api.quran.com/api/v4/chapters/{id}"
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers)
    return response.json()['chapter']['name_simple']
()
# verse_key by juz section
def get_random_verse_data_from_juz(juz, qari):
    url = f"https://api.quran.com/api/v4/verses/by_juz/{juz}"
    querystring = {"words":"false", "per_page":"1"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    max_page = response.json()['pagination']['total_pages']
    
    querystring = {"words":"false","audio":qari, "page":random.randint(1, max_page), "per_page":"1"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    verse_data = response.json()["verses"][0]
    
    if verse_data["audio"]['url'].startswith("mirrors.quranicaudio.com"):
        verse_data["audio"]['url'] = "https://" + verse_data["audio"]['url']
    elif verse_data["audio"]['url'].startswith("//mirrors.quranicaudio.com"):
        verse_data["audio"]['url'] = verse_data["audio"]['url'].replace("//", "https://")
    else:
        verse_data["audio"]['url'] = "https://verses.quran.com/" + verse_data["audio"]['url']

    return verse_data

def get_random_verse_data_from_chapter(chapter, qari):
    url = f"https://api.quran.com/api/v4/verses/by_chapter/{chapter}"
    querystring = {"words":"false", "per_page":"1"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    max_page = response.json()['pagination']['total_pages']
    
    querystring = {"words":"false", "audio":qari, "page":random.randint(1, max_page), "per_page":"1"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    verse_data = response.json()["verses"][0]
    
    if verse_data["audio"]['url'].startswith("mirrors.quranicaudio.com"):
        verse_data["audio"]['url'] = "https://" + verse_data["audio"]['url']
    elif verse_data["audio"]['url'].startswith("//mirrors.quranicaudio.com"):
        verse_data["audio"]['url'] = verse_data["audio"]['url'].replace("//", "https://")
    else:
        verse_data["audio"]['url'] = "https://verses.quran.com/" + verse_data["audio"]['url']

    return verse_data

def get_glyph_image_from_verse_key(verse_key, filename="glyph", style="QFC", font_size=40, color=(255, 255, 255, 255)):
    url = "https://api.quran.com/api/v4/quran/verses/code_v2"
    querystring = {"verse_key":verse_key}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    
    text = response.json()["verses"][0]['code_v2'][:-1]
    text = textwrap.wrap(text, 12)
    
    page_number = response.json()["verses"][0]['v2_page']
    
    if page_number >= 100:
        pass
    elif page_number >= 10:
        page_number = "0" + str(page_number)
    elif page_number < 10:
        page_number = "00" + str(page_number)
        
    font_size = 30
    try:
        font_filepath = f"https://cdn.rawgit.com/mustafa0x/qpc-fonts/f93bf5f3/mushaf-v2/QCF2{page_number}.ttf"
        font = ImageFont.truetype(font_filepath, size=font_size)
    except:
        font_filepath = f"mushaf-v2/QCF2{page_number}.ttf"
        font = ImageFont.truetype(font_filepath, size=font_size)
        
    color = (255, 255, 255, 255)

    for i, j in enumerate(text):
        mask_image = font.getmask(j[::-1], "L")
        img = Image.new("RGBA", mask_image.size)
        img.im.paste(color, (0, 0) + mask_image.size, mask_image)
        img.save(f"img/{filename}{i}.png")
        
    return i

def get_glyph_image_from_code(page_number, code, filename="glyph", color=(255, 255, 255, 255)):
    
    if page_number >= 100:
        pass
    elif page_number >= 10:
        page_number = "0" + str(page_number)
    elif page_number < 10:
        page_number = "00" + str(page_number)
        
    font_size = 30
    try:
        font_filepath = f"https://cdn.rawgit.com/mustafa0x/qpc-fonts/f93bf5f3/mushaf-v2/QCF2{page_number}.ttf"
        font = ImageFont.truetype(font_filepath, size=font_size)
    except:
        font_filepath = f"mushaf-v2/QCF2{page_number}.ttf"
        font = ImageFont.truetype(font_filepath, size=font_size)
        
    color = (255, 255, 255, 255)

    mask_image = font.getmask(code, "L")
    img = Image.new("RGBA", mask_image.size)
    img.im.paste(color, (0, 0) + mask_image.size, mask_image)
    img.save(f"img/{filename}.png")

def get_uncompleted_glyph_image_from_verse_key(verse_key, filename="glyph", style="QFC", font_size=40, color=(255, 255, 255, 255)):
    url = "https://api.quran.com/api/v4/quran/verses/code_v2"
    querystring = {"verse_key":verse_key}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    
    text = response.json()["verses"][0]['code_v2'][:-1].replace(" ", "")
    
    randomizer = random.randint(1, int(len(text)/4) if len(text) > 4 else 2)
    
    text2 = text
    
    text, index_hilang = remove_random_character(text, randomizer)
    text = textwrap.wrap(text, 8)
    
    text3 = ""
    for i in index_hilang:
        text3 += text2[i]
    
    page_number = response.json()["verses"][0]['v2_page']
    
    if page_number >= 100:
        pass
    elif page_number >= 10:
        page_number = "0" + str(page_number)
    elif page_number < 10:
        page_number = "00" + str(page_number)
        
    font_size = 30
    try:
        font_filepath = f"https://cdn.rawgit.com/mustafa0x/qpc-fonts/f93bf5f3/mushaf-v2/QCF2{page_number}.ttf"
        font = ImageFont.truetype(font_filepath, size=font_size)
    except:
        font_filepath = f"mushaf-v2/QCF2{page_number}.ttf"
        font = ImageFont.truetype(font_filepath, size=font_size)
        
    color = (255, 255, 255, 255)

    for i, j in enumerate(text):
        mask_image = font.getmask(j[::-1], "L")
        img = Image.new("RGBA", mask_image.size)
        img.im.paste(color, (0, 0) + mask_image.size, mask_image)
        img.save(f"img/{filename}{i}.png")
    
    mask_image = font.getmask(text3, "L")
    img = Image.new("RGBA", mask_image.size)
    img.im.paste(color, (0, 0) + mask_image.size, mask_image)
    img.save(f"img/{filename}cropped.png")
        
    return i, randomizer, sorted(index_hilang, reverse=True)

def get_translation_from_verse_key(verse_key, language='id'):
    url = f"https://api.quran.com/api/v4/verses/by_key/{verse_key}"
    querystring = {"language":language, "words":"true","word_fields":"code_v2"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    return response.json()['verse']['words']

# print(get_random_verse_data_from_juz(30, 12))

# def get_all_verse_key_by_juz(juz):
#     url = f"https://api.quran.com/api/v4/verses/by_juz/{juz}"
#     headers = {"Content-Type": "application/json"}
#     response = requests.request("GET", url, headers=headers)
#     verses_keys = response.json()
#     return verses_keys

# def get_verse_sequence_by_juz(juz, seq : int):
#     data = get_all_verse_key_by_juz(juz)
#     sample = random.sample(range(0, data['pagination']['total_records'] + 1), seq)
#     verses_keys = []
#     for i in sample:
#         verses_keys.append(data['verses'][i]['verse_key'])
    
#     return verses_keys
        
                           
# print(get_all_verse_key_by_juz(30)['verses'][0]['verse_key'])
# print(get_all_verse_key_by_juz(30)['verses'][random.randint(1, )]['verse_key'])
# print(get_verse_sequence_by_juz(30, 10))