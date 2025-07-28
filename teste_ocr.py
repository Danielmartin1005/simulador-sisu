from PIL import Image
import pytesseract

# Caminho do Tesseract instalado
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Abra a imagem (coloque o arquivo 'teste.png' na mesma pasta)
imagem = Image.open("teste.png")

# Extrair texto em português
texto = pytesseract.image_to_string(imagem, lang="por")

# Exibir o resultado
print("🔍 Texto extraído da imagem:")
print(texto)
