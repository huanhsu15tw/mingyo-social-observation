#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Threads Cards (1080x1350, 4:5 ratio)
Refined with precision typography, anti-orphan wrapping, zero emoji, zero missing glyphs,
and uncropped original screenshots.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (Threads 4:5 vertical standard)
WIDTH = 1080
HEIGHT = 1350

# Colors (Huan Design System)
C_PAPER = "#F7F4EF"
C_CARD_BG = "#FFFFFF"
C_INK = "#2B2A28"
C_INK_MUTED = "#6B6862"
C_STONE = "#B8B2A7"
C_STONE_LIGHT = "#E2DDD4"
C_MOSS = "#5C6B54"
C_MOSS_LIGHT = "#EDF0EA"
C_RUST = "#A85B42"
C_RUST_LIGHT = "#F7E9E4"

# Fonts
FONT_PATH_BOLD = "/Users/huanhsu/Library/Fonts/SourceHanSansTC-Bold.otf"
FONT_PATH_MED = "/Users/huanhsu/Library/Fonts/SourceHanSansTC-Medium.otf"
FONT_PATH_REG = "/Users/huanhsu/Library/Fonts/SourceHanSansTC-Normal.otf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_title_lg = get_font(FONT_PATH_BOLD, 44)
font_title = get_font(FONT_PATH_BOLD, 36)
font_subtitle = get_font(FONT_PATH_REG, 23)
font_eyebrow = get_font(FONT_PATH_BOLD, 17)
font_body = get_font(FONT_PATH_REG, 22)
font_body_bold = get_font(FONT_PATH_BOLD, 22)
font_sm = get_font(FONT_PATH_REG, 18)
font_sm_bold = get_font(FONT_PATH_BOLD, 18)
font_footer = get_font(FONT_PATH_MED, 17)

def create_base_canvas():
    return Image.new("RGB", (WIDTH, HEIGHT), C_PAPER)

def draw_pill(draw, x, y, text, font, bg, fg, border_color=None):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 18, 8
    pill_w = tw + pad_x * 2
    pill_h = th + pad_y * 2 + 2
    draw.rounded_rectangle([x, y, x + pill_w, y + pill_h], radius=999, fill=bg, outline=border_color or fg, width=1)
    text_y = y + (pill_h - th) // 2 - bbox[1] - 1
    draw.text((x + pad_x, text_y), text, font=font, fill=fg)
    return pill_w, pill_h

def draw_header(draw, eyebrow_text, title_text, subtitle_text, is_alert=False):
    x = 64
    y = 56
    
    badge_bg = C_RUST_LIGHT if is_alert else C_MOSS_LIGHT
    badge_fg = C_RUST if is_alert else C_MOSS
    
    pw, ph = draw_pill(draw, x, y, eyebrow_text, font_eyebrow, badge_bg, badge_fg)
    y += ph + 20
    
    # Main Title
    draw.text((x, y), title_text, font=font_title, fill=C_INK)
    y += 50
    
    # Subtitle
    draw.text((x, y), subtitle_text, font=font_subtitle, fill=C_INK_MUTED)
    y += 42
    
    # Separator line
    draw.line([(x, y), (WIDTH - x, y)], fill=C_STONE_LIGHT, width=1)
    return y + 24

def draw_footer(draw, page_str):
    y = HEIGHT - 52
    x = 64
    draw.line([(x, y - 14), (WIDTH - x, y - 14)], fill=C_STONE_LIGHT, width=1)
    draw.text((x, y), page_str, font=font_footer, fill=C_INK_MUTED)
    right_text = "數位社群認知操作與社交工程手法研析"
    r_bbox = font_footer.getbbox(right_text)
    draw.text((WIDTH - x - (r_bbox[2] - r_bbox[0]), y), right_text, font=font_footer, fill=C_INK_MUTED)

def fit_image_inside(img_path, max_w, max_h):
    if not os.path.exists(img_path):
        return None
    im = Image.open(img_path).convert("RGBA")
    w, h = im.size
    ratio = min(max_w / w, max_h / h, 1.0)
    new_w = max(1, int(w * ratio))
    new_h = max(1, int(h * ratio))
    return im.resize((new_w, new_h), Image.Resampling.LANCZOS)

