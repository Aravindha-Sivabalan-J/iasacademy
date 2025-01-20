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
from .models import Forums
from .models import Topic, Message, Cart, Order
from .forms import ForumForm, ProductForm, OrderForm
from decimal import Decimal
from django.http import Http404, HttpResponseRedirect

# Create your views here.

def loginpage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        # try:
        #     user=user.object.get(username=username)
        # except:
        #     messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User does not Exist')


    context={'page':page}
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
    courses=Courses.objects.all()
    contactus=Contactus.objects.all()
    context={'contactus':contactus,'courses':courses}
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


def bookpage(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    
    return render(request, 'bookpage.html', {'product': product})

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
        # handle user registration here
        user = User.objects.create_user(username='new_user', password='new_password')
        
        # Now, create a corresponding Customer object
        customer = Customer.objects.create(user=user)

        return redirect('home')

@login_required(login_url='login')
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


def userprofile(request):
    context={}
    return render (request, 'profile.html, context')


@user_passes_test(is_superuser_or_staff, login_url='login')
def createforum(request):
    form=ForumForm()
    if request.method=='POST':
        form=ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit='FALSE')
            forum.host=request.user
            forum.save()
            return redirect('forums')

    context={'form':form}
    return render (request,'room_form.html', context)

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
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('cart')

@login_required(login_url='login')
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def update_cart(request, cart_item_id, action):
    cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif action == 'decrease' and cart_item.quantity == 1:
        cart_item.delete()
        messages.info(request, f"{cart_item.product.name} was removed from your cart.")
        return redirect('cart')  

    cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    
    cart_items = Cart.objects.filter(user=request.user)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

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
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.info(request, "Your cart is empty. Please add items to the cart before checking out.")
        return redirect('materials')
    total_price = 0
    items_with_totals = []
    for item in cart_items:
        item_total = item.product.price * item.quantity
        total_price += item_total
        items_with_totals.append({
            'product': item.product,
            'quantity': item.quantity,
            'item_total': item_total
        })
    if request.method == 'POST':# Capture shipping information and other details from the form
        shipping_address = request.POST.get('shipping_address')
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')

        if not shipping_address or not phone_number or not payment_method:
            messages.error(request, "Please fill in all the details.")
            return redirect('checkout')
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            phone_number=phone_number,
            total_price=total_price,
            payment_method=payment_method,
            status='Pending'
        )
        for cart_item in cart_items:
            order.items.add(cart_item)
        cart_items.delete()
        messages.success(request, f"Your order has been placed successfully! Order ID: {order.id}")
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'checkout.html', {
        'cart_items': items_with_totals,
        'total_price': total_price
    })


@login_required(login_url='login')
def place_an_order(request):
    checkoutform = OrderForm()
    
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return render(request, 'error_page.html', {'message': 'Your cart is empty.'})

    if request.method == 'POST':
        checkoutform = OrderForm(request.POST)
        if checkoutform.is_valid():
            order = checkoutform.save(commit=False)
            
            order.user = request.user
            
            order.save()
            
            order.items.set(cart_items)  
            
            cart_items.delete()

            return redirect('materials') 

    context = {'checkoutform': checkoutform}
    return render(request, 'place_order.html', context)

