from django import forms
from django.contrib import admin
from shop.models import Product, ProductImage, Category
from import_export.admin import ImportExportModelAdmin
import nested_admin
from multiupload.fields import MultiFileField
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin

class ItemImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    exclude = ['order']
    list_display = ['item', 'image_thumbnail']
    readonly_fields = ['image_thumbnail']


class ItemAdminForm(forms.ModelForm):
    additional_images = MultiFileField(
        min_num=1, 
        max_num=5, 
        required=False,
        label="Дополнительные фото"
    )

    class Meta:
        model = Product
        fields = '__all__'

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'cols': 25
            }
        ),
        label="Описание",
        required=False
    )

    def save(self, commit=True):
        # Save the product object first
        product = super().save(commit=commit)
        
        # Now save any additional images
        if commit and self.cleaned_data.get("additional_images"):
            for image in self.cleaned_data["additional_images"]:
                saved_image = ProductImage(product=product, image=image)
                saved_image.save()  # Make sure product is already saved

        return product

class ItemInline(nested_admin.NestedTabularInline):
    model = Product
    form = ItemAdminForm
    extra = 0
    inlines = []

    # Добавляем поиск по Item.name
    search_fields = ['name']  # Теперь можно искать по названию Item
    exclude = ['slug']


class CategoryAdmin(MPTTModelAdmin, nested_admin.NestedModelAdmin, ImportExportModelAdmin):
    inlines = [ItemInline]
    exclude = ['slug','parent']
    search_fields = ['name']
    list_display = ['name']
    list_filter = ['parent']

class SpamForm(forms.ModelForm):
    #additional_images = MultiFileField(label='Дополнительные фото', min_num=1, max_num=5, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def save(self, commit=True):
        # Save the product object first
        product = super().save(commit=commit)
        
        # Now save any additional images
        if commit and self.cleaned_data.get("additional_images"):
            for image in self.cleaned_data["additional_images"]:
                saved_image = ProductImage(product=product, image=image)
                saved_image.save()  # Make sure product is already saved
        
        return product
    

class ImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class EventAdmin(admin.ModelAdmin):
    form = SpamForm
    inlines = [ItemImageInline]

    # Добавляем фильтр по категориям
    list_filter = ['category']

    # Добавляем поиск по названию товара
    search_fields = ['name']  # Это добавляет возможность поиска по полю 'name'
    exclude = ['slug','parent']


admin.site.register(Category, CategoryAdmin)
