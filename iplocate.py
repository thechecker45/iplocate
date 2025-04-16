import requests
import webbrowser
import string
import random
import time
from datetime import datetime
from os import system, name
from colorama import init, Fore, Style

banner = (Fore.RED + r"""

._____________  .____    ________  _________     ___________________________
|   \______   \ |    |   \_____  \ \_   ___ \   /  _  \__    ___/\_   _____/
|   ||     ___/ |    |    /   |   \/    \  \/  /  /_\  \|    |    |    __)_ 
|   ||    |     |    |___/    |    \     \____/    |    \    |    |        \
|___||____|     |_______ \_______  /\______  /\____|__  /____|   /_______  /
                        \/       \/        \/         \/                 \/ 
   .__________________________________________________________.
   |                TheChecker & Kuvvetmira                   |
   |       guns.lol/thechecker & guns.lol/kuvvetmira          |
   |__________________________________________________________|
          
""")

init(autoreset=True)

TOKEN = "8420333b445024"

def zaman_bilgisi():
    return datetime.now().strftime("[%d.%m.%Y %H:%M:%S]")

def yaz(mesaj, renk=Fore.WHITE):
    print(zaman_bilgisi(), renk + mesaj + Style.RESET_ALL)

def ip_bilgilerini_al(ip_adresi, token):
    url = f"https://ipinfo.io/{ip_adresi}/json?token={token}"
    cevap = requests.get(url)
    return cevap.json()

def ip_konumunu_al(ip_adresi):
    url = f"https://ipinfo.io/{ip_adresi}/json?token={TOKEN}"
    cevap = requests.get(url)
    veri = cevap.json()

    loc = veri.get("loc")
    if loc:
        return loc.split(",")
    else:
        return None, None

def haritada_goster(lat, lon):
    maps_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}"
    webbrowser.open_new_tab(maps_url)

def rastgele_sifre_olustur(uzunluk=14):
    karakterler = string.ascii_lowercase + string.digits
    return ''.join(random.choice(karakterler) for _ in range(uzunluk))

def ip_gecerli_mi(ip):
    allowed = set("0123456789.qQ")
    return all(char in allowed for char in ip)

def ekran_temizle():
    system("cls" if name == "nt" else "clear")
    
while True:
    print(banner)
    ip_adresi = input(Fore.RESET + "IP adresini girin\n> ").strip()

    if ip_adresi.lower() == "q":
        yaz("Programdan çıkılıyor...", Fore.LIGHTRED_EX)
        break

    if not ip_gecerli_mi(ip_adresi):
        yaz("❌ Geçersiz karakter girdiniz. Sadece sayılar, nokta ve q/Q geçerli.", Fore.RED)
        continue

    try:
        bilgiler = ip_bilgilerini_al(ip_adresi, TOKEN)
        lat, lon = ip_konumunu_al(ip_adresi)

        if not lat or not lon:
            yaz("⚠️ Konum bilgisi alınamadı. IP geçersiz olabilir.", Fore.YELLOW)
            continue

        yaz("Yeni API KEY oluşturuluyor...", Fore.CYAN)
        time.sleep(1)
        yeni_sifre = rastgele_sifre_olustur()
        yaz(f"Oluşturulan API KEY: {yeni_sifre}", Fore.GREEN)

        yaz("--- IP Bilgileri ---", Fore.BLUE)
        yaz(f"IP Adresi: {ip_adresi}", Fore.WHITE)
        yaz("Konum: " + f"{bilgiler.get('city')}, {bilgiler.get('region')}, {bilgiler.get('country')}", Fore.WHITE)
        yaz("Posta Kodu: " + bilgiler.get("postal"), Fore.WHITE)
        yaz("Zaman Dilimi: " + bilgiler.get("timezone"), Fore.WHITE)
        yaz("Kullanılan ISP: " + bilgiler.get("org"), Fore.WHITE)

        yaz("--- Konum Bilgileri ---", Fore.BLUE)
        yaz("Haritadaki Konum URL: " + f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}", Fore.CYAN)
        yaz("LAT: " + lat, Fore.WHITE)
        yaz("LON: " + lon, Fore.WHITE)

        haritada_goster(lat, lon)

        input(f"\n{zaman_bilgisi()} {Fore.LIGHTYELLOW_EX}Devam etmek için Enter'a bas")
        ekran_temizle()

    except Exception as e:
        yaz(f"Hata oluştu: {e}", Fore.RED)
