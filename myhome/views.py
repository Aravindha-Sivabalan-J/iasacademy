from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Courses, Product
from .models import Contactus
from .models import Forums, Enquiry, Timetable, CourseEnrollment
from .models import Topic, Message, Cart, Order, CartItem, OrderItem
from .forms import ForumForm, ProductForm, OrderForm, AddcourseForm, TopicForm, ContactForm, EnquiryForm, EnquiryUpdateForm, ProductDeleteForm, OrderUpdateForm
from decimal import Decimal
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .decorators import allowed_user
from django.utils import timezone

# Create your views here.

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                # Authenticate the user with the provided password
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid Password')  # Password does not match
            else:
                messages.error(request, 'Invalid Username')  # Username does not exist
        else:
            messages.error(request, 'Both Fields are required')
    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')

def registeruser(request):
    form=UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            
            login(request, user)
            return redirect ('forums')
        else:
            messages.error(request, 'something went wrong, try after some time or contact support!')
    return render(request, 'login_register.html', {'form':form})


def home(request):
    if request.user.groups.filter(name="admissions").exists():
        return redirect('admissions_home')
    elif request.user.groups.filter(name="storekeeper").exists():
        return redirect('storehome')
    courses=Courses.objects.all()
    contactus=Contactus.objects.all()
    enquireform= EnquiryForm()
    if request.method == 'POST':
        enquireform = EnquiryForm(request.POST)
        if enquireform.is_valid():
            enquiry = enquireform.save(commit='True')
            enquiry.save()
            return redirect('home')
    context={'contactus':contactus,'courses':courses, 'enquireform':enquireform}
    return render (request, 'home.html', context)

def rooms(request,pk):
    course = Courses.objects.get(id=pk)
    context = {'course':course}
    return render (request, 'rooms.html', context)

def aboutus(request):
    return render (request, 'aboutus.html')

def coursehome(request):
    coursehome=Courses.objects.all()
    context={'coursehome':coursehome}
    return render(request,'coursehome.html', context)

def contacthome(request):
    contacthome=Contactus.objects.all()
    context={'contacthome':contacthome}
    return render(request,'contacthome.html', context)

def contactus(request,pk):
    contactus=Contactus.objects.all()
    contact = Contactus.objects.get(id=pk)
    context={'contact':contact,'contactus':contactus}
    return render (request, 'contactus.html', context)

def materials_page(request):
    # Get all categories of products
    tnusrb_materials = Product.objects.filter(product_type='tnusrb')
    book_materials = Product.objects.filter(product_type='book')
    tnbook_materials = Product.objects.filter(product_type='tnbook')
    ssc_materials = Product.objects.filter(product_type='ssc')
    rrb_materials = Product.objects.filter(product_type='rrb')
    app_materials = Product.objects.filter(product_type='app')

    context = {
        'tnusrb_materials': tnusrb_materials,
        'book_materials': book_materials,
        'tnbook_materials': tnbook_materials,
        'ssc_materials': ssc_materials,
        'rrb_materials': rrb_materials,
        'app_materials': app_materials
    }
    return render(request, 'materials.html', context)

def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_superuser_or_staff, login_url='login')
def topicadd(request):
    addtopicform = TopicForm()
    if request.method == 'POST':
        addtopicform = TopicForm(request.POST)
        if addtopicform.is_valid():
            if addtopicform.cleaned_data.get('delete'):  
                topic_name = addtopicform.cleaned_data.get('name')  
                topic = Topic.objects.filter(name=topic_name).first()
                if topic:
                    topic.delete()
                    return redirect('forums')
                else:
                    addtopicform.add_error('name', 'Topic not found for deletion')
            else:
                topic = addtopicform.save(commit=True)
                return redirect('forums')
    context = {'addtopicform': addtopicform}
    return render(request, 'addtopic.html', context)


def add_product(request):
    bookform = ProductForm()
    if request.method == 'POST':
        bookform = ProductForm(request.POST, request.FILES)
        if bookform.is_valid():
            product = bookform.save(commit='TRUE')
            product.save()
            return redirect ('materials')
    context={'bookform':bookform}
    return render (request,'bookform.html', context)

@user_passes_test(is_superuser_or_staff, login_url='login')
def add_contact(request):
    addcontactform = ContactForm()
    if request.method == 'POST':
        addcontactform = ContactForm(request.POST)
        contactus = addcontactform.save(commit = 'TRUE')
        contactus.save()
        return redirect('contacthome')
    context = {'addcontactform':addcontactform}
    return render (request, 'contactform.html', context)

