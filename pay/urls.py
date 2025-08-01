from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('buy/<int:id>/', views.create_checkout_session, name='buy_item'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('order/<int:id>/buy/', views.create_order_checkout_session, name='buy_order'),
    path('payment-intent/<int:id>/', views.create_payment_intent, name='create_payment_intent'),
    path('item-payment-intent/<int:id>/', views.item_detail_payment_intent, name='item_detail_payment_intent'),
]