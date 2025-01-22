from django.forms import ModelForm
from .models import Forums, Product, Order

class ForumForm(ModelForm):
    class Meta:
        model = Forums
        fields = '__all__'
        exclude = ['host', 'participants']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['status', 'items', 'user', 'total_amount'] 