@user_passes_test(is_superuser_or_staff, login_url='login')
def delcontact(request, pk):
    contaact = Conactus.objects.get(id=pk)
    if request.method == 'POST':
        contaact.delete()
        return redirect ('contacthome')
    context = {'obj': contaact}
    return render (request, 'delete.html',context)


# @user_passes_test(is_superuser_or_staff, login_url='login')
@allowed_user(allowed_roles=['admissions'])
def add_course(request):
    courseform = AddcourseForm()
    if request.method == 'POST':
        courseform = AddcourseForm(request.POST)
        if courseform.is_valid():
            courses = courseform.save(commit='TRUE')
            courses.save()
            return redirect ('coursehome')
    context={'courseform':courseform}
    return render (request, 'courseform.html', context)


def delcourse(request, pk):
    coursee = Courses.objects.get(id=pk)
    if request.method == 'POST':
        coursee.delete()
        return redirect ('home')
    context = {'obj': coursee}
    return render (request, 'delete.html', context)

def bookpage(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    return render(request, 'bookpage.html', {'product': product})

@allowed_user(allowed_roles=['faculty', 'students', 'superadmin'])
def forums(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    topics=Topic.objects.all()
    forums=Forums.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(forum_desc__icontains=q)
    )
    forum_count=forums.count()
    context={'forums':forums, 'topics':topics, 'forum_count':forum_count}
    return render (request, 'forum.html', context)

def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(username='new_user', password='new_password')
        customer = Customer.objects.create(user=user)
        return redirect('home')

@login_required(login_url='login')
@allowed_user(allowed_roles=['faculty', 'students', 'superadmin'])
def Forumpage(request,pk):
    forum=Forums.objects.get(id=pk)
    forum_messages=forum.message_set.all().order_by('-created')
    participants=forum.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            forums=forum,
            body=request.POST.get('body')
        )
        forum.participants.add(request.user)
        return redirect ('forumpage', pk=forum.id)
    context={'forum':forum, 'forum_messages':forum_messages, 'participants':participants}
    return render (request, 'forumpage.html', context)


def userprofile(request, pk):
    users = User.objects.get(id=pk)
    is_student = request.user.groups.filter(name='student').exists()
    enrolled_courses = CourseEnrollment.objects.filter(student=users).values_list('course', flat=True)
    timetable = Timetable.objects.filter(course__in=enrolled_courses).order_by('day')

    context={'users':users, 'is_student':is_student, 'timetable':timetable}
    return render(request, 'userprofile.html', context)


@user_passes_test(is_superuser_or_staff, login_url='login')
def createforum(request):
    form = ForumForm()
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum_to_delete = form.cleaned_data.get('delete_forum')
            if forum_to_delete:
                forum_to_delete.delete()  
                return redirect('forums') 
            else:
                forum = form.save(commit=False)
                forum.host = request.user
                forum.save()
                return redirect('forums')
    context = {'form': form}
    return render(request, 'room_form.html', context)


    return render(request, 'delete_forum.html', context)


@login_required(login_url='login')
def updateforum(request,pk):
    forum=Forums.objects.get(id=pk)
    form= ForumForm(instance=forum)
    if request.user != forum.host:
        return HttpResponse('Action Not Allowed!')
    if request.method=='POST':
        form=ForumForm(request.POST, instance=forum)
        if form.is_valid():
            form.save()
            return redirect('forums')
    context={'form':form}
    return render (request, 'room_form.html', context)

@login_required(login_url='login')
def delforum(request,pk):
    forum=Forums.objects.get(id=pk)
    if request.user != forum.host:
        return HttpResponse('Action Not Allowed!')
    if request.method=='POST':
        forum.delete()
        return redirect('forums')
    return render(request, 'delete.html', {'obj':forum})


@login_required(login_url='login')
def delmessages(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Action Not Allowed!')
    if request.method=='POST':
        message.delete()
        return redirect('forums')
    return render(request, 'delete.html', {'obj':message})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    # Fetch the product
    product = get_object_or_404(Product, id=product_id)

    # Get or create the cart for the user
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=user_cart,
        product=product,
        defaults={'quantity': 1}
    )

    # If the item already exists in the cart, increase its quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('cart')

