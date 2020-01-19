import os

from PIL import Image, ImageDraw, ImageFont


WATERMARK_POSITION = (
    "top left",
    "top right",
    "center",
    "bottom left",
    "bottom right",
)


class CustomImage:
    """The CustomImage class implements the image watermark operation.

    Attributes:
        **image** *(Image)*: The image object from PIL.

        **width** *(int)*: The width of the image.

        **height** *(int)*: The height of the image.

        **path** *(str)*: The path of the image.

        **margin** *(int)*: The margin between the image border and the watermark.

        **output_path** *(str)*: The path of the watermarked image.
    """

    def __init__(self, path, margin=25, folder="output"):
        """The constructor of the custom image object.

        :param path: The path of the image file.
        :param margin: The margin between the image border and the watermark.
        :param folder: The name of the output folder.
        :type path: str
        :type margin: int
        :type folder: str
        """
        self.image = Image.open(path)
        self.width, self.height = self.image.size
        self.path = path
        self.margin = margin
        self.output_path = os.path.join(os.path.dirname(self.path),
                                        folder,
                                        os.path.basename(self.path))

    def watermark_text(self, text, color, font_type, font_size, pos_name):
        """Write text on the image.

        :param text: The text to write on the image.
        :param color: The color of the text.
        :param font_type: The font type of the text.
        :param font_size: The font size of the text.
        :param pos_name: The position name of the text.
        :type text: str
        :type color: (int, int, int)
        :type font_type: str
        :type font_size: int
        :type pos_name: str

        :return: True if the path of the reduced image exists else False.
        :rtype: bool
        """
        image = Image.open(self.path)
        drawing = ImageDraw.Draw(image)
        text = text
        font = ImageFont.truetype(font_type, font_size)
        self.watermark_width, self.watermark_height = drawing.textsize(text, font)
        pos = self.watermark_position(pos_name)

        drawing.text(pos, text, fill=color, font=font)
        parent_dir = os.path.dirname(self.output_path)

        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        image.save(self.output_path)
        return os.path.exists(self.output_path)

    def watermark_image(self, watermark_path, pos_name):
        """Add an image watermark on the image.
        Supports only PNG and JPG files.

        :param watermark_path: The path of the image watermark.
        :param pos_name: The position name of the image watermark.
        :type watermark_path: str
        :type pos_name: str

        :return: True if the path of the reduced image exists else False.
        :rtype: bool
        """
        image = Image.open(self.path)
        watermark = Image.open(watermark_path)
        self.watermark_width, self.watermark_height = watermark.size
        pos = self.watermark_position(pos_name)

        parent_dir = os.path.dirname(self.output_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        watermark_ext = os.path.splitext(watermark_path)[-1]
        if watermark_ext in (".png", ".PNG"):
            transparent = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            transparent.paste(image, (0, 0))
            transparent.paste(watermark, pos, mask=watermark)
            self.output_path = ".".join([os.path.splitext(self.output_path)[0], "png"])
            transparent.save(self.output_path)
        elif watermark_ext in (".jpg", ".JPG", ".jpeg", ".JPEG"):
            image.paste(watermark, pos)
            image.save(self.output_path)

        return os.path.exists(self.output_path)

    def watermark_position(self, pos_name):
        if pos_name == "top left":
            return self.margin, self.margin
        if pos_name == "top right":
            return self.width - self.margin - self.watermark_width, self.margin
        if pos_name == "center":
            return (round(self.width/2) - round(self.watermark_width/2),
                    round(self.height/2) - round(self.watermark_height/2))
        if pos_name == "bottom left":
            return self.margin, self.height - self.margin - self.watermark_height
        if pos_name == "bottom right":
            return self.width - self.margin - self.watermark_width, self.height - self.margin - self.watermark_height


if __name__ == '__main__':
    img1 = CustomImage("F:/Workspaces/devenv/qt_for_python/source/_sample_images/bretagne-01.jpg")
    # img1.watermark_text(text="My watermark",
    #                     color=(0, 0, 0),
    #                     font_type="C:/Windows/Fonts/arial.ttf",
    #                     font_size=700,
    #                     pos_name="center")
    img1.watermark_image(watermark_path="F:/Workspaces/devenv/qt_for_python/source/_sample_images/python.png",
                         pos_name="center")
    img2 = CustomImage("F:/Workspaces/devenv/qt_for_python/source/_sample_images/bretagne-02.jpg")
    img2.watermark_image(watermark_path="F:/Workspaces/devenv/qt_for_python/source/_sample_images/python.jpg",
                         pos_name="top right")
