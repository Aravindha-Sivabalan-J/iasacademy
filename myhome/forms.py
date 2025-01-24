from django.forms import ModelForm
from .models import Forums, Product, Order, Courses, Topic, Contactus
from django import forms

class ContactForm(ModelForm):
    class Meta:
        model = Contactus
        fields = '__all__'

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

class AddcourseForm(ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'

class TopicForm(ModelForm):
    delete = forms.BooleanField(required=False, label="Delete this topic")

    class Meta:
        model = Topic
        fields = '__all__'