def wrap_text_balanced(text, max_w, font):
    """Word wrapping with anti-orphan logic (prevents 1-2 char trailing lines)."""
    paragraphs = text.split("\n")
    all_lines = []
    
    for p in paragraphs:
        if not p:
            all_lines.append("")
            continue
        cur = ""
        p_lines = []
        for char in p:
            test = cur + char
            bbox = font.getbbox(test)
            if bbox[2] - bbox[0] <= max_w:
                cur = test
            else:
                p_lines.append(cur)
                cur = char
        if cur:
            p_lines.append(cur)
            
        # Anti-orphan check: if last line is too short, balance with previous line
        if len(p_lines) >= 2 and len(p_lines[-1]) <= 2:
            prev = p_lines[-2]
            last = p_lines[-1]
            if len(prev) > 5:
                # Move 2 characters from prev to last
                p_lines[-2] = prev[:-2]
                p_lines[-1] = prev[-2:] + last
                
        all_lines.extend(p_lines)
    return all_lines

def draw_text_multiline(draw, text, x, y, max_w, font, fill, line_spacing=10):
    lines = wrap_text_balanced(text, max_w, font)
    cur_y = y
    for line in lines:
        draw.text((x, cur_y), line, font=font, fill=fill)
        bbox = font.getbbox(line)
        line_h = (bbox[3] - bbox[1]) if line else 20
        cur_y += line_h + line_spacing
    return cur_y

# ==========================================
# CARD 1: COVER
# ==========================================
def generate_card_01(output_path):
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)
    
    y = draw_header(
        draw,
        "CASE STUDY ｜ 案例研析報告",
        "社群認知操作與社交工程手法解析",
        "跨國盜圖養號、南美門號露餡、生活化故事包裝與境外灌粉"
    )
    
    box_w = WIDTH - 128
    overview_text = (
        "近期社群平台出現自稱在地選民的感人貼文，生動描寫公職候選人於街頭拜票、親切對話等私領域細節。"
        "深入查核其數位跡證，發現該帳號全盤盜用外國無辜素人生活照，註冊地在阿根廷、綁定巴西門號，"
        "揭露了一套精準利用生活感故事帶流量與介入選舉的社群社交工程手法。"
    )
    draw.rounded_rectangle([64, y, 64 + box_w, y + 146], radius=16, fill=C_CARD_BG, outline=C_STONE_LIGHT, width=1)
    draw_text_multiline(draw, overview_text, 88, y + 20, box_w - 48, font_body, C_INK, line_spacing=8)
    
    y += 170
    
    draw.text((64, y), "四大核心手法剖析", font=font_body_bold, fill=C_MOSS)
    y += 38
    
    card_w = (box_w - 24) // 2
    card_h = 186
    
    modules = [
        ("01 跨國盜圖「養號」", "偷取外國素人自拍與隨筆，偽造在地生活感降低戒心", C_MOSS_LIGHT, C_MOSS),
        ("02 地理門號雙重露餡", "阿根廷登記＋巴西電話（+55），卻在台北街頭巧遇？", C_RUST_LIGHT, C_RUST),
        ("03 假貼文社交工程", "避談政策，以「蹲下講話、體貼結紮」吸引演算法推播", C_MOSS_LIGHT, C_MOSS),
        ("04 幽靈灌粉毒害體質", "大量非洲中東帳號湧入，稀釋自然互動，慢性破壞觸及率", C_RUST_LIGHT, C_RUST)
    ]
    
    for idx, (m_title, m_desc, bg_color, tag_color) in enumerate(modules):
        r = idx // 2
        c = idx % 2
        mx = 64 + c * (card_w + 24)
        my = y + r * (card_h + 18)
        
        draw.rounded_rectangle([mx, my, mx + card_w, my + card_h], radius=14, fill=C_CARD_BG, outline=C_STONE_LIGHT, width=1)
        draw.rounded_rectangle([mx, my, mx + card_w, my + 6], radius=3, fill=tag_color)
        
        bbox = font_sm_bold.getbbox(m_title)
        draw.rounded_rectangle([mx + 20, my + 20, mx + 20 + (bbox[2]-bbox[0]) + 16, my + 20 + 30], radius=6, fill=bg_color, outline=tag_color, width=1)
        draw.text((mx + 28, my + 25), m_title, font=font_sm_bold, fill=tag_color)
        
        draw_text_multiline(draw, m_desc, mx + 20, my + 68, card_w - 40, font_sm, C_INK_MUTED, line_spacing=7)
    
    y += card_h * 2 + 46
    
    callout_h = 110
    draw.rounded_rectangle([64, y, 64 + box_w, y + callout_h], radius=14, fill=C_MOSS_LIGHT, outline=C_MOSS, width=1)
    draw.text((88, y + 20), "客觀研析聲明", font=font_body_bold, fill=C_MOSS)
    callout_desc = "本報告全篇本於公開數位跡證與 Meta 官方紀錄客觀梳理，期盼協助大眾理解現代認知操作手法，提升公民數位識讀能力。"
    draw_text_multiline(draw, callout_desc, 88, y + 52, box_w - 48, font_sm, C_INK, line_spacing=6)
    
    draw_footer(draw, "01 / 07 ｜ 案例研析報告")
    img.save(output_path, "PNG", quality=95)
    print("Card 01 generated.")

