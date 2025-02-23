from django.forms import ModelForm
from .models import Forums, Product, Order, Courses, Topic, Contactus, Enquiry, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.dispatch import receiver


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

class AdminForm(UserCreationForm):
    address = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    age = forms.IntegerField(required=True)
    education = forms.CharField(max_length=255, required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="User Role")
    course = forms.ModelChoiceField(queryset=Courses.objects.all(), required=False, label="Select Course")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address', 'phone_number', 'age', 'education', 'group', 'course']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username.lower()

        if commit:
            user.set_password(self.cleaned_data["password1"])
            user.save()  

        # ✅ Assign Group
        group = self.cleaned_data.get('group')
        if group:
            user.groups.add(group)  # ✅ Assign user to group
            user.save()

        # ✅ Create or Update UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.address = self.cleaned_data['address']
        profile.phone_number = self.cleaned_data['phone_number']
        profile.age = self.cleaned_data['age']
        profile.education = self.cleaned_data['education']
        profile.group = group  # ✅ Assign the group

        if group and group.name == "student":
            profile.course = self.cleaned_data.get('course', None)
        else:
            profile.course = None

        profile.save()
        return user







