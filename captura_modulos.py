import time
import cv2
import pytesseract
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO

# Caminho para o Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Caminho do chromedriver
chromedriver_path = r"C:\Users\dan_m\Documents\testepyton\chromedriver.exe"

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acessa a tela de login
driver.get("https://login.plurall.net")

# Aguarda o iframe do auth0 carregar e entra nele
iframe = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='auth0.com']"))
)
driver.switch_to.frame(iframe)

# Preenche e-mail
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, "username"))
).send_keys("daniel.martin@colegioser.com")

# Preenche senha
driver.find_element(By.NAME, "password").send_keys("Nani171211#")

# Clica no botão de login
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Volta ao contexto principal após login
driver.switch_to.default_content()

# Aguarda redirecionamento para página principal
time.sleep(10)

# Aguarda o carregamento da biblioteca de conteúdos
driver.get("https://bibliotecadeconteudos.plurall.net/")
time.sleep(5)

# Rola e espera a visualização dos livros
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.TAG_NAME, "canvas"))
)

# Cria pasta para capturas
output_dir = r"C:\Users\dan_m\Documents\testepyton\modulos"
os.makedirs(output_dir, exist_ok=True)

# Loop de captura de páginas com "Módulo" no topo
for i in range(50):  # Limite de páginas a verificar
    time.sleep(2)

    # Captura screenshot da tela
    screenshot = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(screenshot))
    img_cv = cv2.cvtColor(cv2.imread(BytesIO(screenshot)), cv2.COLOR_BGR2RGB)

    # OCR para detectar texto
    text = pytesseract.image_to_string(img_cv, lang="por")

    if text.strip().lower().startswith("módulo") or "MÓDULO" in text:
        nome_arquivo = os.path.join(output_dir, f"pagina_modulo_{i+1}.png")
        img.save(nome_arquivo)
        print(f"[✔] Página com 'Módulo' encontrada e salva: {nome_arquivo}")

    # Clica na seta para próxima página (ajuste se o botão for diferente)
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-element='pageNextButton']"))
        )
        next_btn.click()
    except:
        print("[!] Botão de próxima página não encontrado.")
        break

print("✅ Captura finalizada.")
driver.quit()
