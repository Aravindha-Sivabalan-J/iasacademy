from django.forms import ModelForm
from .models import Forums, Product, Order, Courses, Topic, Contactus, Enquiry
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

class ProductDeleteForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
  
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

class EnquiryForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = '__all__'
        exclude = ['enquired', 'status', 'next_follow_up', 'last_follow_up']


class EnquiryUpdateForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['status', 'next_follow_up']  # Only allow updating these fields
        widgets = {
            'status': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'placeholder': 'Enter feedback here...'}),
            'next_follow_up': forms.DateInput(attrs={'type': 'date'}),  # Calendar picker
        }

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
