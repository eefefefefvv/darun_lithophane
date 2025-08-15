from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageOps
import os
import numpy as np
from stl import mesh

app = Flask(__name__)

# Папки для хранения
INPUT_FOLDER = 'input/'
STL_FOLDER = 'cache/stl/'
PREVIEW_FOLDER = 'cache/preview/'
OUTPUT_FOLDER = 'output/'

for folder in [INPUT_FOLDER, STL_FOLDER, PREVIEW_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Простейшая обработка фото и генерация STL
def image_to_stl(image_path, stl_path):
    img = Image.open(image_path).convert('L')  # ч/б
    img = ImageOps.invert(img)  # инвертируем, чтобы светлое выступало
    img = img.resize((100, 100))  # маленькая размерность для теста

    data = np.zeros((100, 100, 2, 3))
    for i in range(100):
        for j in range(100):
            z = img.getpixel((i, j)) / 255.0 * 10  # высота
            data[i, j, 0] = [i, j, 0]
            data[i, j, 1] = [i, j, z]

    # создаём STL mesh
    faces = np.zeros((100*99*2, 3, 3))
    count = 0
    for i in range(99):
        for j in range(99):
            faces[count] = [data[i,j,0], data[i+1,j,0], data[i,j+1,0]]
            faces[count+1] = [data[i+1,j,0], data[i+1,j+1,0], data[i,j+1,0]]
            count += 2
    m = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        m.vectors[i] = f
    m.save(stl_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    input_path = os.path.join(INPUT_FOLDER, file.filename)
    stl_path = os.path.join(STL_FOLDER, file.filename.replace('.jpg','.stl'))
    
    file.save(input_path)
    image_to_stl(input_path, stl_path)
    
    return send_file(stl_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

