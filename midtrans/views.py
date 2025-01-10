from decimal import Decimal
from django.shortcuts import render
from .models import Product, Order, CheckoutData
from django.shortcuts import redirect
from .utils import random_order_id
from django.conf import settings
from midtransclient import Snap

def index(request,):

    if request.method == 'POST':
        # Extract data from the POST request
        product_name = request.POST.get('product_name')
        quantity = Decimal(request.POST.get('quantity'))
        price = Decimal(request.POST.get('price'))
        total_price=(price * quantity)
        order_id = random_order_id()
        # Create and save the order
        order = Order(
            order_id=order_id,
            price=price,
            product_name=product_name,
            quantity=quantity,
            total_price=total_price,
        )
        order.save()
        
        # Redirect to the checkout page
        return redirect('checkout', order_id=order_id)
    
    products = Product.objects.all()
    context = {
        'products': products,
    }
    
    return render(request, 'index.html', context)

def checkout(request, order_id):
    order = Order.objects.get(order_id=order_id)
    
    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        phone = request.POST.get('phone')

        # Check if CheckoutData already exists for the order
        try:
            existing_data = CheckoutData.objects.get(order_id=order_id)
            # If data exists, update it instead of creating a new one
            existing_data.name = name
            existing_data.email = email
            existing_data.address = address
            existing_data.city = city
            existing_data.state = state
            existing_data.zip = zip
            existing_data.phone = phone
            existing_data.save()
        except CheckoutData.DoesNotExist:
            # Create and save the checkout data
            data = CheckoutData(
                name=name,
                email=email,
                address=address,
                city=city,
                state=state,
                zip=zip,
                phone=phone,
                order_id=Order.objects.get(order_id=order_id).order_id,
                order_date=Order.objects.get(order_id=order_id).order_date,
            )
            data.save()

        # Initialize Midtrans Snap
        snap = Snap(
            is_production=False,  # Set to True for production
            server_key=settings.MIDTRANS_SERVER_KEY,
            client_key=settings.MIDTRANS_CLIENT_KEY
        )

        # Prepare transaction details
        transaction_details = {
            'order_id': order.order_id,
            'gross_amount': int(order.total_price)
        }

        # Prepare customer details
        customer_details = {
            'first_name': name,
            'email': email,
            'phone': phone,
            'billing_address': {
                'first_name': name,
                'address': address,
                'city': city,
                'postal_code': zip,
            }
        }

        # Create transaction
        transaction = snap.create_transaction({
            'transaction_details': transaction_details,
            'customer_details': customer_details
        })

        # Redirect to Midtrans payment page
        return redirect(transaction['redirect_url'])
    # Fetch the order to display on the checkout page
    return render(request, 'checkout.html', {'order': order})

def payment_success(request, order_id):
    # Fetch the order to display on the payment success page
    order = Order.objects.get(order_id=order_id)
    data = Order(
        order_id = Order.objects.get(order_id=order_id),
        order_date = Order.objects.get(order_id=order_id).order_date,
        total_price = Order.objects.get(order_id=order_id).total_price,
    )
    return render(request, 'payment_success.html', {"order_id":order_id, 'order': order, 'data': data})