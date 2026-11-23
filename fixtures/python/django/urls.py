from django.http import HttpResponse
from django.urls import path


def get_order(request, order_id):
    return HttpResponse(order_id)


urlpatterns = [path("release/orders/<int:order_id>", get_order)]