@login_required(login_url='login')
def view_cart(request):
    user_cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()  
            messages.info(request, f"{cart_item.product.name} was removed from your cart.")
            return redirect('cart')
    cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    user_cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart) 
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def back_view(request): 
    history = request.session.get('history', [])
    print(f"History before back button: {history}")
    if len(history) > 1:
        history.pop()
        request.session['history'] = history
        return HttpResponseRedirect(history[-1])
    return HttpResponseRedirect('/')


def checkout(request):
    # Fetch the cart for the logged-in user
    user_cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)

    # Check if the cart is empty
    if not cart_items.exists():
        messages.info(request, "Your cart is empty. Please add items to the cart before checking out.")
        return redirect('materials')

    # Calculate total price and prepare item details
    total_price = 0
    items_with_totals = []
    for item in cart_items:
        item_total = item.product.price * item.quantity
        total_price += item_total
        items_with_totals.append({
            'product': item.product,
            'quantity': item.quantity,
            'item_total': item_total,
        })

    # Handle the POST request (form submission)
    if request.method == 'POST':
        checkoutform = OrderForm(request.POST)

        if checkoutform.is_valid():
            # Capture shipping information and other details from the form
            order = checkoutform.save(commit=False)
            order.user = request.user
            order.total_amount = total_price
            order.status = 'Pending'  # You can set the order status to "Pending"
            order.save()

            # Create OrderItem instances for each CartItem
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart after placing the order
            cart_items.delete()

            messages.success(request, f"Your order has been placed successfully! Order ID: {order.id}")
            return redirect('materials')  # Redirect to order confirmation page (optional)

    else:
        # Handle the GET request (initial empty form)
        checkoutform = OrderForm()

    # Render the checkout page with form and order details
    return render(request, 'checkout.html', {
        'checkoutform': checkoutform,
        'cart_items': items_with_totals,
        'total_price': total_price,
    })

@allowed_user(allowed_roles=['admissions'])
def admission_details(request):
    details = Enquiry.objects.all()
    admissionform = None 

    age = request.GET.get('age')
    course = request.GET.get('course')
    next_follow_up = request.GET.get('next_follow_up')

    if age:   
        details = details.filter(age=age)

    if course:
        details = details.filter(interested_course_Course=course)

    if next_follow_up:
        details = details.filter(next_follow_up=next_follow_up)

    
    if request.method == "POST" and "enquiry_update" in request.POST:
        enquiry_id = request.POST.get("enquiry_id")
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        admissionform = EnquiryUpdateForm(request.POST, instance=enquiry)
        if admissionform.is_valid():
            enquiry = admissionform.save(commit=False)
            enquiry.last_follow_up = timezone.now()
            enquiry.save()
            return redirect('admissions_home')

    
    courseform = AddcourseForm()
    if request.method == "POST":
        courseform = AddcourseForm(request.POST)
        if courseform.is_valid():
            courses=courseform.save()
            courses.save()
            return redirect('admissions_home') 
    
    coursehome=Courses.objects.all()

    context = {
        'details': details,
        'admissionform': admissionform,
        'courseform': courseform,
        'coursehome':coursehome,
    }
    return render(request, 'details.html', context)

def store_home(request):
    orders = Order.objects.prefetch_related('orderitem_set__product').order_by('-id')
    from django.shortcuts import render, redirect

    orderz = Order.objects.all().order_by('-order_date')

    # Handle form submission
    if request.method == "POST":
        order_id = request.POST.get("order_id")  # Get the order ID from the form
        order = Order.objects.get(id=order_id)  # Get the specific order
        orderform = OrderUpdateForm(request.POST, instance=order)  # Bind form to the instance
        
        if orderform.is_valid():
            order = orderform.save()  # Save the updated status
            return redirect('storehome')  # Redirect to prevent duplicate submissions

    # Create a form for each order, pre-filled with the current status
    order_forms = {order.id: OrderUpdateForm(instance=order) for order in orders}
    context={'orders':orders, 'order_forms': order_forms, 'orderz':orderz}
    return render(request, 'storehome.html', context)

def delmaterials(request):
    if request.method == 'POST':
        form = ProductDeleteForm(request.POST)
        if form.is_valid():
            selected_products = form.cleaned_data['products']
            selected_products.delete()  # Delete selected products
            return redirect('delmaterials')  # Redirect to product list page (change as needed)
    else:
        form = ProductDeleteForm()

    return render(request, 'deleteproduct.html', {'form': form})