# ==========================================
# CARD 2: METHOD 1 - IDENTITY THEFT
# ==========================================
def generate_card_02(output_path):
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)
    
    y = draw_header(
        draw,
        "METHOD 01 ｜ 跨國盜圖「養號」",
        "偷取外國素人自拍隨筆，偽造在地生活感",
        "盜用馬來西亞女性 9/13 居家自拍作頭貼，簡體隨筆改寫成繁體"
    )
    
    box_w = WIDTH - 128
    col_w = (box_w - 24) // 2
    col_h = 670
    
    # Left Column: Authentic Victim
    lx = 64
    draw.rounded_rectangle([lx, y, lx + col_w, y + col_h], radius=16, fill=C_CARD_BG, outline=C_MOSS, width=2)
    draw.rounded_rectangle([lx + 16, y + 16, lx + col_w - 16, y + 54], radius=8, fill=C_MOSS_LIGHT, outline=C_MOSS, width=1)
    draw.text((lx + 28, y + 24), "真實本尊 ｜ 馬來西亞 (@lokejiaen)", font=font_sm_bold, fill=C_MOSS)
    
    img_real = fit_image_inside("assets/img/04_本尊遭盜用成頭貼的照片.jpg", col_w - 40, 430)
    if img_real:
        iw, ih = img_real.size
        im_x = lx + 20 + (col_w - 40 - iw) // 2
        im_y = y + 70 + (430 - ih) // 2
        draw.rounded_rectangle([lx + 18, y + 68, lx + col_w - 18, y + 502], radius=10, fill=C_PAPER, outline=C_STONE_LIGHT, width=1)
        img.paste(img_real, (im_x, im_y), img_real)
    
    draw_text_multiline(
        draw,
        "9/13 於馬來西亞發布居家生活自拍，配搭簡體中文心情隨筆，為真實素人日常生活紀錄。",
        lx + 20, y + 520, col_w - 40, font_sm, C_INK, line_spacing=6
    )
    
    # Right Column: Imposter Account
    rx = 64 + col_w + 24
    draw.rounded_rectangle([rx, y, rx + col_w, y + col_h], radius=16, fill=C_CARD_BG, outline=C_RUST, width=2)
    draw.rounded_rectangle([rx + 16, y + 16, rx + col_w - 16, y + 54], radius=8, fill=C_RUST_LIGHT, outline=C_RUST, width=1)
    draw.text((rx + 28, y + 24), "涉案假帳號 ｜ 境外人頭 (@dpzsm...)", font=font_sm_bold, fill=C_RUST)
    
    img_fake = fit_image_inside("assets/img/04_盜用者頭貼.jpg", col_w - 40, 430)
    if img_fake:
        iw, ih = img_fake.size
        im_x = rx + 20 + (col_w - 40 - iw) // 2
        im_y = y + 70 + (430 - ih) // 2
        draw.rounded_rectangle([rx + 18, y + 68, rx + col_w - 18, y + 502], radius=10, fill=C_PAPER, outline=C_STONE_LIGHT, width=1)
        img.paste(img_fake, (im_x, im_y), img_fake)
        
    draw_text_multiline(
        draw,
        "直接截取同一張自拍照做為個人頭貼，並將簡體字隨筆改寫為繁體「養號」，營造真實生活感。",
        rx + 20, y + 520, col_w - 40, font_sm, C_INK, line_spacing=6
    )
    
    y += col_h + 24
    
    # Bottom Analysis Box
    ana_h = 170
    draw.rounded_rectangle([64, y, 64 + box_w, y + ana_h], radius=14, fill=C_MOSS_LIGHT, outline=C_MOSS, width=1)
    draw.text((88, y + 18), "手法解析：跨國搬運建立「無害人設」", font=font_body_bold, fill=C_MOSS)
    ana_desc = (
        "現代社群防偽機制對純空頭帳號極為敏感。網軍為規避平台偵測並博取大眾信任，"
        "專門跨國搜尋語言相近、追蹤數不高的外國素人，整套搬運自拍與生活隨筆進行「養號」，"
        "藉此塑造親切無害的鄰家女子形象，為後續置入宣傳鋪路。"
    )
    draw_text_multiline(draw, ana_desc, 88, y + 50, box_w - 48, font_sm, C_INK, line_spacing=6)
    
    draw_footer(draw, "02 / 07 ｜ 案例研析報告")
    img.save(output_path, "PNG", quality=95)
    print("Card 02 generated.")

