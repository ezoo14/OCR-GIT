# 预处理：加载、增强、保存预处理图
import cv2
import numpy as np
import os

def load_image(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img

def save_image(path, img_bgr):
    ext = os.path.splitext(path)[1]
    _, buf = cv2.imencode(ext if ext else '.png', img_bgr)
    buf.tofile(path)

def enhance_for_ocr(img_bgr, resize_max=1600, denoise=True, sharpen=False):
    h, w = img_bgr.shape[:2]
    if resize_max and max(h, w) > resize_max:
        scale = resize_max / max(h, w)
        img_bgr = cv2.resize(img_bgr, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    if denoise:
        gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    if sharpen:
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0,-1,0]])
        gray = cv2.filter2D(gray, -1, kernel)
    thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 31, 15)
    vis = cv2.cvtColor(thr, cv2.COLOR_GRAY2BGR)
    return thr, vis
