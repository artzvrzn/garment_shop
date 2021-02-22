from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_tab'),
]