# ==========================================
# CARD 3: METHOD 2 - LOCATION & PHONE
# ==========================================
def generate_card_03(output_path):
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)
    
    y = draw_header(
        draw,
        "METHOD 02 ｜ 地理與門號雙重露餡",
        "阿根廷登記＋巴西門號，卻在台北巷口巧遇？",
        "官方帳號透明度與雙重驗證紀錄，揭露深植南美洲的數位足跡",
        is_alert=True
    )
    
    box_w = WIDTH - 128
    col_w = (box_w - 24) // 2
    col_h = 670
    
    # Left Column: Meta Location Argentina
    lx = 64
    draw.rounded_rectangle([lx, y, lx + col_w, y + col_h], radius=16, fill=C_CARD_BG, outline=C_RUST, width=2)
    draw.rounded_rectangle([lx + 16, y + 16, lx + col_w - 16, y + 54], radius=8, fill=C_RUST_LIGHT, outline=C_RUST, width=1)
    draw.text((lx + 28, y + 24), "跡證一 ｜ Meta 官方透明度紀錄", font=font_sm_bold, fill=C_RUST)
    
    img_loc = fit_image_inside("assets/img/07_盜用者IG狀態.jpg", col_w - 40, 430)
    if img_loc:
        iw, ih = img_loc.size
        im_x = lx + 20 + (col_w - 40 - iw) // 2
        im_y = y + 70 + (430 - ih) // 2
        draw.rounded_rectangle([lx + 18, y + 68, lx + col_w - 18, y + 502], radius=10, fill=C_PAPER, outline=C_STONE_LIGHT, width=1)
        img.paste(img_loc, (im_x, im_y), img_loc)
        
    draw_text_multiline(
        draw,
        "Meta 官方帳號資訊明確顯示：建立時間為 2026 年 8 月，帳號所在地為阿根廷（Argentina）。",
        lx + 20, y + 520, col_w - 40, font_sm, C_INK, line_spacing=6
    )
    
    # Right Column: Brazil Phone (+55)
    rx = 64 + col_w + 24
    draw.rounded_rectangle([rx, y, rx + col_w, y + col_h], radius=16, fill=C_CARD_BG, outline=C_RUST, width=2)
    draw.rounded_rectangle([rx + 16, y + 16, rx + col_w - 16, y + 54], radius=8, fill=C_RUST_LIGHT, outline=C_RUST, width=1)
    draw.text((rx + 28, y + 24), "跡證二 ｜ 密碼驗證綁定之電話門號", font=font_sm_bold, fill=C_RUST)
    
    img_phone = fit_image_inside("assets/img/假帳號電話.jpg", col_w - 40, 430)
    if img_phone:
        iw, ih = img_phone.size
        im_x = rx + 20 + (col_w - 40 - iw) // 2
        im_y = y + 70 + (430 - ih) // 2
        draw.rounded_rectangle([rx + 18, y + 68, rx + col_w - 18, y + 502], radius=10, fill=C_PAPER, outline=C_STONE_LIGHT, width=1)
        img.paste(img_phone, (im_x, im_y), img_phone)
        
    draw_text_multiline(
        draw,
        "帳號雙重驗證代碼傳送至手機號碼「+55 ** *****_**85」，國碼 +55 明確指向南美洲巴西。",
        rx + 20, y + 516, col_w - 40, font_sm, C_INK, line_spacing=6
    )
    
    y += col_h + 24
    
    # Bottom Analysis Box
    ana_h = 170
    draw.rounded_rectangle([64, y, 64 + box_w, y + ana_h], radius=14, fill=C_RUST_LIGHT, outline=C_RUST, width=1)
    draw.text((88, y + 18), "手法解析：境外黑市免洗帳號的數位破綻", font=font_body_bold, fill=C_RUST)
    ana_desc = (
        "發文者在貼文中繪聲繪影描寫自己在台北街頭巧遇候選人，然而其背後的數位足跡卻同時跨越阿根廷與巴西。"
        "這顯示該帳號是由境外黑市批次採購的虛擬門號註冊而成，雖然文字能偽裝在地生活，"
        "但在電信門號與平台官方稽核紀錄上留下難以抹滅的破綻。"
    )
    draw_text_multiline(draw, ana_desc, 88, y + 50, box_w - 48, font_sm, C_INK, line_spacing=6)
    
    draw_footer(draw, "03 / 07 ｜ 案例研析報告")
    img.save(output_path, "PNG", quality=95)
    print("Card 03 generated.")

