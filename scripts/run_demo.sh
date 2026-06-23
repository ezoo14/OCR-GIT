#!/bin/bash
set -e
# 生成 demo 示例（若已生成可跳过）
python demo/generate_demo.py
# 运行主程序处理 demo/input_samples
python main.py --input demo/input_samples --output outputs --mode manual
echo "Done. 查看 outputs/ 目录。"
