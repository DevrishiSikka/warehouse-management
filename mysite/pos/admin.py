from django.contrib import admin
from .models import POSSession, Transaction, Invoice

@admin.register(POSSession)
class POSSessionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'ip_address', 'start_time')
    search_fields = ('employee__username', 'ip_address')
    list_filter = ('employee',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('session', 'product', 'quantity', 'timestamp')
    search_fields = ('session__employee__username', 'product__name')
    list_filter = ('session',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('session', 'total_amount', 'generated_at')
    search_fields = ('session__employee__username',)
    list_filter = ('generated_at',)
