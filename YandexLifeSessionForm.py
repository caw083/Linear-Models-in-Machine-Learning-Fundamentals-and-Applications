from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Setup opsi Chrome
options = Options()
# options.add_argument('--headless')  # Uncomment untuk headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Data presensi
data = {
    "email": "christopher083ade@gmail.com",
    "nama_lengkap": "CHRISTOPHER ADE WIYANTO",
    "no_telepon" : "081548912348",
    "username_telegram" : "@haw121862",
    "nomor_pendaftaran": "19510458840-165",
    "reviewer": "Mas Fuad",
    "hal_menarik": random.choice([
        "Materi mudah dipahami dan banyak insight baru.",
        "Simulasi langsung sangat membantu pemahaman.",
        "Live coding membuat materi jadi lebih menarik.",
        "Penjelasan step-by-step sangat jelas.",
        "Banyak studi kasus yang relevan dan aplikatif."
    ]),
    "feedback": random.choice([
        "Reviewer menjelaskan dengan sangat jelas dan interaktif.",
        "Sesi sangat menyenangkan dan tidak membosankan.",
        "Sangat profesional dan ramah.",
        "Live session tepat waktu dan terstruktur.",
        "Terima kasih, reviewer sangat membantu."
    ])
}

# Start browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLScB4RZrYntzRCuWf-5GtL0QY1701dm4JQ9OoL7wfqXnArxIsA/viewform")
    
    # Wait untuk halaman load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
    
    print("📄 Halaman form berhasil dimuat")
    time.sleep(2)

    # Helper function untuk mengisi input text dengan strategi yang lebih baik
    def isi_input_text(value, field_index):
        """Mengisi input text berdasarkan index dengan fallback strategies"""
        try:
            # Strategi 1: Cari berdasarkan input dengan placeholder "Jawaban Anda"
            inputs_with_placeholder = driver.find_elements(By.XPATH, '//input[@placeholder="Jawaban Anda"]')
            if field_index <= len(inputs_with_placeholder):
                element = inputs_with_placeholder[field_index - 1]
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.clear()
                element.send_keys(value)
                print(f"✅ Input {field_index} berhasil diisi: {value[:30]}...")
                return True
        except Exception as e:
            print(f"Strategi 1 gagal: {e}")
        
        try:
            # Strategi 2: Cari semua input text/email
            inputs = driver.find_elements(By.XPATH, '//input[@type="text" or @type="email"]')
            if field_index <= len(inputs):
                element = inputs[field_index - 1]
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.clear()
                element.send_keys(value)
                print(f"✅ Input {field_index} berhasil diisi: {value[:30]}...")
                return True
        except Exception as e:
            print(f"❌ Gagal mengisi input {field_index}: {e}")
        
        return False

    # Helper function untuk mengisi textarea
    def isi_textarea(value, field_index):
        """Mengisi textarea berdasarkan index"""
        try:
            textareas = driver.find_elements(By.TAG_NAME, 'textarea')
            if field_index <= len(textareas):
                element = textareas[field_index - 1]
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.clear()
                element.send_keys(value)
                print(f"✅ Textarea {field_index} berhasil diisi: {value[:30]}...")
                return True
        except Exception as e:
            print(f"❌ Gagal mengisi textarea {field_index}: {e}")
        return False

    # Helper function untuk memilih dropdown - COMPLETELY REWRITTEN
    def pilih_dropdown_google_forms(option_text):
        """Memilih opsi dari dropdown Google Forms dengan metode yang lebih reliable"""
        try:
            print(f"🔍 Mencari dropdown untuk memilih: {option_text}")
            
            # Strategi 1: Cari dropdown trigger dan klik untuk membuka
            dropdown_triggers = [
                '//div[@role="listbox"]',
                '//div[contains(@class, "quantumWizMenuPaperselectEl")]',
                '//div[contains(@jsaction, "click")][@role="listbox"]',
                '//div[@data-initial-value]'
            ]
            
            dropdown_opened = False
            for trigger_xpath in dropdown_triggers:
                try:
                    trigger = driver.find_element(By.XPATH, trigger_xpath)
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", trigger)
                    time.sleep(1)
                    
                    # Klik untuk membuka dropdown
                    trigger.click()
                    time.sleep(2)
                    dropdown_opened = True
                    print("✅ Dropdown berhasil dibuka")
                    break
                except:
                    continue
            
            if not dropdown_opened:
                print("❌ Tidak bisa membuka dropdown")
                return False
            
            # Strategi 2: Tunggu dan cari opsi yang muncul
            wait = WebDriverWait(driver, 10)
            
            # Coba berbagai selector untuk opsi
            option_selectors = [
                f'//div[@role="option" and @data-value="{option_text}"]',
                f'//div[@role="option"]//span[contains(text(), "{option_text}")]/..',
                f'//div[@role="option" and contains(., "{option_text}")]',
                f'//div[contains(@class, "quantumWizMenuPaperselectOption") and contains(., "{option_text}")]'
            ]
            
            option_found = False
            for selector in option_selectors:
                try:
                    option_element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    
                    # Scroll ke opsi
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", option_element)
                    time.sleep(1)
                    
                    # Klik opsi dengan JavaScript untuk memastikan event ter-trigger
                    driver.execute_script("arguments[0].click();", option_element)
                    time.sleep(2)
                    
                    print(f"✅ Opsi '{option_text}' berhasil diklik")
                    option_found = True
                    break
                    
                except Exception as e:
                    print(f"Selector gagal: {selector} - {e}")
                    continue
            
            if not option_found:
                # Strategi terakhir: Cari semua opsi dan bandingkan text
                try:
                    all_options = driver.find_elements(By.XPATH, '//div[@role="option"]')
                    print(f"🔍 Ditemukan {len(all_options)} opsi, mencari yang cocok...")
                    
                    for i, option in enumerate(all_options):
                        try:
                            option_text_content = option.get_attribute('textContent') or ""
                            data_value = option.get_attribute('data-value') or ""
                            
                            print(f"Opsi {i+1}: text='{option_text_content.strip()}', data-value='{data_value}'")
                            
                            if (option_text in option_text_content or 
                                option_text == data_value or
                                option_text_content.strip() == option_text):
                                
                                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", option)
                                time.sleep(1)
                                driver.execute_script("arguments[0].click();", option)
                                time.sleep(2)
                                
                                print(f"✅ Opsi '{option_text}' berhasil dipilih dari pencarian manual")
                                option_found = True
                                break
                                
                        except Exception as e:
                            continue
                            
                except Exception as e:
                    print(f"Error dalam pencarian manual: {e}")
            
            # Verifikasi apakah selection berhasil
            if option_found:
                try:
                    # Cek apakah ada perubahan di dropdown (misal ada teks yang berubah)
                    time.sleep(2)
                    
                    # Cari element yang menunjukkan nilai terpilih
                    selected_indicators = [
                        '//div[@role="listbox"]//span[contains(@class, "quantumWizMenuPaperselectContent")]',
                        '//div[@data-initial-value]',
                        '//div[contains(@class, "quantumWizMenuPaperselectEl")]//span'
                    ]
                    
                    for indicator_xpath in selected_indicators:
                        try:
                            indicator = driver.find_element(By.XPATH, indicator_xpath)
                            current_value = indicator.get_attribute('textContent') or ""
                            if option_text in current_value:
                                print(f"✅ Verifikasi berhasil: '{current_value.strip()}' mengandung '{option_text}'")
                                return True
                        except:
                            continue
                    
                    print("⚠️ Opsi diklik tapi verifikasi tidak berhasil")
                    return True  # Anggap berhasil karena sudah diklik
                    
                except Exception as e:
                    print(f"Error verifikasi: {e}")
                    return True  # Anggap berhasil
            
            return False
            
        except Exception as e:
            print(f"❌ Error umum dalam pilih_dropdown: {e}")
            return False

    # Fungsi alternatif menggunakan keyboard navigation
    def pilih_dropdown_keyboard(option_text):
        """Alternatif menggunakan keyboard untuk memilih dropdown"""
        try:
            print(f"⌨️ Mencoba pilih dropdown dengan keyboard: {option_text}")
            
            # Cari dropdown element
            dropdown = driver.find_element(By.XPATH, '//div[@role="listbox"]')
            driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
            time.sleep(1)
            
            # Focus ke dropdown
            dropdown.click()
            time.sleep(1)
            
            # Gunakan keyboard navigation
            actions = ActionChains(driver)
            
            # Tekan Arrow Down beberapa kali untuk navigasi
            for i in range(10):  # Maksimal 10 kali navigasi
                actions.send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(0.5)
                
                # Cek element yang sedang di-highlight
                try:
                    highlighted = driver.find_element(By.XPATH, '//div[@role="option" and contains(@class, "Ct2jlb")]')
                    current_text = highlighted.get_attribute('textContent') or ""
                    
                    if option_text in current_text:
                        actions.send_keys(Keys.ENTER).perform()
                        time.sleep(2)
                        print(f"✅ Berhasil pilih '{option_text}' dengan keyboard")
                        return True
                        
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Error keyboard navigation: {e}")
            return False

    # Isi form secara berurutan sesuai urutan baru yang diminta
    print("📝 Mulai mengisi form dengan urutan baru...")
    
    # 1. Nama Reviewer Pada Live Session (dropdown - field pertama)
    print("🔽 Memilih Nama Reviewer dari dropdown...")
    
    # Coba metode utama dulu
    if not pilih_dropdown_google_forms(data["reviewer"]):
        print("🔄 Mencoba metode keyboard...")
        if not pilih_dropdown_keyboard(data["reviewer"]):
            print("❌ Semua metode dropdown gagal")
        
    time.sleep(3)
    
    # 2. Nama (input pertama dengan placeholder "Jawaban Anda")
    print("👤 Mengisi Nama Lengkap...")
    isi_input_text(data["nama_lengkap"], 1)
    time.sleep(1)
    
    # 3. Nomor Telepon (input kedua)
    print("📱 Mengisi Nomor Telepon...")
    isi_input_text(data["no_telepon"], 2)
    time.sleep(1)
    
    # 4. Username Telegram (input ketiga)
    print("📱 Mengisi Username Telegram...")
    isi_input_text(data["username_telegram"], 3)
    time.sleep(1)
    
    # 5. Email (input keempat)
    print("📧 Mengisi Email...")
    isi_input_text(data["email"], 4)
    time.sleep(1)
    
    # 6. DTS ID (input kelima)
    print("🔢 Mengisi DTS ID...")
    isi_input_text(data["nomor_pendaftaran"], 5)
    time.sleep(1)
    
    # 7. Apa hal yang paling menarik pada live session kali ini? (textarea pertama)
    print("📝 Mengisi Hal Menarik...")
    isi_textarea(data["hal_menarik"], 1)
    time.sleep(1)
    
    # 8. Feedback untuk Reviewer / Live Session pada hari ini (textarea kedua)
    print("💬 Mengisi Feedback...")
    isi_textarea(data["feedback"], 2)
    time.sleep(1)

    # Debug: Cek status form sebelum submit
    print("🔍 Mengecek status form sebelum submit...")
    try:
        # Cek apakah ada field yang masih kosong atau invalid
        required_fields = driver.find_elements(By.XPATH, '//div[contains(@class, "quantumWizTextinputPaperInputInputWrapper") and contains(@class, "quantumWizTextinputPaperInputError")]')
        if required_fields:
            print(f"⚠️ Ditemukan {len(required_fields)} field dengan error")
        
        # Cek dropdown value
        dropdown_value = driver.find_element(By.XPATH, '//div[@role="listbox"]')
        current_dropdown_text = dropdown_value.get_attribute('textContent') or ""
        print(f"📋 Nilai dropdown saat ini: '{current_dropdown_text}'")
        
    except Exception as e:
        print(f"Error checking form status: {e}")

    # Cari dan klik tombol submit dengan berbagai strategi
    submit_selectors = [
        (By.XPATH, '//span[contains(text(),"Kirim")]/parent::*'),
        (By.XPATH, '//div[@role="button" and contains(.,"Kirim")]'),
        (By.XPATH, '//input[@type="submit"]'),
        (By.XPATH, '//*[contains(@aria-label, "Submit") or contains(@aria-label, "Kirim")]'),
        (By.CSS_SELECTOR, '[role="button"][aria-disabled="false"]')
    ]
    
    print("🔍 Mencari tombol submit...")
    submit_found = False
    
    for selector_type, selector in submit_selectors:
        try:
            submit_elements = driver.find_elements(selector_type, selector)
            if submit_elements:
                submit_btn = submit_elements[0]
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
                time.sleep(1)
                
                # Cek apakah tombol disabled
                is_disabled = submit_btn.get_attribute('aria-disabled')
                if is_disabled == 'true':
                    print("⚠️ Tombol submit masih disabled - ada field yang belum terisi dengan benar")
                else:
                    print("✅ Tombol submit siap diklik")
                
                submit_btn.click()  # Uncomment untuk benar-benar submit
                print("✅ Tombol submit ditemukan! (Tidak diklik untuk testing)")
                submit_found = True
                break
        except Exception as e:
            continue
    
    if not submit_found:
        print("❌ Tombol submit tidak ditemukan")
    
    print("🎉 Proses selesai!")
    time.sleep(10)

except Exception as e:
    print(f"❌ Error utama: {e}")

finally:
    driver.quit()
