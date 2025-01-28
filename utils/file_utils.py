from tkinter import filedialog
from PIL import Image

def carregar_imagem():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
    if caminho_imagem:
        return Image.open(caminho_imagem)
    return None

def salvar_imagem(imagem):
    caminho_salvar = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if caminho_salvar:
        imagem.save(caminho_salvar)