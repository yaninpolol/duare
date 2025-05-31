from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import re # Import regex for more flexible URL matching

options = {
    'proxy': {
        'http': 'http://8ab4e23e37d62bc26e35__cr.ar:3efeffa0d3f66c71@gw.dataimpulse.com:10203',
        'https': 'https://8ab4e23e37d62bc26e35__cr.ar:3efeffa0d3f66c71@gw.dataimpulse.com:10203',
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
chrome_options.add_argument("--disable-features=OptimizationHints,OptimizationTargetPrediction,SafeBrowsing")
chrome_options.add_argument("--disable-features=Translate,InterestCohortFeaturePolicy")
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-ipc-flooding-protection")
chrome_options.add_argument("--disable-site-specific-hsts-bypass")
chrome_options.add_argument("--disable-hang-monitor")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-prompt-on-repost")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# --- Akhir argumen tambahan ---

driver = webdriver.Chrome(seleniumwire_options=options, options=chrome_options)

try:
    driver.get("https://sepolia-faucet.pk910.de/#/mine/04f47d26-b2f8-4919-8227-d4d0767bb7a2")

    # --- Metode 1: Memeriksa semua permintaan yang telah dibuat ---
    print("\nMemeriksa semua permintaan jaringan yang telah dibuat:")
    found_unwanted_request = False
    for request in driver.requests:
        if "optimizationguide-pa.googleapis.com" in request.url:
            print(f"  [DITEMUKAN] Permintaan yang tidak diinginkan: {request.url}")
            found_unwanted_request = True
            break # Hentikan setelah menemukan satu
    if not found_unwanted_request:
        print("  Tidak ada permintaan ke 'optimizationguide-pa.googleapis.com' yang terdeteksi sejauh ini.")

    # --- Metode 2: Menggunakan driver.wait_for_request() untuk memastikan TIDAK ADA permintaan ---
    # Ini akan menunggu selama 5 detik. Jika permintaan ke URL ini muncul dalam 5 detik,
    # itu akan menangkapnya. Jika tidak, itu akan timeout, yang merupakan hasil yang kita inginkan.
    print("\nMencoba menunggu permintaan ke 'optimizationguide-pa.googleapis.com' (maks 5 detik)...")
    try:
        # Gunakan regex untuk pencocokan yang lebih fleksibel jika diperlukan
        # request = driver.wait_for_request('.*optimizationguide-pa\.googleapis\.com.*', timeout=5)
        request = driver.wait_for_request('optimizationguide-pa.googleapis.com', timeout=5)
        print(f"  [PERINGATAN] Permintaan ke 'optimizationguide-pa.googleapis.com' terdeteksi: {request.url}")
    except Exception as e:
        print(f"  Tidak ada permintaan ke 'optimizationguide-pa.googleapis.com' yang terdeteksi dalam 5 detik. (Pesan: {e})")


    print("\nMenunggu mining selesai (50 detik)...")
    time.sleep(50000) # WAKTU MENUNGGU MINING SELESAI

    div_element = driver.find_element(By.CLASS_NAME, "col-3")
    content_text = div_element.text
    print("\nKonten dari elemen div:")
    print(content_text)

    print("\nMenunggu 15 detik sebelum menutup browser...")
    time.sleep(15000) # WAKTU MENUNGGU MINING SELESAI (jika ada proses lain setelah mendapatkan teks)

finally:
    # Tutup browser
    driver.quit()
    print("\nBrowser ditutup.")
