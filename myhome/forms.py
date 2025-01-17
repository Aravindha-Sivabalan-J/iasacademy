from django.forms import ModelForm
from .models import Forums, Product

class ForumForm(ModelForm):
    class Meta:
        model = Forums
        fields = '__all__'
        exclude = ['host', 'participants']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'