# ==========================================
# CARD 4: METHOD 3 - SOCIAL ENGINEERING POST
# ==========================================
def generate_card_04(output_path):
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)
    
    y = draw_header(
        draw,
        "METHOD 03 ｜ 社交工程假貼文",
        "避開生硬政策，用生活私領域細節吸引推播",
        "以「蹲下與小孩說話」、「體貼妻子結紮」營造高共鳴話題"
    )
    
    box_w = WIDTH - 128
    left_w = 460
    right_w = box_w - left_w - 24
    main_h = 680
    
    # Left: Post Screenshot Container
    draw.rounded_rectangle([64, y, 64 + left_w, y + main_h], radius=16, fill=C_CARD_BG, outline=C_STONE_LIGHT, width=1)
    draw.rounded_rectangle([80, y + 16, 64 + left_w - 16, y + 52], radius=8, fill=C_MOSS_LIGHT, outline=C_MOSS, width=1)
    draw.text((92, y + 22), "涉案假貼文完整卡片截圖", font=font_sm_bold, fill=C_MOSS)
    
    img_post = fit_image_inside("assets/img/threads-post-4009801223340246656.png", left_w - 36, main_h - 90)
    if img_post:
        iw, ih = img_post.size
        im_x = 64 + (left_w - iw) // 2
        im_y = y + 68 + (main_h - 90 - ih) // 2
        img.paste(img_post, (im_x, im_y), img_post)
    
    # Right: Narrative Tactics Breakdown
    rx = 64 + left_w + 24
    draw.rounded_rectangle([rx, y, rx + right_w, y + main_h], radius=16, fill=C_CARD_BG, outline=C_STONE_LIGHT, width=1)
    
    draw.rounded_rectangle([rx + 16, y + 16, rx + right_w - 16, y + 52], radius=8, fill=C_PAPER, outline=C_STONE_LIGHT, width=1)
    draw.text((rx + 28, y + 22), "假貼文三大話術特徵拆解", font=font_sm_bold, fill=C_INK)
    
    tactics = [
        ("一、自稱在地選民巧遇", "以第一人稱自述「帶小孩在巷口遇到」，迅速拉近與在地讀者的心理距離，消除宣傳防備。"),
        ("二、放大親民肢體細節", "生動刻劃候選人「蹲下來跟小孩說話」，營造溫柔、親切、有耐心的公眾人物形象。"),
        ("三、置入私領域家庭話題", "特別提及「體貼妻子主動結紮」、「稱讚太太漂亮」，將討論焦點從嚴肅政見轉移至高共鳴的家庭生活話題。")
    ]
    
    ty = y + 70
    for t_title, t_desc in tactics:
        draw.text((rx + 20, ty), t_title, font=font_sm_bold, fill=C_MOSS)
        ty += 30
        ty = draw_text_multiline(draw, t_desc, rx + 20, ty, right_w - 40, font_sm, C_INK_MUTED, line_spacing=5)
        ty += 16
        draw.line([(rx + 20, ty - 8), (rx + right_w - 20, ty - 8)], fill=C_STONE_LIGHT, width=1)
    
    y += main_h + 24
    
    ana_h = 160
    draw.rounded_rectangle([64, y, 64 + box_w, y + ana_h], radius=14, fill=C_MOSS_LIGHT, outline=C_MOSS, width=1)
    draw.text((88, y + 18), "手法解析：利用社交心理學觸動社群演算法", font=font_body_bold, fill=C_MOSS)
    ana_desc = (
        "現代閱聽眾對傳統政見宣傳防備心高，但對「溫馨家庭、體貼丈夫」的生活化故事極易產生情緒共鳴。"
        "社群平台演算法偏好高留言、高轉發的情緒貼文，這類貼文便能輕易鑽入演算法推播池，達成公關操作目標。"
    )
    draw_text_multiline(draw, ana_desc, 88, y + 50, box_w - 48, font_sm, C_INK, line_spacing=6)
    
    draw_footer(draw, "04 / 07 ｜ 案例研析報告")
    img.save(output_path, "PNG", quality=95)
    print("Card 04 generated.")

