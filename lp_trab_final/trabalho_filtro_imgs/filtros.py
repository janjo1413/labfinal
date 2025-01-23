import cv2
import numpy as np
from PIL import ImageFilter, ImageOps, Image

class Filtro:
    def aplicar(self, imagem: Image.Image) -> Image.Image:
        """
        Aplica um filtro na imagem. Deve ser sobrescrito nas subclasses.
        """
        raise NotImplementedError("Este método deve estar presente nas subclasses!!")

class EscalaCinza(Filtro):
    def aplicar(self, imagem: Image.Image) -> Image.Image:
        """
        Converte a imagem para tons de cinza.
        """
        return imagem.convert("L")

class PretoBranco(Filtro):
    def aplicar(self, imagem: Image.Image) -> Image.Image:
        """
        Converte a imagem para preto e branco puro.
        """
        return imagem.convert("1")

class Cartoon:
    def aplicar(self, imagem_pil):
        """
        Aplica o filtro cartoon à imagem PIL.
        """
        
        imagem_numpy = np.array(imagem_pil)

        # Converte de RGB para BGR para usar com OpenCV
        imagem_bgr = cv2.cvtColor(imagem_numpy, cv2.COLOR_RGB2BGR)

        # Aplica o filtro cartoon (exemplo básico)
        
        imagem_gray = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2GRAY)

        
        imagem_gray = cv2.medianBlur(imagem_gray, 5)

       
        imagem_edge = cv2.adaptiveThreshold(imagem_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                           cv2.THRESH_BINARY, 9, 9)

        
        imagem_color = cv2.bilateralFilter(imagem_bgr, 9, 300, 300)

        
        imagem_cartoon = cv2.bitwise_and(imagem_color, imagem_color, mask=imagem_edge)

        
        imagem_cartoon_rgb = cv2.cvtColor(imagem_cartoon, cv2.COLOR_BGR2RGB)

        
        imagem_final = Image.fromarray(imagem_cartoon_rgb)
        return imagem_final
    
class FotoNegativa(Filtro):
    def aplicar(self, imagem: Image.Image) -> Image.Image:
        """
        Cria a versão negativa da imagem. Converte para RGB, se necessário.
        """
        if imagem.mode != "RGB" and imagem.mode != "L":
            imagem = imagem.convert("RGB")
        return ImageOps.invert(imagem)

class Contorno(Filtro):
    def aplicar(self, imagem: Image.Image) -> Image.Image:
        """
        Realça os contornos dos objetos na imagem.
        """
        return imagem.filter(ImageFilter.CONTOUR)

class Blurred(Filtro):
    def aplicar(self, imagem: Image.Image) -> Image.Image:
        """
        Aplica um desfoque à imagem.
        """
        return imagem.filter(ImageFilter.BLUR)
