import pytest
from PIL import Image
import numpy as np
from app.utils.preprocess import resize_to_max_width, to_grayscale, enhance_contrast, preprocess


def make_rgb_image(width: int, height: int) -> Image.Image:
    arr = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    return Image.fromarray(arr, mode="RGB")


class TestResizeToMaxWidth:
    def test_no_resize_when_within_limit(self):
        img = make_rgb_image(800, 600)
        result = resize_to_max_width(img, max_width=1024)
        assert result.width == 800
        assert result.height == 600

    def test_downscales_preserving_aspect_ratio(self):
        img = make_rgb_image(2048, 1024)
        result = resize_to_max_width(img, max_width=1024)
        assert result.width == 1024
        assert result.height == 512

    def test_does_not_upscale(self):
        img = make_rgb_image(100, 50)
        result = resize_to_max_width(img, max_width=1024)
        assert result.width == 100


class TestToGrayscale:
    def test_converts_to_mode_l(self):
        img = make_rgb_image(200, 100)
        result = to_grayscale(img)
        assert result.mode == "L"

    def test_preserves_dimensions(self):
        img = make_rgb_image(200, 100)
        result = to_grayscale(img)
        assert result.size == (200, 100)


class TestPreprocess:
    def test_full_pipeline_returns_grayscale(self):
        img = make_rgb_image(2000, 1000)
        result = preprocess(img)
        assert result.mode == "L"
        assert result.width <= 1024
