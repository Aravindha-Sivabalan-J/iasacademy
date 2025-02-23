from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import myhome.signals
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.CharField(max_length=255, verbose_name="Address", blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number", blank=True, null=True)
    age = models.IntegerField(verbose_name="Age", blank=True, null=True)
    education = models.CharField(max_length=255, verbose_name="Education", blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User Role")
    course = models.ForeignKey('Courses', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Selected Course")

    def __str__(self):
        return self.user.username
        
class Courses(models.Model):
    #we need course name, duration, fees, no of tests, start date, end date and study material
    subject = models.TextField(max_length=25)
    duration = models.CharField(max_length=20)
    description = models.TextField(max_length=300)
    no_of_tests = models.IntegerField()
    study_material = models.TextField(max_length=300)
    price = models.IntegerField()

    #this is a string representation 
    def __str__(self):
        return self.subject

class Contactus(models.Model):
    #we need to provide our contact details of various branches and mobile number
    branch_name=models.TextField(max_length=100)
    address_line1=models.CharField(max_length=1500,null=True, blank=True)
    address_line2=models.CharField(max_length=1500,null=True, blank=True)
    address_line3=models.CharField(max_length=1500,null=True, blank=True)
    contact_no=models.TextField(max_length=10)
    landline_contact=models.CharField(max_length=12)

    def __str__(self):
        return(f"ID:{self.id}: our branches are located in {self.branch_name}, you can whatsapp us on {self.contact_no} or call us on {self.landline_contact}, feel free to walk into our office at {self.address_line1}")

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Forums(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=100)
    forum_desc=models.CharField(max_length=500)
    participants=models.ManyToManyField(User, related_name='participants', blank='True')
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    forums=models.ForeignKey(Forums, on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]


class Product(models.Model):
    product_type_choices = [
        ('book', 'Book'),
        ('tnbook', 'TNBook'),
        ('tnusrb', 'tnusrb'),
        ('ssb', 'ssb'),
        ('rrb', 'rrb'),
        ('ssc', 'ssc'),
        ('app', 'app'),
    ]
    name = models.CharField(max_length=150)
    price = models.FloatField()
    description = models.TextField(max_length=800)
    product_img = models.ImageField(upload_to='materials/')
    product_type = models.CharField(choices=product_type_choices, max_length=50)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # Return a summary of all items in the cart (for better clarity)
        items = ", ".join([f"{item.product.name} (x{item.quantity})" for item in self.items.all()])
        return f"Cart for {self.user.username}: {items}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Prevent product deletion affecting orders
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return f"{self.product.name} - {self.quantity} items"

class Order(models.Model):
    payment_method_options = [
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI Apps'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Delivery_Address = models.CharField(max_length=255, blank='False', null='False')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Zipcode = models.IntegerField(blank='False', null='False')
    phone_number = models.IntegerField(blank='False', null='False')
    payment_method = models.CharField(choices=payment_method_options, max_length=50, default='COD')
    status = models.CharField(max_length=20, default='Pending')
    items = models.ManyToManyField(CartItem, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Enquiry(models.Model):
    how_do_you_know = [
        ('friends', 'Friends'),
        ('family', 'Family'),
        ('newspaper', 'Newspaper'),
        ('tv ads', 'TV Ads'),
        ('posters', 'Posters'),
        ('others', 'Others'),
    ]
    course_name = [
        ('tnpsc', 'TNPSC'),
        ('upsc', 'UPSC'),
        ('tnusrb', 'TNUSRB'),
        ('ssb', 'SSB'),
        ('rrb', 'RRB'),
        ('app', 'APP'),
    ]
    name = models.CharField(max_length=150)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(21),MaxValueValidator(40)],
        help_text="Age should be between 21 and 40."
    )
    educational_qualification=models.CharField(max_length=255, default='')
    contact_number = models.CharField(max_length=10, help_text ="Enter a Valid Mobile Number")
    address_of_residence = models.CharField(max_length=255)
    pincode = models.CharField(max_length=150, blank='False', null='False')
    interested_course_Course = models.CharField(choices=course_name, max_length=255)
    how_do_you_know_us = models.CharField(choices=how_do_you_know, max_length=255)
    enquired=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='')
    last_follow_up = models.DateTimeField(auto_now=True)
    next_follow_up = models.DateField(default=datetime.date.today)


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class Timetable(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    period_1 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='period_1_timetables')
    period_2 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='period_2_timetables')
    period_3 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='period_3_timetables')
    period_4 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='period_4_timetables')
    period_5 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='period_5_timetables')
    period_6 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='period_6_timetables')
    period_7 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='period_7_timetables')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10, blank=True, null=True)

class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.username} - {self.course.subject}"

class FacultyCourse(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE, related_name='dept_staff')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.username} - {self.course.subject}"


