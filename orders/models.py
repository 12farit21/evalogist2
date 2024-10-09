from django.db import models


class Order(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name='Номер заказа'  # Отображаемое имя в админке и формах
    )
    full_name = models.CharField('ФИО',max_length=250)
    company_name = models.CharField('Компания (Опционально)',max_length=250,blank=True)
    email = models.EmailField('Почта')
    phone = models.CharField('Номер',max_length=100)
    address = models.CharField('Адрес',max_length=250)
    postal_code = models.CharField('Почтовый индекс',max_length=20)
    city = models.CharField('Город',max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'shop.Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
