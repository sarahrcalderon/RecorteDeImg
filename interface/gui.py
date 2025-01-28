import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Removedor de Fundo")
        self.root.geometry("800x400")

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.botao_carregar = tk.Button(self.frame, text="Carregar Imagem", command=self.carregar_imagem)
        self.botao_carregar.pack(pady=10)

        self.botao_remover_fundo = tk.Button(self.frame, text="Remover Fundo", command=self.iniciar_remocao_fundo)
        self.botao_remover_fundo.pack(pady=10)

        self.botao_salvar = tk.Button(self.frame, text="Salvar Imagem", command=self.salvar_imagem)
        self.botao_salvar.pack(pady=10)

        self.label_imagem_original = tk.Label(self.frame)
        self.label_imagem_original.pack(side=tk.LEFT, padx=10)

        self.label_imagem_sem_fundo = tk.Label(self.frame)
        self.label_imagem_sem_fundo.pack(side=tk.RIGHT, padx=10)

        self.imagem_original = None
        self.imagem_sem_fundo = None

    def carregar_imagem(self):
        from utils.file_utils import carregar_imagem
        self.imagem_original = carregar_imagem()
        if self.imagem_original:
            self.exibir_imagem(self.imagem_original, self.label_imagem_original)

    def iniciar_remocao_fundo(self):
        if self.imagem_original:
            self.botao_remover_fundo.config(state=tk.DISABLED)
            threading.Thread(target=self.remover_fundo, daemon=True).start()
        else:
            messagebox.showwarning("Aviso", "Por favor, carregue uma imagem primeiro.")

    def remover_fundo(self):
        try:
            from servicos.remocao_fundo import remover_fundo
            self.imagem_sem_fundo = remover_fundo(self.imagem_original)
            self.root.after(0, self.atualizar_interface)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}"))
            self.botao_remover_fundo.config(state=tk.NORMAL)

    def atualizar_interface(self):
        if self.imagem_sem_fundo:
            self.exibir_imagem(self.imagem_sem_fundo, self.label_imagem_sem_fundo)
            self.botao_remover_fundo.config(state=tk.NORMAL)  # Re-enable the button

    def salvar_imagem(self):
        if self.imagem_sem_fundo:
            from utils.file_utils import salvar_imagem
            salvar_imagem(self.imagem_sem_fundo)
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem sem fundo para salvar.")

    def exibir_imagem(self, imagem, label):
        imagem.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(imagem)
        label.config(image=img_tk)
        label.image = img_tk