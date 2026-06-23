# PaddleOCR 项目模板（手写 / 发票 / 说明书分块 + 中间结果）

本仓库包含一个完整的 OCR 管道，基于 PaddleOCR，支持：
- 手写文本识别（可替换自训练模型）
- 发票（启发式 KIE，支持替换为 PaddleKIE）
- 说明书（PDF）分块：基于形态学的段落分块，并输出块级图片与识别结果
- 每个阶段保存中间效果图（预处理、分块可视化、OCR overlay）和 JSON 汇总

快速开始（本地）
1. 克隆或在本地新建仓库，把本模板文件保存到仓库目录。
2. 建议创建并切换到分支（示例使用 create-ocr-template）：
   git checkout -b create-ocr-template
3. 创建并激活虚拟环境，安装依赖：
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
4. 生成 demo 样例（会在 demo/input_samples 下生成图片与 PDF）：
   python demo/generate_demo.py
5. 运行示例（处理 demo 目录）：
   bash scripts/run_demo.sh

主要命令示例
- 处理 demo 输入（默认 mode=manual）：
  python main.py --input demo/input_samples --output outputs --mode manual
- 处理单个 PDF：
  python main.py --input demo/input_samples/manual_sample.pdf --output outputs --mode manual
- 使用自训练识别模型：
  python main.py --input demo/input_samples --output outputs --mode handwritten --rec_model_dir /path/to/rec_model

输出结构（outputs/）
- outputs/<file_stem>_page_<n>/
  - stage_preprocessed.png
  - stage_layout_overlay.png
  - stage_ocr_overlay.png (如果生成成功)
  - blocks/
    - block_0.png
    - block_0.txt
    - block_0.json
  - page_ocr.json

如何把这些文件提交到 GitHub（示例）
- git init
- git add .
- git commit -m "Add paddleocr template and demo generator"
- git branch -M main
- git remote add origin git@github.com:<owner>/<repo>.git
- git push -u origin main
若需新分支（create-ocr-template）：
- git checkout -b create-ocr-template
- git push -u origin create-ocr-template

扩展建议
- 若要高精度手写识别，准备标注数据并在 PaddleOCR 的 recognition 模型上 finetune，然后把路径传给 --rec_model_dir。
- 若发票场景复杂，接入 PaddleKIE 做结构化抽取。
- 若说明书布局更复杂（表格/图/多列），考虑引入 LayoutParser / Detectron2 或 PaddleDetection 做更精细的 layout 分析。

如果你想我把本模板直接打包为 zip 并发给你，或直接把它们提交到你的 GitHub 仓库（我会在 create-ocr-template 分支上提交），把目标仓库地址发给我并授权即可。我也可以直接为你生成 demo outputs 并在聊天中展示示例 JSON（如果需要我现在就运行 demo 并把 outputs 的关键文件贴出来，请允许我先运行生成脚本）。
