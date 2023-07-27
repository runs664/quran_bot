import requests
import random

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