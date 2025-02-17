from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('register/', views.registeruser, name="register"),
    path('', views.home, name="home"),
    path('rooms/<str:pk>', views.rooms, name="rooms"),
    path('delrooms/<int:pk>', views.delcourse, name="delrooms"),
    path('coursehome/', views.coursehome, name="coursehome"),
    path('addcourse/', views.add_course, name="addcourse"),
    path('contacthome/', views.contacthome, name="contacthome"),
    path('addcontact/', views.add_contact, name = "addcontact"),
    path('delcontact/<int:pk>', views.delcontact, name = "delcontact"),
    path('contactus/<str:pk>', views.contactus, name="contacts"),
    path('materials/', views.materials_page, name="materials"),
    path('addmaterials/', views.add_product, name = "addmaterials"),
    path('bookpage/<int:product_id>/', views.bookpage, name="bookpage"),
    path('forums/', views.forums, name="forums"),
    path('profile/<str:pk>', views.userprofile, name="profile"),
    path('forumpage/<str:pk>', views.Forumpage, name="forumpage"),
    path('addtopic/', views.topicadd, name = "addtopic"),
    path('createforum/', views.createforum, name="createforum"),
    path('updateforum/<int:pk>', views.updateforum, name="updateforum"),
    path('delforum/<int:pk>', views.delforum, name="delforum"),
    path('delmessages/<int:pk>', views.delmessages, name="delmessages"),
    path('cart/', views.cart, name="cart"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('back/', views.back_view, name='back'),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('admissions_home/', views.admission_details, name= 'admissions_home'),
    path('store_home/', views.store_home, name='storehome'),
    path('delmaterials/', views.delmaterials, name='delmaterials'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)