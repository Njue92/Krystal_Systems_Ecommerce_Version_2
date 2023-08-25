from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.index, name='home_page'),
    path('base/', views.base, name='base'),
    path('footer/', views.footer, name='footer'),
    path('contact-us/', views.contact, name='contact'),
    path('view_product/', views.product, name='view_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('edit-vendor/', views.edit_vendor, name='edit_vendor'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('side_bar/', views.left_nav, name='left_nav'),
    path('become_vend/', views.become_vend, name='become_vend'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home_page'), name='logout'),
    path('login/', views.login_view, name='login'),
    path('vendor_adm/', views.vendor_adm, name='vendor_adm'),
    path('login_user/', auth_views.LoginView.as_view(template_name='social/login_user.html'), name='login_user'),
    path('add_post/', views.add_post, name='add_post'),
    path('order_tickets/', views.order_tickets, name='order_tickets'),
    path('shop/', views.shop, name='shop'),

]