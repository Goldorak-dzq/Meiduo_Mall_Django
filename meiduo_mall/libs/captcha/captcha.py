#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
import os.path
from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageTransform, ImageFont
from PIL.Image import Resampling

class Bezier:
    def __init__(self):
        self.tsequence = tuple([t / 20.0 for t in range(21)])
        self.beziers = {}

    def pascal_row(self, n):
        result = [1]
        x, numerator = 1, n
        for denominator in range(1, n // 2 + 1):
            x *= numerator
            x /= denominator
            result.append(x)
            numerator -= 1
        if n & 1 == 0:
            result.extend(reversed(result[:-1]))
        else:
            result.extend(reversed(result))
        return result

    def make_bezier(self, n):
        try:
            return self.beziers[n]
        except KeyError:
            combinations = self.pascal_row(n - 1)
            result = []
            for t in self.tsequence:
                tpowers = (t ** i for i in range(n))
                upowers = ((1 - t) ** i for i in range(n - 1, -1, -1))
                coefs = [c * a * b for c, a, b in zip(combinations,
                                                      tpowers, upowers)]
                result.append(coefs)
            self.beziers[n] = result
            return result


class Captcha(object):
    def __init__(self):
        self._bezier = Bezier()
        self._dir = os.path.dirname(__file__)

    @staticmethod
    def instance():
        if not hasattr(Captcha, "_instance"):
            Captcha._instance = Captcha()
        return Captcha._instance

    def initialize(self, width=200, height=75, color=None, text=None, fonts=None):
        self._text = text if text else random.sample(string.ascii_uppercase + string.ascii_uppercase + '3456789', 4)
        self.fonts = fonts if fonts else \
            [os.path.join(self._dir, 'fonts', font) for font in ['Arial.ttf', 'Georgia.ttf', 'actionj.ttf']]
        self.width = width
        self.height = height
        self._color = color if color else self.random_color(0, 200, random.randint(220, 255))

    @staticmethod
    def random_color(start, end, opacity=None):
        red = random.randint(start, end)
        green = random.randint(start, end)
        blue = random.randint(start, end)
        if opacity is None:
            return red, green, blue
        return red, green, blue, opacity

    def background(self, image):
        ImageDraw.Draw(image).rectangle([(0, 0), image.size], fill=self.random_color(238, 255))
        return image

    @staticmethod
    def smooth(image):
        return image.filter(ImageFilter.SMOOTH)

    def curve(self, image, width=4, number=6, color=None):
        dx, height = image.size
        dx /= number
        path = [(dx * i, random.randint(0, height)) for i in range(1, number)]
        bcoefs = self._bezier.make_bezier(number - 1)
        points = []
        for coefs in bcoefs:
            points.append(tuple(sum([coef * p for coef, p in zip(coefs, ps)]) for ps in zip(*path)))
        ImageDraw.Draw(image).line(points, fill=color if color else self._color, width=width)
        return image

    def noise(self, image, number=50, level=2, color=None):
        width, height = image.size
        dx = width / 10
        width -= dx
        dy = height / 10
        height -= dy
        draw = ImageDraw.Draw(image)
        for i in range(number):
            x = int(random.uniform(dx, width))
            y = int(random.uniform(dy, height))
            draw.line(((x, y), (x + level, y)), fill=color if color else self._color, width=level)
        return image

    def text(self, image, fonts, font_sizes=None, drawings=None, squeeze_factor=0.75, color=None):
        color = color if color else self._color
        fonts = tuple([ImageFont.truetype(name, size) for name in fonts for size in font_sizes or (65, 70, 75)])
        draw = ImageDraw.Draw(image)
        char_images = []
        for c in self._text:
            font = random.choice(fonts)
            # 使用textbbox获取文本尺寸
            # 修改后的代码片段
            bbox = draw.textbbox((0, 0), c, font=font)
            c_width = max(1, int(bbox[2] - bbox[0]))  # 强制转int并确保≥1
            c_height = max(1, int(bbox[3] - bbox[1]))  # 强制转int并确保≥1
            char_image = Image.new('RGB', (c_width, c_height), (0, 0, 0))
            char_draw = ImageDraw.Draw(char_image)
            char_draw.text((-bbox[0], -bbox[1]), c, font=font, fill=color)
            char_image = char_image.crop(char_image.getbbox())
            for drawing in drawings:
                d = getattr(self, drawing)
                char_image = d(char_image)
            char_images.append(char_image)
        width, height = image.size
        offset = int((width - sum(int(i.size[0] * squeeze_factor) for i in char_images[:-1]) - char_images[-1].size[0]) / 2)
        for char_image in char_images:
            c_width, c_height = char_image.size
            mask = char_image.convert('L').point(lambda i: i * 1.97)
            image.paste(char_image, (offset, int((height - c_height) / 2)), mask)
            offset += int(c_width * squeeze_factor)
        return image

    @staticmethod
    def warp(image, dx_factor=0.27, dy_factor=0.21):
        width, height = image.size
        dx = width * dx_factor
        dy = height * dy_factor
        x1 = int(random.uniform(-dx, dx))
        y1 = int(random.uniform(-dy, dy))
        x2 = int(random.uniform(-dx, dx))
        y2 = int(random.uniform(-dy, dy))
        image2 = Image.new('RGB', (width + abs(x1) + abs(x2), height + abs(y1) + abs(y2)))
        image2.paste(image, (abs(x1), abs(y1)))
        width2, height2 = image2.size
        return image2.transform(
            (width, height),
            ImageTransform.QuadTransform(
                (x1, y1,
                 -x1, height2 - y2,
                 width2 + x2, height2 + y2,
                 width2 - x2, -y1)
            )
        )

    @staticmethod
    def offset(image, dx_factor=0.1, dy_factor=0.2):
        width, height = image.size
        dx = int(random.random() * width * dx_factor)
        dy = int(random.random() * height * dy_factor)
        image2 = Image.new('RGB', (width + dx, height + dy))
        image2.paste(image, (dx, dy))
        return image2

    @staticmethod
    def rotate(image, angle=25):
        return image.rotate(
            random.uniform(-angle, angle),
            resample=Resampling.BILINEAR,
            expand=1
        )

    def captcha(self, path=None, fmt='JPEG'):
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        image = self.background(image)
        image = self.text(image, self.fonts, drawings=['warp', 'rotate', 'offset'])
        image = self.curve(image)
        image = self.noise(image)
        image = self.smooth(image)
        text = "".join(self._text)
        out = BytesIO()
        image.save(out, format=fmt)
        return text, out.getvalue()

    def generate_captcha(self):
        self.initialize()
        return self.captcha("")

captcha = Captcha.instance()

if __name__ == '__main__':
    print(captcha.generate_captcha())