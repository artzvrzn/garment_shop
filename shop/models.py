import os
from io import BytesIO
from PIL import Image
from django.db import models
from django.urls import reverse
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
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __call__(self, instance, filename):
        name, extension = filename.split('.')
        path_name = os.path.join(f'{self.path}', f'{instance.category}', f'{self.name}_{instance.id}.{extension}')
        return path_name


class Item(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    desc = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    image = models.ImageField(upload_to=Upload('image', path='images'), blank=True)
    thumbnail = models.ImageField(upload_to=Upload('thumbnail', path='thumbnails'), editable=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # solution to get db id before saving image, so there wouldn't be None in its name
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = saved_image
        # here image is getting resized and getting thumbnail
        self.thumb_creator()
        super().save(*args, **kwargs)

    def thumb_creator(self):
        img = Image.open(self.image)
        file_path, file_ext = os.path.splitext(self.image.name)
        img_cropped = image_crop(img, min(img.size), min(img.size))
        img_resized = img_cropped.resize((300, 300))
        # saving image to the memory
        temp_thumb = BytesIO()
        if file_ext == '.jpg':
            file_ext = 'JPEG'
        else:
            file_ext = file_ext[1:]
        img_resized.save(temp_thumb, file_ext)
        # saving obtained image to the thumbnail ImageField (path, file, save=False).
        # not setting save to False will save image immediately, as a result thumb will be saved before main image
        # uploaded
        self.thumbnail.save(self.image.name, ContentFile(temp_thumb.getvalue()), save=False)
        temp_thumb.close()


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_tab', kwargs={'category_id': self.pk})


class SubCategory(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# UNSAVED = 'unsaved'


# @receiver(pre_save, sender=Item)
# def skip_saving(sender, instance, **kwargs):
#     if not instance.pk and not hasattr(instance, UNSAVED):
#         setattr(instance, UNSAVED, instance.image)
#         instance.image = None
#
#
# @receiver(post_save, sender=Item)
# def save_file(sender, instance, created, **kwargs):
#     if created and hasattr(instance, UNSAVED):
#         instance.image = getattr(instance, UNSAVED)
#         instance.save()


