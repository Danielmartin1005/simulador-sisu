import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pytesseract
import os

# Caminho onde a imagem será salva
screenshot_path = "captura_plurall.png"

# Configurar opções do navegador
options = Options()
options.add_argument("--start-maximized")

# Iniciar o driver (assumindo que o chromedriver já está rodando em modo standalone)
driver = webdriver.Remote(command_executor='http://localhost:9515', options=options)

# URL do livro (exemplo real)
url = "https://bibliotecadeconteudos.plurall.net/#book/pdf/21437d2e-3405-45ce-99a4-c04952aad3cd"
driver.get(url)

# Tempo de espera para carregar o conteúdo visual
print("⌛ Aguardando carregamento da página...")
time.sleep(15)  # Ajuste se necessário

# Tira screenshot da janela inteira
driver.save_screenshot(screenshot_path)
print(f"📸 Captura de tela salva em: {screenshot_path}")

# Fecha o navegador
driver.quit()

# Realiza OCR com pytesseract
print("\n🧠 Extraindo texto da imagem com OCR...")
imagem = Image.open(screenshot_path)
texto = pytesseract.image_to_string(imagem, lang="por")

print("\n📝 Texto extraído da imagem:\n")
print(texto)
