import os
from io import BytesIO
from PIL import Image
from django.db import models
from django.utils.deconstruct import deconstructible
from django.core.files.base import ContentFile


def image_crop(img, crop_width, crop_height):
    width, height = img.size
    x = (width - crop_width) // 2
    y = (height - crop_height) // 2
    x1 = (width + crop_width) // 2
    y1 = (height + crop_height) // 2
    return img.crop((x, y, x1, y1))


# deconstructible decorator helps to avoid errors during migrations
@deconstructible
class Upload:
    def __init__(self, name):
        self.name = name

    def __call__(self, instance, filename):
        try:
            name, extension = filename.split('.')
            path_name = os.path.join('images', f'{instance.category}', f'{self.name}_{instance.id}.{extension}')
        except ValueError:
            print('Filename for thumbnail is absent, getting name from uploaded image')
            path_name = os.path.join('images', f'{instance.category}', f'{instance.image.name}')
        return path_name


class Item(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    desc = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    image = models.ImageField(upload_to=Upload('image'), blank=True)
    thumbnail = models.ImageField(upload_to=Upload('thumbnail'), editable=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.thumb_creator()
        super().save(*args, **kwargs)

    def thumb_creator(self):
        img = image_crop(Image.open(self.image), 300, 300)
        # saving image to the memory
        temp_thumb = BytesIO()
        img.save(temp_thumb, 'JPEG')
        # saving obtained image to the thumbnail ImageField (path, file, save=False).
        # not setting save to False will save image immediately, as a result thumb will be saved before main image
        # uploaded
        self.thumbnail.save(self.thumbnail.name, ContentFile(temp_thumb.getvalue()), save=False)
        temp_thumb.close()


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


