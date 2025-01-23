import requests
from PIL import Image
from tkinter import filedialog, simpledialog, messagebox
import io
import validators
import os


class Download:
    def __init__(self, url):
        self.url = url

    def fazer_download(self):
        """
        Faz o download da imagem da URL fornecida e retorna o caminho do arquivo salvo.
        """
        try:
            # Verifica se a URL é válida
            if not validators.url(self.url):
                messagebox.showerror("Erro", "O link fornecido não é uma URL válida. Certifique-se de que o link está completo e inclui o esquema (http:// ou https://).")
                return None

            response = requests.get(self.url, timeout=10) 
            response.raise_for_status()

            # Verifica se o conteúdo é uma imagem
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                messagebox.showerror("Erro", "O conteúdo do link não é uma imagem. Por favor, forneça um link para uma imagem válida.")
                return None

            
            imagem = Image.open(io.BytesIO(response.content)).convert("RGB")
            
            
            caminho = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png")],
                title="Salvar Imagem"
            )
            if not caminho:
                return None

            imagem.save(caminho)
            return caminho

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Download", f"Não foi possível baixar a imagem. Verifique a URL e sua conexão com a internet. Detalhes: {e}")
        except IOError as e:
            messagebox.showerror("Erro de Imagem", f"Não foi possível processar a imagem. Detalhes: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Um erro inesperado ocorreu: {e}")
        return None
