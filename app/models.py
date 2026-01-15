from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)  # Product ka naam
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Sirf whole number price
    image = models.ImageField(upload_to="products/", blank=True, null=True)  # Image upload
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)

    SHIPPING_CHOICES = [
        ("free", "Free Shipping"),
        ("flat", "Flat rate: $15.00"),
        ("pickup", "Local Pickup: $8.00"),
    ]
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_CHOICES)

    PAYMENT_CHOICES = [
        ("bank", "Direct Bank Transfer"),
        ("check", "Check Payments"),
        ("cod", "Cash on Delivery"),
        ("paypal", "Paypal"),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.first_name}"


    def update_totals(self):
        self.subtotal = sum(item.total_price for item in self.items.all())

        shipping_cost = 0
        if self.shipping_method == "flat":
            shipping_cost = 15
        elif self.shipping_method == "pickup":
            shipping_cost = 8

        self.total = self.subtotal + shipping_cost
        self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"
    


class Meta:
    verbose_name_plural = "Orders"


    

class orderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    @property
    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    

class Pro(models.Model):
    amount = models.IntegerField()  # ✅ paisa me store hoga (e.g. 50000 = ₹500)
    order_id = models.CharField(max_length=1000)
    razorpay_payment_id = models.CharField(max_length=1000, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.order_id} - {'Paid' if self.paid else 'Unpaid'}"
