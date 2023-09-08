from  django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', views.menu_items),
    path('menu-items/<int:id>/', views.single_menu_item),
    path('cart/', views.cart),
    path('orders/', views.orders),
    path('order-items/', views.order_items),
    path('secret/', views.secret),
    path('api-token-auth/', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('groups/manager/users/', views.managers),
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth/', views.throttle_check_auth),
]