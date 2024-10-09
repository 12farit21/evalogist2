from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Order, OrderItem

# Custom filter for 'paid' field
class PaidFilter(admin.SimpleListFilter):
    title = _('Статус оплаты')  # Custom label for the filter
    parameter_name = 'paid'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Paid')),
            ('no', _('Not Paid')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(paid=True)
        elif self.value() == 'no':
            return queryset.filter(paid=False)
        return queryset

# Custom filter for 'created' field
class CreatedFilter(admin.SimpleListFilter):
    title = _('Дата создания')  # Custom label for the filter
    parameter_name = 'created'

    def lookups(self, request, model_admin):
        # You can add specific lookups if needed, or just rely on the default behavior
        return []

    def queryset(self, request, queryset):
        return queryset

# Custom filter for 'updated' field
class UpdatedFilter(admin.SimpleListFilter):
    title = _('Дата обновления')  # Custom label for the filter
    parameter_name = 'updated'

    def lookups(self, request, model_admin):
        return []

    def queryset(self, request, queryset):
        return queryset


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'full_name',
        'company_name',
        'email',
        'phone',
        'address',
        'postal_code',
        'city',
        'paid',
        'created',
        'updated',
    ]
    
    #list_filter = [PaidFilter, CreatedFilter, UpdatedFilter]  # Using custom filters with custom labels
    inlines = [OrderItemInline]
