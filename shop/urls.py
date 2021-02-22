from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_tab'),
    path('item/<int:item_pk>', ItemView.as_view(), name='item'),
]
