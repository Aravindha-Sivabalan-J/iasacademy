from django.contrib import admin
from myhome.views import decrypt_data

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
from .models import Enquiry
from .models import Subject
from .models import Timetable
from .models import CourseEnrollment
from .models import FacultyCourse
from .models import UserProfile

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 
    readonly_fields = ('encrypted_product_name', 'quantity', 'price')
    show_change_link = False  # Remove the edit link for each OrderItem
    can_delete = False  # Remove the delete checkboxes
    max_num = 0
    exclude = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status')
    readonly_fields = ('encrypted_username', 'phone_number', 'Delivery_Address', 'total_amount', 'status', 'get_payment_method')
    exclude = ['user', 'items', 'payment_method']
    inlines = [OrderItemInline]

    def get_payment_method(self, obj):
        return obj.payment_method
    get_payment_method.short_description = "Payment Method"

    # def get_payment_method(self, obj):
    #     try:
    #         return decrypt_data(obj.payment_method) if obj.payment_method else "N/A"
    #     except:
    #         return f"Error: {str(e)}"

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'enquired')
    readonly_fields = ('enquired',)


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
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(Subject)
admin.site.register(Timetable)
admin.site.register(CourseEnrollment)
admin.site.register(FacultyCourse)
admin.site.register(UserProfile)

