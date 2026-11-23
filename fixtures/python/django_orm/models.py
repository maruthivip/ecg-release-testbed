from django.db import models


class Order(models.Model):
    total = models.IntegerField()


def find_order(order_id: int):
    return Order.objects.get(pk=order_id)
