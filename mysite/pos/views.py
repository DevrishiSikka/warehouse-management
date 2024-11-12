from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import POSSession, Transaction, Invoice
from products.models import Product
from django.utils import timezone
from django.conf import settings
from twilio.rest import Client


def start_session(request):
    if request.method == "POST":
        ip_address = request.META.get('REMOTE_ADDR')
        session = POSSession.objects.create(employee=None, ip_address=ip_address)
        return redirect('pos:scan_product', session_id=session.id)
    return render(request, 'start_session.html')

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

def generate_invoice(request, session_id):
    session = get_object_or_404(POSSession, id=session_id)
    transactions = Transaction.objects.filter(session=session)
    subtotal = sum(transaction.product.price * transaction.quantity for transaction in transactions)
    gst = subtotal * Decimal('0.10') 
    total = subtotal + gst
    invoice, created = Invoice.objects.get_or_create(session=session, total_amount=total)
    context = {
        'invoice': invoice,
        'transactions': transactions,
        'subtotal': subtotal,
        'gst': gst,
        'total': total,
        'session': session,
        'employee': session.employee,
    }
    return render(request, 'invoice.html', context)


def send_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    transactions = Transaction.objects.filter(session=invoice.session)
    session = invoice.session
    employee = session.employee


    subtotal = sum(transaction.product.price * transaction.quantity for transaction in transactions)
    gst = subtotal * Decimal('0.10')
    total = subtotal + gst

    invoice_content = f"\nInvoice ID: {invoice.id}\n"
    invoice_content += f"Date: {invoice.generated_at.date()}\n"
    invoice_content += f"Time: {invoice.generated_at.time()}\n"
    invoice_content += f"Session ID: {session.id}\n"
    invoice_content += "\nProducts:\n"
    for transaction in transactions:
        invoice_content += f"{transaction.product.name} - {transaction.quantity} @ Rs.{transaction.product.price:.2f} each\n"

    invoice_content += f"\nSubtotal: ${subtotal:.2f}\n"
    invoice_content += f"GST (10%): ${gst:.2f}\n"
    invoice_content += f"Total: ${total:.2f}\n"

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    recipient_number = '+916392667261'  

    try:
        message = client.messages.create(
            body=invoice_content,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        return redirect('pos:start_session')
    except Exception as e:
        return redirect('pos:start_session')

