from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class POSSession(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.start_time}"

class Transaction(models.Model):
    session = models.ForeignKey(POSSession, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.product.name} by {self.session.employee.username}"

class Invoice(models.Model):
    session = models.ForeignKey(POSSession, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.session.employee.username} - {self.total_amount}"
