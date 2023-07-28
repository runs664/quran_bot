import requests
import random, textwrap
from PIL import Image, ImageFont

def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]

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
    font_filepath = f"https://cdn.rawgit.com/mustafa0x/qpc-fonts/f93bf5f3/mushaf-v2/QCF2{page_number}.ttf"
    color = (255, 255, 255, 255)

    for i, j in enumerate(text):
        font = ImageFont.truetype(font_filepath, size=font_size)
        mask_image = font.getmask(j[::-1], "L")
        img = Image.new("RGBA", mask_image.size)
        img.im.paste(color, (0, 0) + mask_image.size, mask_image)
        img.save(f"img/{filename}{i}.png")
        
    return i

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