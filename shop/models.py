import os
from django.db import models


def upload_path(instance, filename):
    name, extension = filename.split('.')
    path_name = os.path.join('images', f'{instance.category}', f'image_{instance.pk}.{extension}')
    return path_name


class Item(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    desc = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    image = models.ImageField(upload_to=upload_path, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


