# Customizable QR Code Generator

A simple web interface to generate customizable QR Codes in real time. Built with Python, Flask, qrcode, and Pillow.

## 📦 Technologies

- **Python 3.7+**
- **Flask**: lightweight web framework
- **qrcode**: library for QR Code generation
- **Pillow**: image processing library (for logo insertion)

## 🚀 Features

- Generate a QR Code from any text or URL
- Real-time customization of:
  - Foreground color
  - Background color
  - Module (box) size
  - Border width
  - Error correction level (L, M, Q, H)
  - Optional centered PNG logo
- Instant preview via web interface

## 🛠️ How It Was Built (Summary)

1. **`qr_code_generator.py`**: Encapsulates the logic for creating QR Code images with customizable parameters and an optional logo.
2. **`app.py`**: Flask server that serves an HTML page with a form and preview. Handles AJAX requests and uses the QR generator module to produce images on the fly.
3. **HTML + JavaScript**: Provides input fields, color pickers, file upload for the logo, and an asynchronous fetch call to update the QR Code without reloading the page.

## 📋 Prerequisites

- Git
- Python 3.7 or higher
- pip (Python package manager)

## ⚙️ Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/qr-code-generator-customizable.git
   cd qr-code-generator-customizable
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If you don’t have a `requirements.txt`, simply run:
   ```bash
   pip install flask qrcode pillow
   ```

4. **Run the server**
   ```bash
   python app.py
   ```

5. **Open in your browser**
   Navigate to [http://localhost:5000](http://localhost:5000) to start generating QR Codes.

## 📁 Project Structure

```plaintext
├── app.py                 # Flask server and web interface
├── qr_code_generator.py   # Core QR Code generation logic
├── requirements.txt       # (optional) dependency list
└── README.md              # This documentation file
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

