from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

    # Helper function untuk memilih dropdown - IMPROVED VERSION
    def pilih_dropdown(option_text):
        """Memilih opsi dari dropdown Google Forms dengan trigger events yang tepat"""
        try:
            print(f"🔍 Mencari dropdown untuk memilih: {option_text}")
            
            # Tunggu sampai dropdown tersedia
            wait = WebDriverWait(driver, 10)
            
            # Strategi 1: Cari opsi yang sudah ada dan visible
            try:
                # Cari opsi dengan data-value yang sesuai
                option_xpath = f'//div[@role="option" and @data-value="{option_text}"]'
                option_element = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
                
                # Scroll ke element
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", option_element)
                time.sleep(1)
                
                # Trigger mouse events untuk memastikan Google Forms mendeteksi interaksi
                driver.execute_script("""
                    var element = arguments[0];
                    var mouseOverEvent = new MouseEvent('mouseover', {bubbles: true, cancelable: true});
                    var mouseDownEvent = new MouseEvent('mousedown', {bubbles: true, cancelable: true});
                    var clickEvent = new MouseEvent('click', {bubbles: true, cancelable: true});
                    var mouseUpEvent = new MouseEvent('mouseup', {bubbles: true, cancelable: true});
                    
                    element.dispatchEvent(mouseOverEvent);
                    element.dispatchEvent(mouseDownEvent);
                    element.dispatchEvent(clickEvent);
                    element.dispatchEvent(mouseUpEvent);
                """, option_element)
                
                # Tunggu sebentar untuk memastikan perubahan ter-apply
                time.sleep(2)
                
                # Verifikasi apakah opsi sudah terpilih
                if option_element.get_attribute('aria-selected') == 'true':
                    print(f"✅ Opsi '{option_text}' berhasil dipilih dan terverifikasi")
                    return True
                else:
                    print("⚠️ Opsi diklik tapi belum ter-select, mencoba metode alternatif...")
                
            except Exception as e:
                print(f"Strategi 1 gagal: {e}")
            
            # Strategi 2: Cari listbox dan klik opsi dengan cara berbeda
            try:
                # Cari listbox container
                listbox = driver.find_element(By.XPATH, '//div[@role="listbox"]')
                driver.execute_script("arguments[0].scrollIntoView(true);", listbox)
                time.sleep(1)
                
                # Cari semua opsi dalam listbox
                options = listbox.find_elements(By.XPATH, './/div[@role="option"]')
                
                for option in options:
                    try:
                        data_value = option.get_attribute('data-value')
                        if data_value == option_text:
                            print(f"🎯 Ditemukan opsi dengan data-value: {data_value}")
                            
                            # Gunakan ActionChains untuk klik yang lebih natural
                            from selenium.webdriver.common.action_chains import ActionChains
                            actions = ActionChains(driver)
                            actions.move_to_element(option).click().perform()
                            time.sleep(2)
                            
                            # Verifikasi selection
                            if option.get_attribute('aria-selected') == 'true':
                                print(f"✅ Opsi '{option_text}' berhasil dipilih dengan ActionChains")
                                return True
                                
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"Strategi 2 gagal: {e}")
            
            # Strategi 3: Manual JavaScript selection
            try:
                js_script = f"""
                var options = document.querySelectorAll('div[role="option"]');
                for (var i = 0; i < options.length; i++) {{
                    if (options[i].getAttribute('data-value') === '{option_text}') {{
                        // Set aria-selected
                        options[i].setAttribute('aria-selected', 'true');
                        options[i].setAttribute('tabindex', '0');
                        
                        // Remove selection from other options
                        var allOptions = document.querySelectorAll('div[role="option"]');
                        for (var j = 0; j < allOptions.length; j++) {{
                            if (allOptions[j] !== options[i]) {{
                                allOptions[j].setAttribute('aria-selected', 'false');
                                allOptions[j].setAttribute('tabindex', '-1');
                                allOptions[j].classList.remove('KKjvXb');
                            }}
                        }}
                        
                        // Add selected class
                        options[i].classList.add('KKjvXb');
                        
                        // Trigger change event
                        var event = new Event('change', {{ bubbles: true }});
                        options[i].dispatchEvent(event);
                        
                        return true;
                    }}
                }}
                return false;
                """
                
                result = driver.execute_script(js_script)
                if result:
                    print(f"✅ Opsi '{option_text}' berhasil dipilih dengan JavaScript manual")
                    time.sleep(2)
                    return True
                    
            except Exception as e:
                print(f"Strategi 3 gagal: {e}")
            
            # Debug: Tampilkan semua opsi yang tersedia
            print("🔍 Debug - Semua opsi yang tersedia:")
            try:
                all_options = driver.find_elements(By.XPATH, '//div[@role="option"]')
                for i, opt in enumerate(all_options):
                    data_value = opt.get_attribute('data-value')
                    aria_selected = opt.get_attribute('aria-selected')
                    span_text = ""
                    try:
                        span = opt.find_element(By.XPATH, './/span[@class="vRMGwf oJeWuf"]')
                        span_text = span.text
                    except:
                        pass
                    print(f"Opsi {i+1}: data-value='{data_value}', text='{span_text}', selected='{aria_selected}'")
            except Exception as e:
                print(f"Error debug: {e}")
            
            print(f"❌ Semua strategi gagal untuk memilih '{option_text}'")
            return False
            
        except Exception as e:
            print(f"❌ Error umum dalam pilih_dropdown: {e}")
            return False

    # Isi form secara berurutan sesuai layout yang benar
    print("📝 Mulai mengisi form...")
    
    # 1. Nama Reviewer (dropdown - paling atas)
    print("🔽 Memilih Nama Reviewer dari dropdown...")
    pilih_dropdown(data["reviewer"])  
    time.sleep(2)
    
    # 2. Nama Lengkap (input pertama dengan placeholder "Jawaban Anda")
    print("👤 Mengisi Nama Lengkap...")
    isi_input_text(data["nama_lengkap"], 1)
    time.sleep(1)
    
    # 3. Email (input kedua dengan placeholder "Jawaban Anda")
    print("📧 Mengisi Email...")
    isi_input_text(data["email"], 2)
    time.sleep(1)
    
    # 4. DTS ID / Nomor Pendaftaran (input ketiga)
    print("🔢 Mengisi DTS ID...")
    isi_input_text(data["nomor_pendaftaran"], 3)
    time.sleep(1)
    
    # 5. Hal Menarik (textarea pertama)
    print("📝 Mengisi Hal Menarik...")
    isi_textarea(data["hal_menarik"], 1)
    time.sleep(1)
    
    # 6. Feedback (textarea kedua)
    print("💬 Mengisi Feedback...")
    isi_textarea(data["feedback"], 2)
    time.sleep(1)

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