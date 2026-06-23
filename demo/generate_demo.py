# 生成 demo 示例图片与 PDF（模拟手写、发票与说明书）
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join('demo', 'input_samples')
os.makedirs(OUT, exist_ok=True)

def save(img, path):
    img.save(path)
    print("生成:", path)

# 1. 手写样例（使用普通字体模拟；若有手写字体可替换）
w,h = 1200, 400
img = Image.new('RGB', (w,h), 'white')
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 48)
except:
    font = ImageFont.load_default()
text = "手写样例：\n张三  2026年6月23日\n这是一段模拟手写的文字，用于测试OCR。"
draw.multiline_text((40,40), text, fill='black', font=font, spacing=10)
save(img, os.path.join(OUT, 'handwritten_sample.png'))

# 2. 发票样例（结构化字段）
img2 = Image.new('RGB', (1200,800), 'white')
d2 = ImageDraw.Draw(img2)
try:
    fontb = ImageFont.truetype("DejaVuSans.ttf", 36)
except:
    fontb = ImageFont.load_default()
lines = [
    "发票代码: 123456789012",
    "发票号码: 98765432",
    "开票日期: 2026-06-23",
    "",
    "购方：张三公司",
    "数量  单价  金额",
    "产品A  1   100.00",
    "产品B  2   200.00",
    "",
    "合计：￥300.00"
]
d2.multiline_text((40,40), "\n".join(lines), fill='black', font=fontb, spacing=10)
save(img2, os.path.join(OUT, 'invoice_sample.png'))

# 3. 说明书示例（多页 PDF）
pages = []
try:
    fontp = ImageFont.truetype("DejaVuSans.ttf", 28)
except:
    fontp = ImageFont.load_default()
for p in range(3):
    pg = Image.new('RGB', (1240,1754), 'white')  # A4-ish
    d = ImageDraw.Draw(pg)
    header = f"示例说明书 - 第 {p+1} 页"
    d.text((60,40), header, fill='black', font=fontp)
    body = ("本说明书用于演示 OCR 模板的分块能力。以下为示例段落，包含若干句子，"
            "用于测试形态学分块与段落检测。\n\n" * 6)
    d.multiline_text((60,120), body, fill='black', font=fontp, spacing=6)
    pages.append(pg)
pdf_path = os.path.join(OUT, 'manual_sample.pdf')
pages[0].save(pdf_path, save_all=True, append_images=pages[1:])
print("生成:", pdf_path)
