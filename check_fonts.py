
import matplotlib.font_manager as fm
import sys

def find_japanese_font():
    fonts = fm.findSystemFonts()
    print(f"Found {len(fonts)} fonts.")
    jp_fonts = []
    keywords = ['Hiragino', 'NotoSansJP', 'Takao', 'IPAGothic', 'MS Gothic', 'Meiryo']
    for font_path in fonts:
        try:
            font_prop = fm.FontProperties(fname=font_path)
            font_name = font_prop.get_name()
            # Check for common Japanese font names
            for kw in keywords:
                if kw.lower() in font_name.lower() or kw.lower() in font_path.lower():
                    jp_fonts.append((font_name, font_path))
        except:
            continue
    
    if jp_fonts:
        print("Japanese fonts found:")
        for name, path in jp_fonts[:5]:
            print(f"- {name}: {path}")
    else:
        print("No Japanese fonts found in common locations.")

if __name__ == "__main__":
    find_japanese_font()
