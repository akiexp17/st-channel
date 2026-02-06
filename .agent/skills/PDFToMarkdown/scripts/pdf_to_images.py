#!/usr/bin/env python3
"""
PDF to Images Converter
PDFファイルを各ページの画像ファイルに変換するスクリプト
"""

from pdf2image import convert_from_path
import os
import sys

def pdf_to_images(pdf_path, output_dir=None, dpi=150):
    """
    PDFを画像に変換
    
    Args:
        pdf_path: PDFファイルのパス
        output_dir: 出力先ディレクトリ（省略時はPDFと同名のフォルダ）
        dpi: 解像度（デフォルト150）
    """
    if output_dir is None:
        output_dir = os.path.splitext(pdf_path)[0]
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Converting: {pdf_path}")
    print(f"Output dir: {output_dir}")
    print("-" * 40)
    
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        
        for i, image in enumerate(images, 1):
            image_path = os.path.join(output_dir, f"page_{i:03d}.png")
            image.save(image_path, "PNG")
            print(f"[{i}/{len(images)}] Saved: {image_path}")
        
        print("-" * 40)
        print(f"Done! {len(images)} pages converted.")
    except Exception as e:
        print(f"Error converting PDF: {e}")
        print("Please ensure 'poppler' is installed (e.g., 'brew install poppler' on macOS).")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_images.py <pdf_path> [output_dir] [dpi]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    
    pdf_to_images(pdf_path, output_dir, dpi)
