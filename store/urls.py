from django.urls import path
from . import views

from django.urls import path
from .api import (
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    OrderListCreateAPIView,
    OrderRetrieveUpdateDestroyAPIView,
    OrderItemListCreateAPIView,
    OrderItemRetrieveUpdateDestroyAPIView,
    ShippingAddressListCreateAPIView,
    ShippingAddressRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    


	path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),
    path('order-items/', OrderItemListCreateAPIView.as_view(), name='orderitem-list-create'),
    path('order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyAPIView.as_view(), name='orderitem-detail'),
    path('shipping-addresses/', ShippingAddressListCreateAPIView.as_view(), name='shippingaddress-list-create'),
    path('shipping-addresses/<int:pk>/', ShippingAddressRetrieveUpdateDestroyAPIView.as_view(), name='shippingaddress-detail'),

]





