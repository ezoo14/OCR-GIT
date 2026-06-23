# 简单发票信息抽取（基于识别后的全文）
import re

def extract_invoice_fields(full_text):
    out = {}
    m = re.search(r'(发票代码[:：]?\s*[\d\-]+)|(发票号码[:：]?\s*[\d\-]+)|(发票号[:：]?\s*[\d\-]+)', full_text)
    if m:
        out['invoice_no'] = m.group(0)
    m = re.search(r'(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})|(\d{4}年\d{1,2}月\d{1,2}日)', full_text)
    if m:
        out['date'] = m.group(0)
    m = re.search(r'(合计[:：]?\s*￥?\s*[\d,]+\.\d{2})|(金额[:：]?\s*￥?\s*[\d,]+\.\d{2})', full_text)
    if m:
        out['total'] = m.group(0)
    if 'total' not in out:
        m = re.search(r'￥\s*[\d,]+\.\d{2}|[0-9,]+\.\d{2}', full_text)
        if m:
            out['total_guess'] = m.group(0)
    return out
