# CLI：支持图片目录或PDF（pdf2image），mode: manual|invoice|handwritten
import argparse
import os
from pathlib import Path
from ocr_pipeline import get_ocr_model, process_page
from pdf2image import convert_from_path
from tqdm import tqdm

def process_input(input_path, out_root, mode='manual', lang='ch', rec_model_dir=None):
    ocr = get_ocr_model(lang=lang, rec_model_dir=rec_model_dir)
    p = Path(input_path)
    if p.is_file() and p.suffix.lower() in ['.pdf']:
        pages = convert_from_path(str(p))
        for i, page in enumerate(pages):
            page_img_path = os.path.join(out_root, f'{p.stem}_page_{i}.png')
            os.makedirs(out_root, exist_ok=True)
            page.save(page_img_path)
            out_dir = os.path.join(out_root, f'{p.stem}_page_{i}')
            process_page(page_img_path, out_dir, ocr, mode=mode)
    elif p.is_dir():
        files = sorted([x for x in p.iterdir() if x.is_file() and x.suffix.lower() in ['.png','.jpg','.jpeg','.tif','.tiff','.bmp']])
        for f in tqdm(files):
            out_dir = os.path.join(out_root, f.stem)
            process_page(str(f), out_dir, ocr, mode=mode)
    elif p.is_file():
        out_dir = os.path.join(out_root, p.stem)
        process_page(str(p), out_dir, ocr, mode=mode)
    else:
        raise ValueError('Input not找到')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='image file / pdf file / input dir')
    parser.add_argument('--output', required=True, help='output dir')
    parser.add_argument('--mode', default='manual', choices=['manual','invoice','handwritten'], help='processing mode')
    parser.add_argument('--lang', default='ch', help='paddleocr lang param (ch/en/other)')
    parser.add_argument('--rec_model_dir', default=None, help='可选：自定义识别模型目录')
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)
    process_input(args.input, args.output, mode=args.mode, lang=args.lang, rec_model_dir=args.rec_model_dir)
