from django.urls import path

from .views import BuyView, CancelView, ItemAnOrderView, ItemView, ListItemView, OrderView, PayOrderView, SuccessView

urlpatterns = [
    path('', ListItemView.as_view(), name='main_page'),
    path('buy/<int:id>/', BuyView.as_view(), name='buy'),
    path('item/<int:id>/', ItemView.as_view(), name='item'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('order/<int:id>/', OrderView.as_view(), name='order'),
    path('add_to_order/', ItemAnOrderView.as_view(), name='add_to_order'),
    path('order/<int:id>/pay_order/', PayOrderView.as_view(), name='pay_order'),
]
