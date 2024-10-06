from django.shortcuts import render, redirect
from .models import POSSession, Transaction, Invoice
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def start_session(request):
    if request.method == "POST":
        ip_address = request.META.get('REMOTE_ADDR')
        session = POSSession.objects.create(employee=request.user, ip_address=ip_address)
        return redirect('pos:scan_product', session_id=session.id)
    return render(request, 'start_session.html')

@login_required
def scan_product(request, session_id):
    session = POSSession.objects.get(id=session_id)
    if request.method == "POST":
        barcode = request.POST.get('barcode')
        product = Product.objects.filter(barcode=barcode).first()
        if product:
            quantity = int(request.POST.get('quantity', 1))
            Transaction.objects.create(session=session, product=product, quantity=quantity)
        return redirect('pos:scan_product', session_id=session.id)

    transactions = Transaction.objects.filter(session=session)
    total = sum(transaction.product.price * transaction.quantity for transaction in transactions)
    return render(request, 'scan_product.html', {
        'session': session,
        'transactions': transactions,
        'total': total,
    })


@login_required
def generate_invoice(request, session_id):
    session = POSSession.objects.get(id=session_id)
    transactions = Transaction.objects.filter(session=session)
    total_amount = sum(transaction.product.price * transaction.quantity for transaction in transactions)
    invoice = Invoice.objects.create(session=session, total_amount=total_amount)
    # Here, you could send the invoice to the customer via email
    return render(request, 'invoice.html', {'invoice': invoice, 'transactions': transactions})
