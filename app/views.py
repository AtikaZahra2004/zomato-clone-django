
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from .models import Contact
from .forms import OrderForm
from .models import Order,Pro
from .models import Product,orderItem

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseBadRequest
from django.db.models.functions import ExtractMonth
# import razorpay



# Create your views here.

def blog(req):
    return render(req,'blog.html')
def about(req):
    return render(req,'about.html')
def profile(req):
    return render(req,'profile.html')
def blog1(req):
    return render(req, "blog1.html")
def blog2(req):
    return render(req, "blog2.html")
def blog3(req):
    return render(req, "blog3.html")
def blog4(req):
    return render(req, "blog4.html")
def blog5(req):
    return render(req, "blog5.html")
def blog6(req):
    return render(req, "blog6.html")
def faq(req):
    return render(req,"faq.html")
def test(req):
    return render(req,"test.html")
def gallery(req):
    return render(req,"gallery.html")
def page(req):
    return render(req,"page.html")
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Database me save karna
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        # Session me bhi dalna ho to
        request.session['contact_data'] = {
            'name': name,
            'email': email,
            'message': message,
        }
        messages.success(request, "Your message has been saved successfully!")
        return redirect("contact")
    contact_data = request.session.get('contact_data', None)
    return render(request, "contact.html", {"contact_data": contact_data})




def order_history(request):
    orders = Order.objects.all().order_by("-id")  # latest order sabse upar
    return render(request, "order_history.html", {"orders": orders})



# product
def shop(request):
    products=Product.objects.all()
    return render (request,'shop.html',{'products':products})

def home(request):
    products=Product.objects.all()
   

    return render (request,'home.html',{'products':products})


def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0

    for product_id, details in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = details.get("quantity", 0)
            subtotal = product.price * quantity
            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            continue

    return render(request, "cart.html", {"items": items, "total": total})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart = request.session.get("cart", {})
    # Current quantity in cart
    current_qty = cart.get(str(pk), {}).get("quantity", 0)
    if current_qty + 1 > product.stock:
        messages.error(request, f"❌ {product.name} is out of stock!")
    else:
        # jo hai msg kro
        cart[str(pk)] = {"quantity": current_qty + 1}
        request.session["cart"] = cart
        messages.success(request, f"✅ {product.name} added to cart!")
    return redirect(request.META.get("HTTP_REFERER", "product_list"))


# update
def update(request,pk,action):
    cart=request.session.get('cart',{})
    if str(pk) in cart:
        if action=="increase":
            cart[str(pk)]['quantity']+=1
        elif action=="decrease":
            cart[str(pk)]['quantity']-=1
            if cart[str(pk)]['quantity']>=0:
                del cart[str(pk)]
    request.session['cart']=cart
    return redirect('cart')               

# remove
def remove(request,pk):
    cart=request.session.get('cart',{})
    if str(pk) in cart:
        del cart[str(pk)]
    request.session['cart']=cart
    return redirect('cart')    

# cart_count
def cart_count(request):
    cart = request.session.get("cart", {})
    total_items = sum(item["quantity"] for item in cart.values())
    return {"cart_count": total_items}


#checkout
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("shop")

    if request.method == "POST":
        order = Order.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            mobile=request.POST["mobile"],
            address=request.POST["address"],
            city=request.POST["city"],
            country=request.POST["country"],
            postcode=request.POST["postcode"],
            shipping_method=request.POST["shipping_method"],
            payment_method=request.POST["payment_method"],
        )

        subtotal = 0
        for product_id, details in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = details["quantity"]
            price = product.price
            subtotal += price * quantity

            orderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )

        order.subtotal = subtotal
        if order.shipping_method == "flat":
            order.total = subtotal + 15
        elif order.shipping_method == "pickup":
            order.total = subtotal + 8
        else:
            order.total = subtotal
        order.save()

        request.session["cart"] = {}  # clear cart
        return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html")


# order_succes
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_success.html", {"order": order})

    





def payment(request):
    if request.method == "POST":
        # paisa * 100 (INR → paisa)
        amount = float(request.POST.get("amount")) * 100

        client = razorpay.Client(auth=("rzp_test_pr99iascS1WRtU", "UTDIzPGwICnAssu3Q3lk7zUi"))

        data = {"amount": amount, "currency": "INR", "receipt": "order_rcptid_11"}
        payment = client.order.create(data=data)

        # Save order in DB
        pro = Pro.objects.create(amount=amount, order_id=payment["id"])
        cart = request.session.get("cart", {})
        items = []
        total = 0

        for product_id, details in cart.items():
            product = Product.objects.get(id=product_id)
            subtotal = details["quantity"] * product.price
            items.append({
                "product": product,
                "quantity": details["quantity"],
                "subtotal": subtotal
            })
            total += subtotal

        return render(request, "cart.html", {"items": items, "total": total,"payment": payment})











# Payment Status
@csrf_exempt
def payment_status(request):
    if request.method == "POST":
        response = request.POST

        params_dict = {
            "razorpay_order_id": response.get("razorpay_order_id"),
            "razorpay_payment_id": response.get("razorpay_payment_id"),
            "razorpay_signature": response.get("razorpay_signature"),
        }

        client = razorpay.Client(auth=("rzp_test_pr99iascS1WRtU", "UTDIzPGwICnAssu3Q3lk7zUi"))

        try:
            # Verify signature
            client.utility.verify_payment_signature(params_dict)

            # Update payment in DB
            pro = Pro.objects.get(order_id=response.get("razorpay_order_id"))
            pro.razorpay_payment_id = response.get("razorpay_payment_id")
            pro.paid = True
            pro.save()

            return render(request, "success.html", {"status": True})

        except Exception as e:
            print("Payment Failed:", e)
            return render(request, "success.html", {"status": False})

    return HttpResponseBadRequest("Invalid request")



def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # stored credentials check
        user = request.session.get('registered_user')
        if user and user['username'] == username and user['password'] == password:
            request.session['username'] = username
            return redirect('home')
        elif username == "admin" and password == "1234":
            request.session['username'] = username
            return redirect('home')
        else:
            return render(request, 'signin.html', {'error': 'Invalid username or password!'})
    return render(request, 'signin.html')

def signout(request):
    request.session.flush()
    return redirect('signin')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # save in session (temporary DB)
        request.session['registered_user'] = {'username': username, 'email': email, 'password': password}
        request.session['username'] = username
        return redirect('home')

    return render(request, 'signup.html')
