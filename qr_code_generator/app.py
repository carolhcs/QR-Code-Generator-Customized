#!/usr/bin/env python3
"""
app.py

Interface web para geração customizada de QR Codes em tempo real.

Dependências:
  pip install flask qrcode pillow

Execute:
  python app.py

Acesse:
  http://localhost:5000/
"""
import io
import os
import tempfile
from flask import Flask, request, send_file, render_template_string
from qr_code_generator import QRCodeGenerator  # importa o módulo criado anteriormente

app = Flask(__name__)

# Template HTML para a interface
HTML = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; }
        label { display: block; margin-top: 1rem; }
        input, select { width: 100%; padding: 0.5rem; margin-top: 0.3rem; }
        #qr-preview { display: block; margin-top: 1rem; width: 100%; height: auto; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Gerador de QR Code Customizável</h1>
    <form id="qr-form">
        <label>Dados ou URL:
            <input type="text" name="data" placeholder="https://exemplo.com" required />
        </label>
        <label>Cor dos quadrados:
            <input type="color" name="fill_color" value="#000000" />
        </label>
        <label>Cor de fundo:
            <input type="color" name="back_color" value="#ffffff" />
        </label>
        <label>Tamanho da caixa (px):
            <input type="number" name="box_size" value="10" min="1" />
        </label>
        <label>Borda (caixas):
            <input type="number" name="border" value="4" min="0" />
        </label>
        <label>Correção de Erros:
            <select name="error_correction">
                <option value="L">L (7%)</option>
                <option value="M" selected>M (15%)</option>
                <option value="Q">Q (25%)</option>
                <option value="H">H (30%)</option>
            </select>
        </label>
        <label>Logo (PNG):
            <input type="file" name="logo" accept="image/png" />
        </label>
    </form>
    <img id="qr-preview" alt="Pré-visualização do QR Code" />

    <script>
        const form = document.getElementById('qr-form');
        const preview = document.getElementById('qr-preview');
        let timeoutId;

        function updateQRCode() {
            const formData = new FormData(form);
            fetch('/generate', { method: 'POST', body: formData })
                .then(res => res.blob())
                .then(blob => {
                    preview.src = URL.createObjectURL(blob);
                });
        }

        form.addEventListener('input', () => {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(updateQRCode, 300);
        });
        form.logo.addEventListener('change', updateQRCode);
        window.addEventListener('load', updateQRCode);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/generate', methods=['POST'])
def generate():
    # Captura parâmetros
    data = request.form.get('data', '')
    fill_color = request.form.get('fill_color', 'black')
    back_color = request.form.get('back_color', 'white')
    box_size = int(request.form.get('box_size', 10))
    border = int(request.form.get('border', 4))
    error_correction = request.form.get('error_correction', 'M')

    # Trata upload de logo
    logo_file = request.files.get('logo')
    logo_path = None
    if logo_file and logo_file.filename:
        suffix = os.path.splitext(logo_file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            logo_file.save(tmp.name)
            logo_path = tmp.name

    # Gera QR code
    gen = QRCodeGenerator(
        error_correction=error_correction,
        box_size=box_size,
        border=border,
        fill_color=fill_color,
        back_color=back_color
    )
    img = gen.generate(data=data, logo_path=logo_path)

    # Remove arquivo temporário de logo
    if logo_path:
        os.remove(logo_path)

    # Retorna imagem como resposta
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
