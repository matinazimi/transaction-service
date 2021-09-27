from django import forms
from django.contrib.auth.models import User

from djongo import models


class Transaction(models.Model):
    _id = models.ObjectIdField()
    merchantId = models.CharField(max_length=30)
    amount = models.CharField(max_length=20)
    createdAt = models.DateField()

    class Meta:
        ordering = ('-createdAt',)


class TransactionData(models.Model):
    createdAt = models.DateField()
    totalAmount = models.CharField(max_length=30)
    Count = models.CharField(max_length=30)

    class Meta:
        abstract = True


class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionData
        fields = [
            'createdAt',
            'totalAmount',
            'Count',
        ]


class TransactionCache(models.Model):
    _id = models.ObjectIdField()
    mode = models.CharField(max_length=30)
    merchantId = models.CharField(max_length=30)
    type = models.CharField(max_length=30, null=True, blank=True)
    data = models.EmbeddedField(
        model_container=TransactionData,
        model_form_class=TransactionForm,
    )
