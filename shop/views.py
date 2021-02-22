from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from .models import Item, Category, SubCategory


class IndexView(ListView):
    model = Item
    template_name = 'shop/index.html'
    queryset = Item.objects.filter(available=True).select_related('category', 'subcategory')


class CategoryView(ListView):
    model = Item
    template_name = 'shop/index.html'

    def get_queryset(self):
        print(self.kwargs)
        queryset = Item.objects.filter(category_id=self.kwargs['category_id'], available=True)
        return queryset.select_related('category', 'subcategory')
