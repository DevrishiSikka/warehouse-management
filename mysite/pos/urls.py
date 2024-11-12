from django.urls import path
from .views import start_session, scan_product, generate_invoice, send_invoice

app_name = 'pos'

urlpatterns = [
    path('start/', start_session, name='start_session'),
    path('scan/<int:session_id>/', scan_product, name='scan_product'),
    path('invoice/<int:session_id>/', generate_invoice, name='generate_invoice'),
    path('send-invoice/<int:invoice_id>/', send_invoice, name='send_invoice'),
]