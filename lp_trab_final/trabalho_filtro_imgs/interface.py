from downloads import Download
from tkinter import filedialog, simpledialog, messagebox
from imagens import Imagem
from filtros import EscalaCinza, PretoBranco, Cartoon, FotoNegativa, Contorno, Blurred
import tkinter as tk
from PIL import Image, ImageTk
import os
import validators

class Principal:
    def __init__(self):
        """
        Inicializa a interface gráfica e configura os elementos.
        """
        self.janela = tk.Tk()
        self.janela.title("Aplicação de Filtros")
        self.janela.geometry("600x700")  # Aumentando um pouco a janela
        self.janela.configure(bg="#f0f0f0")  # Definindo um fundo mais suave
        self.imagem = None

        # Label de Imagem
        self.label_imagem = tk.Label(self.janela, bg="#f0f0f0")
        self.label_imagem.pack(pady=5)  # Espaço superior

        # Botão para escolher imagem
        self.botao_selecionar_imagem = tk.Button(self.janela, text="Escolher Imagem Local", command=self.selecionar_imagem, relief="solid", bg="#5cb85c", fg="white", width=30)
        self.botao_selecionar_imagem.pack(pady=5)

        # Botão para inserir link
        self.botao_inserir_link = tk.Button(self.janela, text="Inserir via Link", command=self.inserir_link_imagem, relief="solid", bg="#0275d8", fg="white", width=30)
        self.botao_inserir_link.pack(pady=5)

        # Filtros
        self.filtros = {
            "Escala de Cinza": EscalaCinza(),
            "Preto e Branco": PretoBranco(),
            "Cartoon": Cartoon(),
            "Modo Negativo": FotoNegativa(),
            "Modo Contorno": Contorno(),
            "Modo Blurred": Blurred()
        }

        self.var_filtros = {nome: tk.BooleanVar() for nome in self.filtros.keys()}
        self.filtro_frame = tk.LabelFrame(self.janela, text="Selecione os Filtros", bg="#f0f0f0", padx=5, pady=5)
        self.filtro_frame.pack(pady=5, padx=10, fill="both")

        for nome, var in self.var_filtros.items():
            tk.Checkbutton(self.filtro_frame, text=nome, variable=var, bg="#f0f0f0").pack(anchor="w", pady=5)

        # Botão para aplicar filtros
        self.botao_aplicar_filtros = tk.Button(self.janela, text="Aplicar Filtros", command=self.aplicar_filtros, relief="solid", bg="#f0ad4e", fg="white", width=30)
        self.botao_aplicar_filtros.pack(pady=5)

        # Botão para listar imagens
        self.botao_listar_imagens = tk.Button(self.janela, text="Listar Arquivos de Imagens", command=self.listar_imagens, relief="solid", bg="#5bc0de", fg="white", width=30)
        self.botao_listar_imagens.pack(pady=5)

        # Botão para sair
        self.botao_sair = tk.Button(self.janela, text="Sair", command=self.janela.quit, relief="solid", bg="#d9534f", fg="white", width=30)
        self.botao_sair.pack(pady=5)

    def selecionar_imagem(self):
        """
        Abre um diálogo para selecionar uma imagem local e a carrega.
        """
        caminho_imagem = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png")])
        if caminho_imagem:
            if not os.path.isfile(caminho_imagem):
                messagebox.showerror("Erro", "O arquivo selecionado não existe.")
                return
            self.imagem = Imagem(caminho_imagem)
            self.exibir_imagem(caminho_imagem)

    def inserir_link_imagem(self):
        """
        Abre um diálogo para inserir um link de imagem, faz o download e carrega a imagem.
        """
        link = simpledialog.askstring("Inserir Link", "Digite o link da imagem:")

        if link:
            link = link.strip()  # Remove espaços em branco antes e depois da URL

            # Verifica se o link é uma URL válida
            if not validators.url(link):
                messagebox.showerror("Erro", "O link fornecido não é uma URL válida. Certifique-se de que o link está completo e inclui o esquema (http:// ou https://).")
                return

            # Faz o download e carrega a imagem
            download = Download(link)
            caminho = download.fazer_download()
            if caminho:
                self.imagem = Imagem(caminho)
                self.exibir_imagem(caminho)
        else:
            messagebox.showerror("Erro", "Nenhum link foi inserido. Por favor, insira um link válido.")

    def exibir_imagem(self, caminho_imagem):
        """
        Exibe a imagem na interface gráfica.
        """
        try:
            imagem = Image.open(caminho_imagem)
            imagem = imagem.resize((300, 300))
            imagem = ImageTk.PhotoImage(imagem)
            self.label_imagem.configure(image=imagem)
            self.label_imagem.image = imagem
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível exibir a imagem: {e}")

    def aplicar_filtros(self):
        """
        Aplica os filtros selecionados à imagem carregada e exibe a imagem filtrada.
        """
        if not self.imagem:
            messagebox.showerror("Erro", "Nenhuma imagem carregada.")
            return

        filtros_selecionados = [filtro for nome, filtro in self.filtros.items() if self.var_filtros[nome].get()]
        
        if not filtros_selecionados:
            messagebox.showinfo("Aviso", "Nenhum filtro foi selecionado. Mostrando imagem original.")
            imagem_original = self.imagem.resetar_imagem()
            caminho_imagem = self.imagem.salvar_imagem(imagem_original, prefixo="imagem_original")
            self.exibir_imagem(caminho_imagem)
            return

        try:
            imagem_filtrada = self.imagem.aplicar_filtros(filtros_selecionados)
            caminho_imagem = self.imagem.salvar_imagem(imagem_filtrada)
            self.exibir_imagem(caminho_imagem)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {e}")

    def listar_imagens(self):
        """
        Lista as imagens salvas na pasta 'imagens modificadas'.
        """
        pasta = "imagens com filtro aplicado"
        try:
            if not os.path.exists(pasta):
                messagebox.showinfo("Info", "Nenhuma imagem encontrada na pasta 'imagens modificadas'.")
                return

            imagens = [f for f in os.listdir(pasta) if f.endswith((".jpg", ".png"))]
            if not imagens:
                messagebox.showinfo("Info", "Nenhuma imagem encontrada na pasta 'imagens modificadas'.")
            else:
                lista_imagens = "\n".join(imagens)
                messagebox.showinfo("Imagens Encontradas", lista_imagens)
        except OSError as e:
            messagebox.showerror("Erro", f"Não foi possível acessar a pasta: {e}")

    def iniciar(self):
        self.janela.mainloop()
