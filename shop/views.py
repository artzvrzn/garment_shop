from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from .models import Item, Category, SubCategory


class IndexView(ListView):
    model = Item
    template_name = 'shop/index.html'
    queryset = Item.objects.filter(available=True).select_related('category', 'subcategory')



