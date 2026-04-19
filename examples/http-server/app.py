"""
pi-captcha HTTP example server
"""
import json
import sys
import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from PIL import Image

# debug lib
BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pi_captcha import ClickBuilder, RotateBuilder, SlideBuilder
from pi_captcha.base import option
from pi_captcha.click import validate as click_validate
from pi_captcha.rotate import validate as rotate_validate
from pi_captcha.slide import validate as slide_validate
from pi_captcha.slide.block import GraphImage

app = Flask(__name__)
CORS(app)

captcha_store: dict[str, dict] = {}

ASSETS_DIR = BASE_DIR / 'assets'
WEB_DIR = BASE_DIR / 'web'
IMAGE_DIR = ASSETS_DIR / 'images'
THUMB_DIR = ASSETS_DIR / 'thumbs'
FONT_DIR = ASSETS_DIR / 'fonts'
TILE_DIR = ASSETS_DIR / 'tiles'
CHARS_FILE = ASSETS_DIR / 'chars' / 'char.json'


def success_response(**payload):
    data = {'code': 0}
    data.update(payload)
    return jsonify(data)


def error_response(message: str, status_code: int = 400):
    return jsonify({'code': 1, 'message': message}), status_code


def load_images_from_dir(directory: Path, filename: str) -> list[Image.Image]:
    images = []
    if directory.exists():
        for subdir in sorted(directory.iterdir()):
            file_path = subdir / filename
            if subdir.is_dir() and file_path.exists():
                images.append(Image.open(file_path))
    return images


def load_font_paths(directory: Path, filename: str = 'font.ttf') -> list[str]:
    font_paths = []
    if directory.exists():
        for subdir in sorted(directory.iterdir()):
            file_path = subdir / filename
            if subdir.is_dir() and file_path.exists():
                font_paths.append(str(file_path))
    return font_paths


