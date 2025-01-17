from django.contrib import admin

# Register your models here.

from .models import Courses
from .models import Contactus
from .models import Forums
from .models import Message
from .models import Topic
from .models import Product

admin.site.register(Courses)
admin.site.register(Contactus)
admin.site.register(Forums)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(Product)