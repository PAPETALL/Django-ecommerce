from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import Product, Order, OrderItem, ShippingAddress
from .utils import cartData, guestOrder
from django.db.models import Q
from .models import Product, Customer
from django.contrib.auth import get_user_model



User = get_user_model()
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    # Vérifie si l'utilisateur est authentifié et crée un Customer si nécessaire
    if request.user.is_authenticated:
        try:
            customer = request.user.customer  # Tente d'accéder à un Customer existant pour l'utilisateur
        except Customer.DoesNotExist:
            # Si le Customer n'existe pas, le créer avec l'email de l'utilisateur actuel
            Customer.objects.create(user=request.user, email=request.user.email)
    
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def get(request):
    products = Product.objects.all()
    q = request.GET.get("q")
    if q:
        products = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))

    context = {"products": products}
    return render(request, 'store/store.html', context)


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total():
        order.complete = True
        order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
