
from PIL import Image, ImageDraw, ImageFont
import os

# Paths
IMAGE_PATH = "/Users/akitomo/src/vault/10_Projects/ST_channnel/03_SNS/visuals/2026-02-16_Microbiome_Brain_Rejuvenation.png"
OUTPUT_PATH = "/Users/akitomo/src/vault/10_Projects/ST_channnel/03_SNS/visuals/2026-02-16_Microbiome_Brain_Rejuvenation_Info.png"

# Text content
TITLE = "脳の若返りは腸から？"
SUBTITLE = "Antibiotics restore neurogenesis"
SOURCE = "Source: bioRxiv (2026.02.13)"

LB_AGED = "老化（炎症）"
LB_REJU = "若返り（神経新生）"
LB_GUT = "腸内細菌叢"
LB_EOTAXIN = "Eotaxin-1 (老化信号)"
LB_BLOCK = "抗生物質でリセット"

def get_font(size):
    # Try common Mac fonts
    font_paths = [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Hiragino Kaku Gothic ProN W3.ttc",
        "/Library/Fonts/Arial Unicode.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

def create_infographic():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Image not found at {IMAGE_PATH}")
        return

    img = Image.open(IMAGE_PATH).convert("RGBA")
    width, height = img.size
    
    # Create overlay
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Fonts - Smaller sizes
    title_font = get_font(int(width * 0.05)) # Reduced from 0.08
    subtitle_font = get_font(int(width * 0.03)) # Reduced from 0.04
    label_font = get_font(int(width * 0.035)) # Reduced from 0.05
    source_font = get_font(int(width * 0.025))

    # Helper to draw text with background
    def draw_label(text, x, y, bg_color=(0, 0, 0, 200), text_color="white", anchor="mm"):
        bbox = d.textbbox((x, y), text, font=label_font, anchor=anchor)
        # Expand bbox slightly
        padding = 10
        bbox = (bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding)
        d.rectangle(bbox, fill=bg_color)
        d.text((x, y), text, font=label_font, fill=text_color, anchor=anchor)

    # Header Background
    header_h = int(height * 0.12)
    d.rectangle([(0, 0), (width, header_h)], fill=(15, 23, 42, 230))

    # Title
    d.text((width/2, header_h * 0.35), TITLE, font=title_font, fill="white", anchor="mm")
    d.text((width/2, header_h * 0.75), SUBTITLE, font=subtitle_font, fill="#38BDF8", anchor="mm")

    # Labels - targeted to cover English text based on layout
    
    # Top Left: AGING
    draw_label("老化 (AGING)", width * 0.25, height * 0.15, bg_color=(20, 20, 20, 200))

    # Top Right: Neuroinflammation / Cognitive Decline
    draw_label("脳の炎症", width * 0.75, height * 0.15, text_color="#FCA5A5")
    draw_label("認知機能の低下", width * 0.75, height * 0.40, text_color="#FCA5A5")

    # Bottom Left: REJUVENATION
    draw_label("若返り (REJUVENATION)", width * 0.25, height * 0.53, bg_color=(20, 20, 20, 200), text_color="#6EE7B7")

    # Bottom Right: Neurogenesis / Vitality
    draw_label("神経新生", width * 0.75, height * 0.55, text_color="#6EE7B7")
    draw_label("記憶力の回復", width * 0.80, height * 0.85, text_color="#6EE7B7")

    # Middle: Eotaxin
    # d.line([(width * 0.35, height * 0.3), (width * 0.55, height * 0.25)], fill="red", width=3)
    draw_label("老化信号 (Eotaxin-1)", width * 0.40, height * 0.35, bg_color=(50, 0, 0, 200), text_color="#F87171")
    
    # Bottom Left: Intestine reset
    draw_label("腸内細菌リセット", width * 0.25, height * 0.85, text_color="#34D399")

    # Footer
    footer_h = int(height * 0.05)
    d.rectangle([(0, height - footer_h), (width, height)], fill=(0, 0, 0, 150))
    d.text((width/2, height - footer_h/2), SOURCE, font=source_font, fill="#94A3B8", anchor="mm")

    # Composite
    out = Image.alpha_composite(img, overlay)
    out.save(OUTPUT_PATH)
    print(f"Saved infographic to {OUTPUT_PATH}")

if __name__ == "__main__":
    create_infographic()
