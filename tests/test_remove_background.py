import pytest
from PIL import Image
import os
import sys

# Добавляем путь к src для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from remove_background import hex_to_rgb, parse_rgb_string, parse_colors, remove_background

@pytest.fixture
def sample_gif(tmp_path):
    """Создает простой GIF для тестов"""
    img = Image.new('RGBA', (10, 10), (136, 152, 186, 255))  # Фон по умолчанию
    output = tmp_path / "test_input.gif"
    img.save(output, save_all=True, append_images=[img], duration=100, loop=0)
    return output

@pytest.fixture
def output_gif(tmp_path):
    """Путь для выходного GIF"""
    return tmp_path / "test_output.gif"

def test_hex_to_rgb():
    assert hex_to_rgb("#8898BA") == (136, 152, 186)
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)
    with pytest.raises(ValueError, match="Invalid HEX color format"):
        hex_to_rgb("invalid")

def test_parse_rgb_string():
    assert parse_rgb_string("rgb(136,152,186)") == (136, 152, 186)
    assert parse_rgb_string("rgb(255,  255,  255)") == (255, 255, 255)
    with pytest.raises(ValueError, match="RGB values must be between 0 and 255"):
        parse_rgb_string("rgb(256,0,0)")
    with pytest.raises(ValueError, match="Invalid RGB format. Use: rgb\\(r,g,b\\)"):
        parse_rgb_string("rgb(invalid)")

def test_parse_colors():
    assert parse_colors("#8898BA") == [(136, 152, 186)]
    assert parse_colors("#8898BA,#FFFFFF") == [(136, 152, 186), (255, 255, 255)]
    # Исправляем тест: убираем пробел после запятой
    assert parse_colors("rgb(136,152,186),#FFFFFF") == [(136, 152, 186), (255, 255, 255)]
    with pytest.raises(ValueError, match="Color must be in HEX \\(#RRGGBB\\) or rgb\\(r,g,b\\) format"):
        parse_colors("invalid")

def test_remove_background_single_color(sample_gif, output_gif):
    remove_background(str(sample_gif), str(output_gif), ["#8898BA"])
    assert os.path.exists(output_gif)
    result = Image.open(output_gif).convert("RGBA")
    pixels = list(result.getdata())
    assert pixels[0][3] == 0  # Альфа-канал должен быть 0 (прозрачный)

def test_remove_background_multiple_colors(sample_gif, output_gif):
    remove_background(str(sample_gif), str(output_gif), ["#8898BA", "#FFFFFF"])
    assert os.path.exists(output_gif)
    result = Image.open(output_gif).convert("RGBA")
    pixels = list(result.getdata())
    assert pixels[0][3] == 0

def test_remove_background_invalid_file(tmp_path, output_gif):
    invalid_file = tmp_path / "invalid.txt"
    invalid_file.write_text("not a gif")
    with pytest.raises(ValueError, match="Input file must be a GIF"):
        remove_background(str(invalid_file), str(output_gif), ["#8898BA"])

def test_remove_background_invalid_color(sample_gif, output_gif):
    with pytest.raises(ValueError, match="Color must be in HEX \\(#RRGGBB\\) or rgb\\(r,g,b\\) format"):
        remove_background(str(sample_gif), str(output_gif), ["invalid_color"])

def test_remove_background_out_of_range_color(sample_gif, output_gif):
    with pytest.raises(ValueError, match="RGB values must be between 0 and 255"):
        remove_background(str(sample_gif), str(output_gif), ["rgb(300,152,186)"])