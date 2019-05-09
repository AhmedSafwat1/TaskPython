from django.urls import path

from .views import *

app_name = "Hospital"
urlpatterns = [
    path('', index),
    path("bank/search", search, name="searching"),
    path("make/order/<int:bid>", order, name="makeOrder"),
    path("make/order/", order2, name="makeOrder2"),
    path("make/order/request", order3, name="makerequest")
]
