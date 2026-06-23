# 可选：简单 Flask 上传 API（返回识别 JSON）
from flask import Flask, request, jsonify
import os
import tempfile
from ocr_pipeline import get_ocr_model, process_page

app = Flask(__name__)
ocr = get_ocr_model()

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    mode = request.form.get('mode', 'manual')
    if not f:
        return jsonify({'error': 'no file'}), 400
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, f.filename)
    f.save(path)
    out_dir = os.path.join(tmpdir, 'out')
    try:
        result = process_page(path, out_dir, ocr, mode=mode)
        return jsonify({'result': result})
    finally:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