def load_chars_from_json() -> list[str]:
    if CHARS_FILE.exists():
        try:
            with open(CHARS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'chars' in data:
                    return data['chars']
        except Exception:
            pass
    return []


def build_slide_graph_images() -> list[GraphImage]:
    graph_images = []
    if TILE_DIR.exists():
        for subdir in sorted(TILE_DIR.iterdir()):
            if not subdir.is_dir():
                continue
            overlay_path = subdir / 'tile.png'
            shadow_path = subdir / 'tile-shadow.png'
            mask_path = subdir / 'tile-mask.png'
            if overlay_path.exists() and shadow_path.exists() and mask_path.exists():
                graph_image = GraphImage()
                graph_image.overlay_image = Image.open(overlay_path)
                graph_image.shadow_image = Image.open(shadow_path)
                graph_image.mask_image = Image.open(mask_path)
                graph_images.append(graph_image)
    return graph_images


def get_backgrounds() -> list[Image.Image]:
    backgrounds = load_images_from_dir(IMAGE_DIR, 'image.jpg')
    return backgrounds or [Image.new('RGB', (300, 220), color=(255, 255, 255))]


def get_thumb_backgrounds() -> list[Image.Image]:
    thumb_backgrounds = load_images_from_dir(THUMB_DIR, 'thumb.jpg')
    return thumb_backgrounds or [Image.new('RGB', (150, 40), color=(255, 255, 255))]


def get_click_fonts() -> list[str]:
    return load_font_paths(FONT_DIR)


def new_captcha_key() -> str:
    return str(uuid.uuid4())


def store_captcha(captcha_type: str, payload: dict) -> str:
    captcha_key = new_captcha_key()
    captcha_store[captcha_key] = {
        'type': captcha_type,
        **payload,
    }
    return captcha_key


def pop_captcha(captcha_key: str) -> dict | None:
    return captcha_store.pop(captcha_key, None)


def get_form_value(name: str, default=''):
    return request.form.get(name, default)


def parse_int(value, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default


def parse_csv_ints(value: str) -> list[int]:
    if not value:
        return []
    values = []
    for item in value.split(','):
        item = item.strip()
        if not item:
            continue
        values.append(parse_int(item))
    return values


def parse_point(value: str) -> tuple[int, int] | None:
    nums = parse_csv_ints(value)
    if len(nums) != 2:
        return None
    return nums[0], nums[1]


def get_click_builder() -> ClickBuilder:
    builder = ClickBuilder(
        ClickBuilder.with_range_len(option.RangeVal(min_val=4, max_val=6)),
        ClickBuilder.with_range_verify_len(option.RangeVal(min_val=2, max_val=4)),
    )
    chars = load_chars_from_json()
    if not chars:
        chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    builder.set_resources(
        ClickBuilder.with_chars(chars),
        ClickBuilder.with_fonts(get_click_fonts()),
        ClickBuilder.with_backgrounds(get_backgrounds()),
        ClickBuilder.with_thumb_backgrounds(get_thumb_backgrounds()),
    )
    return builder


def get_slide_builder() -> SlideBuilder:
    builder = SlideBuilder()
    builder.set_resources(
        SlideBuilder.with_backgrounds(get_backgrounds()),
        SlideBuilder.with_graph_images(build_slide_graph_images()),
    )
    return builder


def get_rotate_builder() -> RotateBuilder:
    builder = RotateBuilder()
    builder.set_resources(
        RotateBuilder.with_images(get_backgrounds()),
    )
    return builder


@app.route('/')
def index():
    return send_from_directory(WEB_DIR, 'index.html')


@app.route('/web')
@app.route('/web/')
def web_index():
    return send_from_directory(WEB_DIR, 'index.html')


@app.route('/<path:filename>')
def web_static(filename: str):
    file_path = WEB_DIR / filename
    if file_path.is_file():
        return send_from_directory(WEB_DIR, filename)
    abort(404)


@app.route('/api/captcha/click/generate', methods=['GET'])
def click_generate():
    try:
        captcha_data = get_click_builder().make().generate()
        dots = captcha_data.get_data()
        ordered_dots = [dots[idx] for idx in sorted(dots.keys())]
        captcha_key = store_captcha(
            'click',
            {
                'dots': [
                    {
                        'index': dot.index,
                        'x': dot.x,
                        'y': dot.y,
                        'width': dot.width,
                        'height': dot.height,
                    }
                    for dot in ordered_dots
                ],
            },
        )

        return success_response(
            image_base64=captcha_data.get_master_image().to_base64(),
            thumb_base64=captcha_data.get_thumb_image().to_base64(),
            captcha_key=captcha_key,
        )
    except Exception as exc:
        return error_response(str(exc), 500)


@app.route('/api/captcha/click/verify', methods=['POST'])
def click_verify():
    captcha_key = get_form_value('key')
    captcha = captcha_store.get(captcha_key)
    if not captcha or captcha.get('type') != 'click':
        return error_response('Captcha does not exist or has expired')

    dots = captcha.get('dots', [])
    points = parse_csv_ints(get_form_value('dots'))
    if len(points) != len(dots) * 2:
        return error_response('Click count mismatch')

    for idx, dot in enumerate(dots):
        point_x = points[idx * 2]
        point_y = points[idx * 2 + 1]
        if not click_validate(point_x, point_y, dot['x'], dot['y'], dot['width'], dot['height'], 5):
            pop_captcha(captcha_key)
            return error_response('Verification failed')

    pop_captcha(captcha_key)
    return success_response(message='Verification successful')


@app.route('/api/captcha/slide/generate', methods=['GET'])
def slide_generate():
    try:
        captcha_data = get_slide_builder().make().generate()
        block = captcha_data.get_data()
        captcha_key = store_captcha(
            'slide',
            {
                'dx': block.dx,
                'dy': block.dy,
            },
        )

        return success_response(
            image_base64=captcha_data.get_master_image().to_base64(),
            tile_base64=captcha_data.get_tile_image().to_base64(),
            tile_x=block.tile_x,
            tile_y=block.tile_y,
            tile_width=block.width,
            tile_height=block.height,
            captcha_key=captcha_key,
        )
    except Exception as exc:
        return error_response(str(exc), 500)


@app.route('/api/captcha/slide/region/generate', methods=['GET'])
def slide_region_generate():
    try:
        captcha_data = get_slide_builder().make_drag_drop().generate()
        block = captcha_data.get_data()
        captcha_key = store_captcha(
            'slide_region',
            {
                'dx': block.dx,
                'dy': block.dy,
            },
        )

        return success_response(
            image_base64=captcha_data.get_master_image().to_base64(),
            tile_base64=captcha_data.get_tile_image().to_base64(),
            tile_x=block.tile_x,
            tile_y=block.tile_y,
            tile_width=block.width,
            tile_height=block.height,
            captcha_key=captcha_key,
        )
    except Exception as exc:
        return error_response(str(exc), 500)


@app.route('/api/captcha/slide/verify', methods=['POST'])
def slide_verify():
    captcha_key = get_form_value('key')
    captcha = captcha_store.get(captcha_key)
    if not captcha or captcha.get('type') not in {'slide', 'slide_region'}:
        return error_response('Captcha does not exist or has expired')

    point = parse_point(get_form_value('point'))
    if point is None:
        return error_response('Invalid slide coordinates')

    if not slide_validate(point[0], point[1], captcha['dx'], captcha['dy'], 5):
        pop_captcha(captcha_key)
        return error_response('Verification failed')

    pop_captcha(captcha_key)
    return success_response(message='Verification successful')


@app.route('/api/captcha/rotate/generate', methods=['GET'])
def rotate_generate():
    try:
        captcha_data = get_rotate_builder().make().generate()
        block = captcha_data.get_data()
        captcha_key = store_captcha(
            'rotate',
            {
                'angle': block.angle,
                'thumb_size': block.width,
            },
        )

        return success_response(
            image_base64=captcha_data.get_master_image().to_base64(),
            thumb_base64=captcha_data.get_thumb_image().to_base64(),
            thumb_size=block.width,
            captcha_key=captcha_key,
        )
    except Exception as exc:
        return error_response(str(exc), 500)


@app.route('/api/captcha/rotate/verify', methods=['POST'])
def rotate_verify():
    captcha_key = get_form_value('key')
    captcha = captcha_store.get(captcha_key)
    if not captcha or captcha.get('type') != 'rotate':
        return error_response('Captcha does not exist or has expired')

    angle = parse_int(get_form_value('angle'))
    if not rotate_validate(angle, captcha['angle'], 10):
        pop_captcha(captcha_key)
        return error_response('Verification failed')

    pop_captcha(captcha_key)
    return success_response(message='Verification successful')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
