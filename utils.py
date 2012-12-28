# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw
from random import randint
from time import sleep

class ImageDestory:
    
    def __init__(self, imagepath):
        self.img = Image.open(imagepath)
        self.img.x, self.img.y = self.img.size 

    def _select_rotate(self):
        target = randint(0, 3)
        if target == 1:
            return Image.ROTATE_90
        elif target == 2:
            return Image.ROTATE_180
        elif target == 3:
            return Image.ROTATE_270
        return False

    def random_convert(self):
        target = randint(0, 2)
        if target == 1:
            img = self.img.convert("1")
        elif target == 2:
            img = self.img.convert("L")
        self.img = self.img.convert("RGB")

    def _get_rgb(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

    def random_draw_line_noise(self, noise=True):
        self._do_draw_line(self.img, max_line=50, noise=True)

    def _do_draw_line(self, canvas, max_line=5, noise=False):
        def __gen_random(canvas_x, noise):
            x = {}
            if noise:
                x["fst"] = randint(canvas.x * -1, canvas.x * 2)
                x["snd"] = randint(canvas.x * -1, canvas.x * 2)
            else:
                x["fst"] = 0
                x["snd"] = canvas.x
            return x

        def __draw_line(draw, x, line=0):
            draw.line(
                [(x["fst"], target + line), (x["snd"], target + line)],
                fill=self._get_rgb())

        canvas.x, canvas.y = canvas.size
        draw = ImageDraw.Draw(canvas)
        for times in range(randint (max_line / 2, max_line)):
            target = randint(0, canvas.x )
            x = __gen_random(canvas.x, noise)
            if noise:
                for line in range(randint(0, 3)):
                    __draw_line(draw, x)
            else: 
                for line in range(randint(0, 10)):
                    __draw_line(draw, x, line)
        del draw
        return canvas

    def random_rotate(self):
        select_rotate = self._select_rotate()
        if select_rotate:
            self.img = self.img.transpose(select_rotate)
    
    def _make_background(self):
        ground = Image.new("RGB", self.img.size, (0, 0, 0))
        ground.putalpha(Image.new("L", self.img.size, 1))
        return ground

    def random_shadow_line(self):
        image = self.img
        self._set_mask(image)

        background = self._make_background()
        background = self._do_draw_line(background, 50)
        self.img = Image.blend(
                image, background, 0.05).convert("RGB")

    def _set_mask(self, image):
        mask = Image.new("L", image.size, 1)
        image.putalpha(mask)
        return image

    def _get_rect(self, x, start_y, height):
        background = self._make_background()
        draw = ImageDraw.Draw(background)
        draw.rectangle((0, start_y, x, start_y + height), fill=self._get_rgb()) 
        del draw
        return background

    def random_color(self, start_y=0):
        # TODO: 範囲をnつにわけて四角を生成する
        image = self.img
        x, max_y = self.img.size
        self._set_mask(image)
        
        if max_y - start_y <= 10:
            height = max_y - start_y
        else:
            height = randint(10, max_y - start_y)
        
        background = self._get_rect(x, start_y, height)
        self.img = Image.blend(
                image, background, 0.08).convert("RGB")
        if start_y + height < max_y:
            self.random_color(start_y=start_y + height)

    def random_shadow(self):
        image = self.img
        mask = Image.new("L", self.img.size, 1)
        cut_image = image.crop((0, 0, 140, 140))
        image = self.img
        image.putalpha(mask)
        for x in range(6):
            shadow_image = self._make_background()
            shadow_image.paste(cut_image, ( -1 * (x * 5), 0))
            self.img = Image.blend(
                shadow_image, image, 0.75).convert("RGB")

    def random_cut_paste(self):
        image = self.img
        target_y = 0
        while target_y < self.img.y:
            height = randint(1, 10)
            if height > self.img.y:
                height = self.img.y - target_y
            box = (0, target_y, self.img.x, target_y + height)
            cut_image = image.crop(box)
            fix_x = randint(-20, 20)
            image.paste(cut_image, (fix_x, target_y))
            target_y = target_y + height
        self.img = image

    def save(self, imagepath):
        self.img.save(imagepath, "JPEG")

def module_test_main():
    img = ImageDestory("base.jpg")
    img.random_cut_paste()
    img.random_shadow()
    img.random_shadow_line()
    #img.random_rotate()
    img.random_convert()
    img.random_shadow_line()
    img.random_color()
    img.random_draw_line_noise()
    img.save("profile.jpg")

if __name__ == "__main__":
    for i in range(100):
        sleep(0.5)
        module_test_main()
