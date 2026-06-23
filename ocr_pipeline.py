# OCR 管道：预处理 -> 分块 -> PaddleOCR 识别 -> 保存阶段图与 JSON
import os
import json
from paddleocr import PaddleOCR, draw_ocr
import cv2
from preprocess import load_image, enhance_for_ocr, save_image
from layout import get_text_blocks, draw_layout_overlay
from invoice_kie import extract_invoice_fields
from PIL import Image
import numpy as np

def get_ocr_model(lang='ch', use_angle_cls=True, rec_model_dir=None):
    kwargs = {'use_angle_cls': use_angle_cls, 'lang': 'ch' if lang.startswith('ch') else lang}
    if rec_model_dir:
        kwargs['rec_model_dir'] = rec_model_dir
    ocr = PaddleOCR(**kwargs)
    return ocr

def process_page(image_path, out_dir, ocr, mode='manual', min_area=500):
    os.makedirs(out_dir, exist_ok=True)
    img_bgr = load_image(image_path)
    thr, vis_pre = enhance_for_ocr(img_bgr)
    pre_path = os.path.join(out_dir, 'stage_preprocessed.png')
    save_image(pre_path, cv2.cvtColor(vis_pre, cv2.COLOR_GRAY2BGR))
    boxes = get_text_blocks(thr, min_area=min_area)
    layout_vis_path = os.path.join(out_dir, 'stage_layout_overlay.png')
    layout_vis = draw_layout_overlay(img_bgr, boxes, layout_vis_path)
    blocks_dir = os.path.join(out_dir, 'blocks')
    os.makedirs(blocks_dir, exist_ok=True)
    page_summary = {'image': image_path, 'stages': {'preprocessed': pre_path, 'layout_overlay': layout_vis_path}, 'blocks': []}
    # 整页识别（用于 KIE）
    img_for_ocr = Image.open(image_path)
    ocr_result_page = ocr.ocr(np.array(img_for_ocr), cls=True)
    page_text_all = []
    for line in ocr_result_page:
        if len(line) >=2:
            page_text_all.append(line[1][0])
    page_full_text = '\n'.join(page_text_all)
    kie_result = None
    if mode == 'invoice':
        kie_result = extract_invoice_fields(page_full_text)
    for idx,(x,y,w,h) in enumerate(boxes):
        x2,y2 = x+w, y+h
        block_img = img_bgr[y:y2, x:x2]
        block_path = os.path.join(blocks_dir, f'block_{idx}.png')
        save_image(block_path, block_img)
        block_ocr = ocr.ocr(block_img, cls=True)
        block_texts = []
        for line in block_ocr:
            if len(line)>=2:
                block_texts.append({'text': line[1][0], 'confidence': float(line[1][1]), 'box': [int(v) for v in line[0]]})
        txt_path = os.path.join(blocks_dir, f'block_{idx}.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join([t['text'] for t in block_texts]))
        json_path = os.path.join(blocks_dir, f'block_{idx}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({'texts': block_texts, 'image': block_path}, f, ensure_ascii=False, indent=2)
        page_summary['blocks'].append({'id': idx, 'bbox': [int(x),int(y),int(w),int(h)], 'block_image': block_path, 'text_json': json_path, 'text_file': txt_path})
    page_summary['page_full_text'] = page_full_text
    page_summary['kie'] = kie_result
    page_json_path = os.path.join(out_dir, 'page_ocr.json')
    with open(page_json_path, 'w', encoding='utf-8') as f:
        json.dump(page_summary, f, ensure_ascii=False, indent=2)
    try:
        boxes_all = [line[0] for line in ocr_result_page]
        txts = [line[1][0] for line in ocr_result_page]
        scores = [line[1][1] for line in ocr_result_page]
        img_pil = Image.fromarray(img_bgr[:,:,::-1])
        img_draw = draw_ocr(np.array(img_pil), boxes_all, txts, scores, font_path=None)
        overlay_path = os.path.join(out_dir, 'stage_ocr_overlay.png')
        Image.fromarray(img_draw).save(overlay_path)
        page_summary['stages']['ocr_overlay'] = overlay_path
        with open(page_json_path, 'w', encoding='utf-8') as f:
            json.dump(page_summary, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return page_summary