# ==========================================
# CARD 5: METHOD 4 - COMMENT MANIPULATION
# ==========================================
def generate_card_05(output_path):
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)
    
    y = draw_header(
        draw,
        "METHOD 04 ｜ 套版留言唱和",
        "留言搭腔超不誠懇、無真人味",
        "一搭一唱公式化對答，缺乏真實選民的自然生活感"
    )
    
    box_w = WIDTH - 128
    
    # Clean text without missing unicode arrows
    comments_data = [
        ("assets/img/截圖 2026-10-18 上午9.51.49.png", "留言「很親民」／作者秒回官方口號「真的！好感度+1」", "套版回覆：秒回官方宣傳口號，毫無一般選民對話的自然誠懇感。"),
        ("assets/img/截圖 2026-10-18 上午9.51.53.png", "留言「蹲下跟小孩說話很加分」／作者附和「有同感~」", "刻意唱和：完全順著文章預設人設搭腔，套路痕跡明顯、無真人味。"),
        ("assets/img/截圖 2026-10-18 上午9.52.07.png", "留言「自己去結紮」／作者回「體貼的男人會發財」", "金句推銷：硬塞套版宣傳金句，完全看不出真實民眾討論市政的人味。")
    ]
    
    row_h = 210
    for idx, (c_img_path, c_summary, c_critique) in enumerate(comments_data):
        cy = y + idx * (row_h + 16)
        draw.rounded_rectangle([64, cy, 64 + box_w, cy + row_h], radius=14, fill=C_CARD_BG, outline=C_STONE_LIGHT, width=1)
        
        img_c = fit_image_inside(c_img_path, 460, row_h - 28)
        if img_c:
            iw, ih = img_c.size
            im_x = 80 + (460 - iw) // 2
            im_y = cy + 14 + (row_h - 28 - ih) // 2
            draw.rounded_rectangle([78, cy + 12, 542, cy + row_h - 12], radius=8, fill=C_PAPER, outline=C_STONE_LIGHT, width=1)
            img.paste(img_c, (im_x, im_y), img_c)
            
        tx = 560
        draw.text((tx, cy + 24), f"實證 {idx+1} ｜ {c_summary}", font=font_sm_bold, fill=C_RUST)
        draw_text_multiline(draw, c_critique, tx, cy + 64, box_w - 520, font_sm, C_INK_MUTED, line_spacing=6)
        
    y += (row_h + 16) * 3 + 12
    
    ana_h = 160
    draw.rounded_rectangle([64, y, 64 + box_w, y + ana_h], radius=14, fill=C_RUST_LIGHT, outline=C_RUST, width=1)
    draw.text((88, y + 18), "手法解析：缺乏生活真實感的套版留言", font=font_body_bold, fill=C_RUST)
    ana_desc = (
        "真實的社群留言充滿在地日常用詞與不同立場的提問。涉案貼文底下的留言帳號與作者迅速拋接既定口號，"
        "對話內容高度公式化、圍繞單一人設打轉，顯得十分不誠懇且缺乏真人味，呈現典型公關帳號一搭一唱的唱和模式。"
    )
    draw_text_multiline(draw, ana_desc, 88, y + 50, box_w - 48, font_sm, C_INK, line_spacing=6)
    
    draw_footer(draw, "05 / 07 ｜ 案例研析報告")
    img.save(output_path, "PNG", quality=95)
    print("Card 05 generated.")

