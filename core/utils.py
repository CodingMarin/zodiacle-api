import requests
import unicodedata
from bs4 import BeautifulSoup

def get_horoscope_by_day(zodiac_sign: str, day: str):
    base_url = "https://www.horoscopo.com/horoscopos/general-"

    if day == 'hoy':
        url = f"{base_url}diaria-{zodiac_sign}"
    elif day == 'manana':
        url = f"{base_url}diaria-manana-{zodiac_sign}"
    elif day == 'semanal':
        url = f"{base_url}semanal-{zodiac_sign}"
    else:
        raise Exception("Parametro incorrecto")

    res = requests.get(url)

    if res.status_code != 200:
        raise Exception(f"Failed to retrieve horoscope. Status code: {res.status_code}")

    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'horoscope-box'})

    if data and data.p:
        return data.p.text
    else:
        raise Exception("Horórscopo no encontrado")


def get_horoscope_by_week(zodiac_sign: str):
    base_url = "https://www.horoscopo.com/horoscopos/general-semanal-"

    res = requests.get(
        f"{base_url}{zodiac_sign}")

    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'horoscope-box'})

    if data and data.p:
        return data.p.text
    else:
        raise Exception("Horórscopo no encontrado")


def get_horoscope_by_month(zodiac_sign: str):
    base_url = "https://www.horoscopo.com/horoscopos/mensual-"

    res = requests.get(
        f"{base_url}{zodiac_sign}")

    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'horoscope-box'})

    if data and data.p:
        return data.p.text
    else:
        raise Exception("Horórscopo no encontrado")

def get_compatibility_sign(zodiac_sign_a: str, zodiac_sign_b: str):
    base_url = "https://www.lavanguardia.com/horoscopo/compatibilidad-signos-zodiaco/"

    res = requests.get(
        f"{base_url}{zodiac_sign_a}-{zodiac_sign_b}")

    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find('div', attrs={'class': 'text-block'})

    if data and data.p:
        return data.p.text
    else:
        raise Exception("Ups! hubo un problema...")

def normalize_string(input_string):
    lower_case_string = input_string.lower()
    normalized_string = unicodedata.normalize('NFKD', lower_case_string)
    no_accent_string = ''.join(c for c in normalized_string if not unicodedata.combining(c))

    return no_accent_string