from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from unidecode import unidecode
from mptt.models import MPTTModel, TreeForeignKey

def item_upload_location(instance, filename):
    item_name = instance.product.name.lower().replace(" ", "-")  # Use `product` instead of `item`
    file_name = filename.lower().replace(" ", "-")
    return f"item_images/{item_name}/{file_name}"

def validate_file_size(value):
    limit = 104857600  # 100 MB
    if value.size > limit:
        raise ValidationError('Файл слишком большой. Максимальный размер 100 MB.')




class Category(MPTTModel):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    parent = TreeForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        related_name='subcategories', 
        null=True, blank=True, 
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.parent.name + " -> " if self.parent else ""}{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерация slug на основе имени категории
            self.slug = slugify(unidecode(self.name))
            
            # Проверка на уникальность slug
            original_slug = self.slug
            num = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{num}'
                num += 1
        
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(
        
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категория товара',
    )
    name = models.CharField('Название',max_length=200)
    slug = models.SlugField(max_length=200,unique=True, blank=True)
    image = models.ImageField('Главное фото',
        upload_to='products/%Y/%m/%d',
<<<<<<< HEAD

=======
        
>>>>>>> 1e04cd6 (ubuntu)
    )
    video = models.FileField("Видео", upload_to='item_videos/', blank=True, null=True, validators=[validate_file_size])
    description = models.TextField('Описание',blank=True)
    price = models.DecimalField('Цена',max_digits=10, decimal_places=2)
    available = models.BooleanField('Отображать?',default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Если slug пустой, генерируем его из имени категории
        if not self.slug:
            # Используем unidecode для транслитерации имени
            self.slug = slugify(unidecode(self.name))
            
            # Проверяем, чтобы slug был уникальным
            num = 1
            original_slug = self.slug
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{num}'
                num += 1

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Фотография',upload_to=item_upload_location, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def image_thumbnail(self):
        if self.image:
            thumbnail_url = get_thumbnailer(self.image)['admin_thumbnail'].url
            return format_html('<img src="{}" width="150" height="150" />', thumbnail_url)
        return "Нет изображения"

    image_thumbnail.short_description = 'Предпросмотр фотографии'

    def __str__(self):
        return f"Фотография товара: {self.product.name}"
    
    class Meta:
        verbose_name = "Фотографии товара"
        verbose_name_plural = "Фотографии товара"
