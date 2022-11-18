from django.db import models

# Create your models here.
class Product(models.Model):
    FASHION     = 'Fashion'
    DEVICES     = 'Devices'
    PHARMECY    = 'Pharmecy'
    BEAUTY      = 'Beauty'
    COMPUTERACC = 'Computer & Accessories'
    MOTORBIKES  = 'Car, Cycle & Motorbike'
    GROCERY     = 'Grocery'
    category_choices = [
        ('', 'Select Category'),
        (FASHION, 'Fashion'),
        (DEVICES, 'Devices'),
        (PHARMECY, 'Pharmecy'),
        (BEAUTY, 'Beauty'),
        (COMPUTERACC, 'Computer & Accessories'),
        (MOTORBIKES, 'Car, Cycle & Motorbike'),
        (GROCERY, 'Grocery'),
    ]
    product_id     = models.AutoField
    product_name   = models.CharField(max_length=255)
    category       = models.CharField(max_length=50, choices=category_choices ,default="")
    sub_category   = models.CharField(max_length=50, default="")
    price          = models.IntegerField(default=0)
    desc           = models.CharField(max_length=300)
    published_date = models.DateTimeField()
    image          = models.ImageField(upload_to="shop/images", default="")


    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name   = models.CharField(max_length=255, null=True)
    email  = models.EmailField(max_length=255, null= True)
    phone  = models.CharField(max_length=255, null=True)
    desc   = models.TextField(max_length=10000, null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    order_id   = models.AutoField(primary_key=True)
    amount     = models.IntegerField(default=0)
    items_json = models.CharField(max_length=5000, null = True)
    name       = models.CharField(max_length=250, null = True)
    email      = models.EmailField(max_length=250, null = True)
    address    = models.TextField(max_length=1000, null = True)
    city       = models.CharField(max_length=250, null = True)
    state      = models.CharField(max_length=250, null = True)
    phone      = models.CharField(max_length=250, null = True)
    zip        = models.CharField(max_length=250, null = True)

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id   = models.AutoField(primary_key=True)
    order_id    = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp   = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7]+ "..."
    
