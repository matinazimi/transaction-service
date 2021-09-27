from django.contrib import admin

from .models import Transaction, TransactionCache


class TransactionAdmin(admin.ModelAdmin):
    pass


class TransactionCacheAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionCache, TransactionCacheAdmin)
