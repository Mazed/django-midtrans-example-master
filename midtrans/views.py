from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Product, Order, CheckoutData
from .utils import random_order_id
from django.conf import settings
from midtransclient import CoreApi

def index(request):
    if request.method == 'POST':
        # Extract data from the POST request
        product_name = request.POST.get('product_name')
        quantity = Decimal(request.POST.get('quantity'))
        price = Decimal(request.POST.get('price'))
        total_price = price * quantity
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
        core_api = CoreApi(
            is_production=False,  # Set to True for production
            server_key=settings.MIDTRANS_SERVER_KEY,
            client_key=settings.MIDTRANS_CLIENT_KEY
        )

        # prepare CORE API parameter to get credit card token
        # another sample of card number can refer to https://docs.midtrans.com/en/technical-reference/sandbox-test?id=card-payments
        params = {
            'card_number': '4661601264117463',
            'card_exp_month': '07',
            'card_exp_year': '2029',
            'card_cvv': '809',
            'client_key': settings.MIDTRANS_CLIENT_KEY
        }

        card_token_response = core_api.card_token(params)
        cc_token = card_token_response['token_id']

        param = {
            'payment_type': 'credit_card',
            'credit_card': {
                "token_id": cc_token
            },
            'transaction_details' : {
                "order_id": order.order_id,
                "gross_amount": int(order.total_price),
            },
            'customer_details' : {
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
        }       

        # Create transaction
        charge_response = core_api.charge(param)

        print('charge_response:')
        print(charge_response)

        return redirect('payment_success', order_id=order_id)
    
    # Fetch the order to display on the checkout page
    return render(request, 'checkout.html', {'order': order})

def midtrans_callback(request):
    # Extract status_code and transaction_status from the request
    status_code = request.GET.get('status_code')
    transaction_status = request.GET.get('transaction_status')
    order_id = request.GET.get('order_id')

    # Check if the transaction is successful
    if transaction_status == 'settlement':
        # Redirect to the payment success page with the status code and transaction status
        return redirect('payment_success', order_id=order_id, status_code=status_code, transaction_status=transaction_status)
    else:
        # Handle failed or pending transactions
        return redirect('payment_failed', order_id=order_id, status_code=status_code, transaction_status=transaction_status)

def payment_success(request, order_id):
    # Fetch the order to display on the payment success page
    order = Order.objects.get(order_id=order_id)

    # Pass the status code and transaction status to the template
    status_code = request.GET.get('status_code')
    transaction_status = request.GET.get('transaction_status')

    context = {
        "order_id": order_id,
        'order': order,
        'status_code': status_code,
        'transaction_status': transaction_status,
    }
    
    return render(request, 'payment_success.html', context)
