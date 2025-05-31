from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

options = {
    'proxy': {
        'http': 'http://8ab4e23e37d62bc26e35__cr.tn:3efeffa0d3f66c71@gw.dataimpulse.com:10203',
        'https': 'https://8ab4e23e37d62bc26e35__cr.tn:3efeffa0d3f66c71@gw.dataimpulse.com:10203',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--verbose")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--window-size=1920, 1200")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument("--disable-client-side-phishing-detection")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-features=NetworkPrediction")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--metrics-recording-only")
chrome_options.add_argument("--safebrowsing-disable-auto-update")
chrome_options.add_argument("--disable-component-update")
chrome_options.add_argument("--disable-domain-reliability")

# --- Argumen tambahan untuk memblokir koneksi ke Google Optimization Guide ---
# Menonaktifkan fitur-fitur yang terkait dengan Optimization Guide dan sejenisnya
chrome_options.add_argument("--disable-features=OptimizationHints,OptimizationTargetPrediction,SafeBrowsing")
chrome_options.add_argument("--disable-features=Translate,InterestCohortFeaturePolicy")
chrome_options.add_argument("--disable-background-timer-throttling") # Mencegah throttling timer di latar belakang
chrome_options.add_argument("--disable-ipc-flooding-protection") # Melindungi dari serangan flooding IPC
chrome_options.add_argument("--disable-site-specific-hsts-bypass") # Menonaktifkan bypass HSTS
chrome_options.add_argument("--disable-hang-monitor") # Menonaktifkan monitor hang
chrome_options.add_argument("--disable-popup-blocking") # Menonaktifkan pemblokiran popup
chrome_options.add_argument("--disable-prompt-on-repost") # Menonaktifkan prompt saat memposting ulang
chrome_options.add_argument("--disable-web-security") # Menonaktifkan keamanan web (gunakan dengan hati-hati)
chrome_options.add_argument("--no-first-run") # Mencegah menjalankan proses 'first run'
chrome_options.add_argument("--no-default-browser-check") # Mencegah pemeriksaan browser default
chrome_options.add_argument("--disable-blink-features=AutomationControlled") # Menyembunyikan bahwa browser dikontrol oleh otomatisasi
# --- Akhir argumen tambahan ---

driver = webdriver.Chrome(seleniumwire_options=options, options=chrome_options)

driver.get("https://sepolia-faucet.pk910.de/#/mine/a9e342c5-e299-479e-b6a4-541b0bc7a208")

# Anda mungkin ingin memeriksa permintaan jaringan di sini untuk memastikan optimizationguide-pa.googleapis.com tidak muncul
# for request in driver.requests:
#     if "optimizationguide-pa.googleapis.com" in request.url:
#         print(f"Detected unwanted request: {request.url}")

print("Menunggu mining selesai...")
time.sleep(50000) # WAKTU MENUNGGU MINING SELESAI

div_element = driver.find_element(By.CLASS_NAME, "col-3")
content_text = div_element.text
print("Konten dari elemen div:")
print(content_text)

print("Menunggu 15 detik sebelum menutup browser...")
time.sleep(15000) # WAKTU MENUNGGU MINING SELESAI (jika ada proses lain setelah mendapatkan teks)

# Tutup browser
driver.quit()
print("Browser ditutup.")
