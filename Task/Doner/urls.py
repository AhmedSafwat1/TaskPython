from django.urls import path

from .views import *

app_name = "Doner"
urlpatterns = [
    path('', index),

]
