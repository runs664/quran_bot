import requests

# audio sections
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
    return "https://verses.quran.com/" + str(audio)

print(get_audio(7, get_random_verse_key()))