from django.urls import path

from .views import TransactionView, CacheView

urlpatterns = [
    path('transaction_list/', TransactionView.as_view()),
    path('transaction_cache/', CacheView.as_view())
]

