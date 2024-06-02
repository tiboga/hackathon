from PIL import Image, ImageDraw, ImageFont


def get_font_size(text, base_size=70):
    if len(text) > 10:
        base_size = max(30, 700 // len(text))
    return base_size


def draw_multiline_text(draw, text, position, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and (draw.textlength(line + ' ' + words[0], font=font) <= max_width):
            line = ' '.join([line, words.pop(0)]).strip()
        lines.append(line)
    y = position[1]
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        x = position[0] + (max_width - width) / 2  # Центрирование по горизонтали
        draw.text((x, y), line, fill="black", font=font)
        y += bbox[3] - bbox[1]


def generate_certificate(name, template_path, output_path):
    """
        Функция для создания грамоты. На вход получает:
        name: str # имя пользователя
        template_path: str # путь до bg
        output_path: str # путь сохранения
        upd: Я закоммичу файл bg сразу
    """
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)

    main_text = "За отличные успехи в решении примеров награждается:"
    name_font_size = get_font_size(name)
    main_text_font_size = get_font_size(main_text, base_size=40)

    name_font = ImageFont.truetype("arial.ttf", name_font_size)
    main_text_font = ImageFont.truetype("arial.ttf", main_text_font_size)

    width, height = template.size
    max_text_width = width - 100

    main_text_position = (50, height * 0.4)
    draw_multiline_text(draw, main_text, main_text_position, main_text_font, max_text_width)

    name_bbox = draw.textbbox((0, 0), name, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_height = name_bbox[3] - name_bbox[1]
    name_position = ((width - name_width) / 2, main_text_position[1] + 150)  # Смещение имени ниже

    draw.text(name_position, name, fill="black", font=name_font)

    template.save(output_path)


# template_path = "Pinterest_Download (3).jpg"
# output_path = "certificate.png"
# name = "Александр Булгаков"
# generate_certificate(name, template_path, output_path)
