from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Courses(models.Model):
    #we need course name, duration, fees, no of tests, start date, end date and study material
    subject = models.TextField(max_length=100)
    duration = models.CharField(max_length=100)
    description = models.TextField(max_length=2500)
    no_of_tests = models.IntegerField()
    study_material = models.TextField(max_length=1000)
    price = models.IntegerField()

    #this is a string representation 
    def __str__(self):
        return(f"ID:{self.id}: our coaching for {self.subject}, with a duration of {self.duration} has proven to be more effective. {self.description} along with {self.no_of_tests} is the best coaching that you can get today, join now at just ${self.price}")

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
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
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
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # Prevent product deletion affecting orders
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
    Address_line_1 = models.CharField(max_length=255)
    Address_line_2 = models.CharField(max_length=255, blank='True', null='True')
    Address_line_3 = models.CharField(max_length=255, blank='True', null='True')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Zipcode = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    payment_method = models.CharField(choices=payment_method_options, max_length=50, default='COD')
    status = models.CharField(max_length=20, default='Pending')
    items = models.ManyToManyField(CartItem, related_name="orders") 

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)





    



