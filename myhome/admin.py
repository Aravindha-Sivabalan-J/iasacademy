from django.contrib import admin

# Register your models here.

from .models import Courses
from .models import Contactus
from .models import Forums
from .models import Message
from .models import Topic
from .models import Product
from .models import Order
from .models import Cart
from .models import CartItem
from .models import OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 
    readonly_fields = ('product', 'quantity', 'price')
    show_change_link = False  # Remove the edit link for each OrderItem
    can_delete = False  # Remove the delete checkboxes
    max_num = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status')
    readonly_fields = ('total_amount', 'items')
    inlines = [OrderItemInline]


admin.site.register(Courses)
admin.site.register(Contactus)
admin.site.register(Forums)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)

