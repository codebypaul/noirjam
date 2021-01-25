from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json, datetime
from .utils import cartData, guestOrder

# Create your views here.
def cart(request):
    data = cartData(request)

    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)

    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


def store(request):
    data = cartData(request)

    # items = data["items"]
    # order = data["order"]
    # cartItems = data["cartItems"]

    products = Product.objects.all()
    context = {
        "products": {"name": "watch", "digital": False, "price": 179.99},
        # "cartItems": cartItems,
        # "test_data": "test_data",
    }
    print(context)
    return render(request, "store/store.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    print("Action:", action)
    print("Prodcut:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        print(data)
    else:
        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    return JsonResponse("Payment submitted...", safe=False)


def createOrGuest(request):
    data = cartData(request)

    items = data["items"]
    order = data["order"]
    cartItems = data["cartItems"]

    context = {"cartItems": cartItems}
    return render(request, "store/create_or_guest.html", context)


def testRoute(request):
    return render(request, "store/test.html")