# ==========================================
# CARD 6: METHOD 5 - ALGORITHM POISONING (WITH REAL FRAME SCREENSHOT)
# ==========================================
def generate_card_06(output_path):
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)
    
    y = draw_header(
        draw,
        "METHOD 05 ｜ 演算法毒害分析",
        "境外幽靈灌粉：毒害粉專演算法健康度",
        "大量外國機器人湧入，不僅無法帶來真實支持，更嚴重拉低自然觸及",
        is_alert=True
    )
    
    box_w = WIDTH - 128
    
    # Top Box: With actual video frame screenshot!
    top_h = 300
    draw.rounded_rectangle([64, y, 64 + box_w, y + top_h], radius=16, fill=C_CARD_BG, outline=C_RUST, width=2)
    draw.rounded_rectangle([80, y + 16, 64 + box_w - 16, y + 52], radius=8, fill=C_RUST_LIGHT, outline=C_RUST, width=1)
    draw.text((92, y + 22), "客觀跡證 ｜ 相關官方粉專同期湧入大量境外人頭帳號", font=font_sm_bold, fill=C_RUST)
    
    # Left: video frame screenshot (uncropped, fit inside)
    # Right: bullet points
    frame_w = 460
    img_frame = fit_image_inside("assets/img/bot_frame_10s.png", frame_w - 20, 220)
    if img_frame:
        iw, ih = img_frame.size
        im_x = 80 + (frame_w - iw) // 2
        im_y = y + 66 + (220 - ih) // 2
        draw.rounded_rectangle([78, y + 64, 78 + frame_w, y + 286], radius=8, fill=C_PAPER, outline=C_STONE_LIGHT, width=1)
        img.paste(img_frame, (im_x, im_y), img_frame)
        
    rx = 80 + frame_w + 24
    rw = box_w - (frame_w + 24) - 40
    evidence_points = [
        "・地理嚴重異常：密集出現埃及開羅、瓦加杜古、安特衛普等跨國帳號。",
        "・批次註冊命名：出現多組公式化隨機英數字命名的幽靈人頭。",
        "・大量非受眾名單：短期內集體灌入，呈現人為公關灌水操作特徵。"
    ]
    draw_text_multiline(draw, "\n".join(evidence_points), rx, y + 74, rw, font_sm, C_INK, line_spacing=10)
    
    y += top_h + 20
    
    # Bottom: 3 Algorithmic Damage Cards
    dmg_w = box_w
    dmg_h = 138
    damages = [
        ("A. 抽樣互動崩潰（觸及率直接被拉低）", "發新貼文時系統先推給一小批粉絲測試。當幽靈粉 0 點讚、0 閱讀時，演算法判定貼文連粉絲都不看，大幅壓低自然擴散觸及。"),
        ("B. 受眾輪廓失真（數據徹底失準）", "粉專後台人口統計被非洲、中東無效名單污染，競選團隊無法獲得真實民意數據，廣告相似受眾（Lookalike）亦全面失靈。"),
        ("C. 實質隱性傷害（暗中被演算法扣分）", "雖然真實支持者仍熱情互動，但系統機制上粉專健康度已被持續消耗，嚴重限制了政見向廣大在地中間選民擴散的能量。")
    ]
    
    for idx, (d_title, d_desc) in enumerate(damages):
        dy = y + idx * (dmg_h + 14)
        draw.rounded_rectangle([64, dy, 64 + dmg_w, dy + dmg_h], radius=14, fill=C_CARD_BG, outline=C_STONE_LIGHT, width=1)
        draw.rounded_rectangle([64, dy, 64 + 6, dy + dmg_h], radius=3, fill=C_RUST)
        
        draw.text((88, dy + 16), d_title, font=font_body_bold, fill=C_RUST)
        draw_text_multiline(draw, d_desc, 88, dy + 48, dmg_w - 48, font_sm, C_INK_MUTED, line_spacing=5)
        
    draw_footer(draw, "06 / 07 ｜ 案例研析報告")
    img.save(output_path, "PNG", quality=95)
    print("Card 06 generated.")

