#!/usr/bin/env python3
"""
qr_code_generator.py

Sistema para gerar QR Codes customizáveis via linha de comando ou API Python.
Permite ajustar cores, tamanho, nível de correção de erros e incluir logo no centro.

Dependências:
  pip install qrcode pillow

Exemplo de uso (CLI):
  python qr_code_generator.py --data "https://example.com" --output qr.png \
    --fill-color blue --back-color yellow --box-size 10 --border 4 \
    --error-correction H --logo logo.png
"""
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image
import argparse
import os

# Mapear letra de correção para constante
ERROR_CORRECTION_MAP = {
    'L': ERROR_CORRECT_L,  # 7% de correção de erros
    'M': ERROR_CORRECT_M,  # 15%
    'Q': ERROR_CORRECT_Q,  # 25%
    'H': ERROR_CORRECT_H,  # 30%
}

class QRCodeGenerator:
    def __init__(self,
                 error_correction: str = 'M',
                 box_size: int = 10,
                 border: int = 4,
                 fill_color: str = 'black',
                 back_color: str = 'white'):
        """
        Inicializa o gerador de QR code.
        :param error_correction: Nível de correção (L, M, Q, H).
        :param box_size: Número de pixels por "caixinha" do QR.
        :param border: Largura da borda (em caixinhas).
        :param fill_color: Cor dos quadrados do QR.
        :param back_color: Cor de fundo.
        """
        self.error_correction = ERROR_CORRECTION_MAP.get(error_correction.upper(), ERROR_CORRECT_M)
        self.box_size = box_size
        self.border = border
        self.fill_color = fill_color
        self.back_color = back_color

    def generate(self, data: str, logo_path: str = None) -> Image.Image:
        """
        Gera o QR code com os parâmetros definidos.
        :param data: Conteúdo a codificar.
        :param logo_path: Caminho para imagem de logo a ser inserida no centro.
        :return: PIL Image do QR code gerado.
        """
        qr = qrcode.QRCode(
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color).convert('RGB')

        if logo_path and os.path.isfile(logo_path):
            logo = Image.open(logo_path).convert('RGBA')
            # Calcula tamanho do logo (20% do QR)
            w, h = img.size
            factor = 5
            size_logo = (w // factor, h // factor)
            logo = logo.resize(size_logo, Image.ANTIALIAS)

            # Insere logo no centro
            pos = ((w - size_logo[0]) // 2, (h - size_logo[1]) // 2)
            img.paste(logo, pos, logo)

        return img


def main():
    parser = argparse.ArgumentParser(description="Gerador de QR Code customizável")
    parser.add_argument('--data',       required=True, help='Dados ou URL para codificar')
    parser.add_argument('--output',     required=True, help='Arquivo de saída (ex: qr.png)')
    parser.add_argument('--fill-color', default='black', help='Cor dos quadrados (nome CSS ou hex)')
    parser.add_argument('--back-color', default='white', help='Cor de fundo')
    parser.add_argument('--box-size',   type=int, default=10, help='Tamanho de cada caixa em pixels')
    parser.add_argument('--border',     type=int, default=4, help='Tamanho da borda em caixas')
    parser.add_argument('--error-correction', choices=['L','M','Q','H'], default='M',
                        help='Nível de correção de erros: L(7%%),M(15%%),Q(25%%),H(30%%)')
    parser.add_argument('--logo',       help='Caminho para logo (PNG com transparência)')
    args = parser.parse_args()

    gen = QRCodeGenerator(
        error_correction=args.error_correction,
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill_color,
        back_color=args.back_color
    )

    img = gen.generate(data=args.data, logo_path=args.logo)
    img.save(args.output)
    print(f"QR Code salvo em {args.output}")

if __name__ == '__main__':
    main()
