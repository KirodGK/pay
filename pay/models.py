from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

    def total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total *= (1 - self.discount.percent_off / 100)
        if self.tax:
            total *= (1 + self.tax.percentage / 100)
        return round(total, 2)

    def total_price_cents(self):
        return int(self.total_price() * 100)