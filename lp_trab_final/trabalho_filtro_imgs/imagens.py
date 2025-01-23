from tkinter import messagebox
from PIL import Image
from datetime import datetime
import os

class Imagem:
    def __init__(self, caminho):
        """
        Inicializa a imagem a partir do caminho fornecido.
        Se a imagem não for carregada corretamente, define a imagem como None.
        """
        self.caminho = caminho
        try:
            self.imagem_original = Image.open(caminho).convert("RGB")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")
            self.imagem_original = None

    def aplicar_filtros(self, filtros):
        """
        Aplica uma lista de filtros à imagem original e retorna a imagem filtrada.
        """
        if not self.imagem_original:
            messagebox.showerror("Erro", "Imagem não carregada corretamente.")
            return None
        
        if not filtros:
            messagebox.showinfo("Aviso", "Nenhum filtro selecionado.")
            return self.imagem_original

        imagem = self.imagem_original
        for filtro in filtros:
            if hasattr(filtro, 'aplicar'):
                imagem = filtro.aplicar(imagem)
            else:
                messagebox.showerror("Erro", f"O filtro {filtro} não possui o método 'aplicar'.")
                return None

        return imagem

    def salvar_imagem(self, imagem, prefixo="imagem_filtrada"):
        """
        Salva a imagem filtrada em um arquivo com um prefixo e um timestamp.
        """
        if not imagem:
            messagebox.showerror("Erro", "Imagem não fornecida para salvar.")
            return None
        
        pasta = "imagens com filtro aplicado"
        os.makedirs(pasta, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(pasta, f"{prefixo}_{timestamp}.png")
        
        try:
            imagem.save(caminho)
            return caminho
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a imagem: {e}")
            return None

    def resetar_imagem(self):
        """
        Retorna uma cópia da imagem original.
        """
        if not self.imagem_original:
            messagebox.showerror("Erro", "Imagem original não carregada corretamente.")
            return None
        return self.imagem_original.copy()
