# 布局分块：使用形态学将行合并为段落块
import cv2
import numpy as np

def get_text_blocks(binary_image, min_area=500):
    img = binary_image.copy()
    if np.mean(img) < 127:
        img = cv2.bitwise_not(img)
    h, w = img.shape[:2]
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (max(10, w//40), 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (max(15, w//30), max(15, h//80)))
    closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, hor_kernel)
    closed = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for c in contours:
        x,y,wc,hc = cv2.boundingRect(c)
        area = wc*hc
        if area < min_area:
            continue
        boxes.append((x,y,wc,hc))
    boxes = sorted(boxes, key=lambda b: (b[1]//50, b[0]))
    return boxes

def draw_layout_overlay(orig_bgr, boxes, save_path=None):
    img = orig_bgr.copy()
    for i,(x,y,w,h) in enumerate(boxes):
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(img, str(i), (x, y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    if save_path:
        _, buf = cv2.imencode('.png', img)
        buf.tofile(save_path)
    return img
