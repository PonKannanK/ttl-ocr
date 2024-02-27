from flask import Flask, request, jsonify
import easyocr
from PIL import Image
import re

app = Flask(__name__)

def perform_ocr(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)

    ext_dic = {'Name': [], 'Company name': [], 'Email': []}

    for item in result:
        text = item[1]
        if '@' in text and '.com' in text:
            small = text.lower()
            ext_dic['Email'].append(small)
        elif re.match(r'^[A-Za-z]', text):
            ext_dic['Name'].append(text)
        else:
            ext_dic['Company name'].append(text)

    return ext_dic

@app.route('/extract-data', methods=['POST'])
def extract_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        image = Image.open(file)
        extracted_data = perform_ocr(image)
        return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)