# ==========================================
# CARD 7: GUIDE & SUMMARY
# ==========================================
def generate_card_07(output_path):
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)
    
    y = draw_header(
        draw,
        "SUMMARY ｜ 數位公民識讀指南",
        "辨識境外假帳號的三個關鍵數位跡證",
        "面對社群認知操作與社交工程，如何自我查驗、避免被帶風向？"
    )
    
    box_w = WIDTH - 128
    
    guides = [
        ("跡證 1 ｜ 查驗 Meta 官方透明度紀錄", "點擊個人檔案右上角選單，選擇「關於這個帳號」。檢視帳號建立時間、註冊所在地與更名歷史。若自稱是在地生活選民，登記地卻位於南美、中東或非洲，即為重大警訊。", C_MOSS_LIGHT, C_MOSS),
        ("跡證 2 ｜ 反向圖搜頭貼與日常生活照", "利用 Google 圖片搜尋或以圖搜圖工具檢索個人頭貼與日常照。境外網軍為求逼真，常直接盜用外國無辜素人的生活自拍，或使用 AI 生成面孔，一搜便能原形畢露。", C_RUST_LIGHT, C_RUST),
        ("跡證 3 ｜ 檢視發文脈絡與留言互動氛圍", "檢視帳號過往是否長期無生活痕跡、突然密集轉傳特定公關貼文；並觀察留言區是否充滿秒回特定宣傳口號、一搭一唱毫無生活人味的套版對話。", C_MOSS_LIGHT, C_MOSS)
    ]
    
    card_h = 200
    for idx, (g_title, g_desc, bg_col, tag_col) in enumerate(guides):
        gy = y + idx * (card_h + 18)
        draw.rounded_rectangle([64, gy, 64 + box_w, gy + card_h], radius=16, fill=C_CARD_BG, outline=C_STONE_LIGHT, width=1)
        draw.rounded_rectangle([64, gy, 64 + 6, gy + card_h], radius=3, fill=tag_col)
        
        bbox = font_sm_bold.getbbox(g_title)
        draw.rounded_rectangle([88, gy + 18, 88 + (bbox[2]-bbox[0]) + 16, gy + 18 + 30], radius=6, fill=bg_col, outline=tag_col, width=1)
        draw.text((96, gy + 22), g_title, font=font_sm_bold, fill=tag_col)
        
        draw_text_multiline(draw, g_desc, 88, gy + 62, box_w - 48, font_body, C_INK_MUTED, line_spacing=6)
        
    y += (card_h + 18) * 3 + 10
    
    call_h = 130
    draw.rounded_rectangle([64, y, 64 + box_w, y + call_h], radius=14, fill=C_MOSS_LIGHT, outline=C_MOSS, width=1)
    draw.text((88, y + 18), "共同守護健康理性的公共討論空間", font=font_body_bold, fill=C_MOSS)
    call_desc = "健康的民主選舉需要真實的公眾溝通。識破境外人頭帳號與公關套路，拒絕造假與灌粉，讓公共事務回歸真實政策與實質服務。"
    draw_text_multiline(draw, call_desc, 88, y + 52, box_w - 48, font_sm, C_INK, line_spacing=6)
    
    draw_footer(draw, "07 / 07 ｜ 案例研析報告")
    img.save(output_path, "PNG", quality=95)
    print("Card 07 generated.")

def main():
    os.makedirs("比對圖卡", exist_ok=True)
    os.makedirs("assets/img", exist_ok=True)
    
    cards = [
        ("比對圖卡/card_01_cover.png", generate_card_01),
        ("比對圖卡/card_02_identity_theft.png", generate_card_02),
        ("比對圖卡/card_03_location_and_phone.png", generate_card_03),
        ("比對圖卡/card_04_social_engineering_post.png", generate_card_04),
        ("比對圖卡/card_05_comment_manipulation.png", generate_card_05),
        ("比對圖卡/card_06_algorithm_poisoning.png", generate_card_06),
        ("比對圖卡/card_07_citizen_guide.png", generate_card_07)
    ]
    
    for path, gen_func in cards:
        gen_func(path)
        im = Image.open(path)
        webp_path = path.replace(".png", ".webp")
        im.save(webp_path, "WEBP", quality=90)
        
        base_name = os.path.basename(path)
        im.save(os.path.join("assets/img", base_name), "PNG", quality=95)
        im.save(os.path.join("assets/img", base_name.replace(".png", ".webp")), "WEBP", quality=90)
        
    print("All 7 cards regenerated successfully!")

if __name__ == "__main__":
    main()
