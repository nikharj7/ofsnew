# from email.policy import default
from email.policy import default
from django.utils.text import slugify
from xml.dom.minidom import Document
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.forms import BooleanField
from django.utils.html import escape, mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
import uuid
import datetime
from django.utils import timezone


PAYMENT_CHOICES = (
    ("NOT PAID", "NOT PAID"),
    ("CHECKING FOR TRANSACTION", "CHECKING FOR TRANSACTION"),
    ("TRANSACTION APPROVED", "TRANSACTION APPROVED"),
    
)

PAYMENT_STATUS = (
    ("SUCCESS", "SUCCESS"),
    ("FAILURE", "FAILURE"),
    ("PENDING", "PENDING"),
    
)

ORDER_STATUS = (
    ("YES", "YES"),
    ("NO", "NO"),
    
)

FROM_ORDER4SURE = (
    ("YES", "YES"),
    ("NO", "NO"),
    
)

REQUIREMENT_CHOICES = (
    ("APPROVED","APPROVED"),
    ("PENDING","PENDING"),
    ("REJECTED","REJECTED"),
    ("EXPIRED","EXPIRED"),
    ("DISABLED","DISABLED"),
    ("ON HOLD","ON HOLD"),


)





def phone_validator(value):
    if len(str(value)) != 10:
        raise ValidationError(
            "Enter Valid phone Number")
def pincode_validator(value):
    if len(str(value)) != 6:
        raise ValidationError(
            "Enter Valid pincode")
        
        
class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.EmailField(max_length=75, unique=True)
    username= models.CharField(max_length=75)
    email_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']


class Brands(models.Model):
    name = models.CharField(max_length=30)
    image = models.FileField(upload_to='Brands', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta: 
        
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        html = '<span class="badge badge-primary">%s</span>' % ( name)
        return mark_safe(html)
        

class Category(models.Model):
    image = models.ImageField(upload_to="Brands", null=True, blank=True)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)



    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'



class customer_Detail(models.Model):
    """
    Simply contains User details, referenced by Placement model
    """
    customer_id= models.OneToOneField(User, on_delete=models.CASCADE)
    Orgnization_Name = models.CharField(max_length=255, null=True)
    Full_Name = models.CharField(max_length=255, null=True )
    Phone = models.CharField(max_length=255, null=True)
    Address = models.CharField(max_length=255, null=True)
    Pincode = models.IntegerField(blank=True, null=True)
    State = models.CharField(max_length=30, null=True)
    City = models.CharField(max_length=20, null=True)
    GST_IN = models.CharField(max_length=20, null=True, blank=True)
    License_Number = models.CharField(max_length=20,null=True, blank=True)
    Document = models.FileField(upload_to='Customers_Details/Documents', null=True, blank=True)
    status= models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta: 
        
        verbose_name_plural = "Customer's Details"

    def __str__(self):
        return self.Full_Name


class vendor_Detail(models.Model):
    """
    Simply contains User details, referenced by Placement model
    """
    vendor_id= models.OneToOneField(User, on_delete=models.CASCADE)
    Orgnization_Name = models.CharField(max_length=255, null=True)
    Full_Name = models.CharField(max_length=255, null=True )
    Phone = models.CharField(max_length=255, null=True )
    Address = models.CharField(max_length=255, null=True)
    Pincode = models.IntegerField(blank=True, null=True)
    State = models.CharField(max_length=30, null=True)
    City = models.CharField(max_length=20, null=True)
    GST_IN = models.CharField(max_length=20, null=True)
    License_Number = models.CharField(max_length=20,null=True)
    Document = models.FileField(upload_to='Vendors_Details/Documents', null=True, blank=True, validators=[FileExtensionValidator( ['pdf'] ) ])
    Banking_Name = models.CharField(max_length=255)
    Account_Number = models.CharField(max_length=255)
    IFSC = models.CharField(max_length=255)
    Branch = models.CharField(max_length=255)
    Cheque = models.FileField(upload_to= 'Vendor/Bank_Details')
    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    status= models.BooleanField(default=False)
    class Meta: 
        
        verbose_name_plural = "Vendor's Details"


    def __str__(self):
        return self.Orgnization_Name




class Customer_Requirement(models.Model):
    """
    Simply contains User details, referenced by Placement model
    """

    product_id= models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_image_1 = models.ImageField(upload_to = 'Customer/Product_Requirement_Image', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name = "Product" )
    category = models.CharField(max_length=25)
    brand = models.CharField(max_length=25)
    quantity= models.PositiveIntegerField()
    start_price= models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    lowest_bid= models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    created_at=  models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    Exp_delivery_days=  models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(90)])
    delivery_contact= models.IntegerField(validators=[phone_validator])
    delivery_address =  models.TextField(default=None)
    delivery_pincode = models.IntegerField(validators=[pincode_validator])
    product_ref_no = models.CharField(max_length=255, default='None', null=True, blank=True)
    created_at = models.DateField(auto_now_add =True)
    bidding_expiry= models.DateTimeField(null=True, blank=True)
    requirement_status = models.CharField(max_length=255, choices=REQUIREMENT_CHOICES, default="PENDING" )
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    signature_id = models.CharField(_("Signature ID"), max_length=128, null=False, blank=False)
    PaymentStatus = models.CharField(max_length=255, choices=PAYMENT_STATUS, default="PENDING" )
    Ordered = models.CharField(max_length=25, choices=ORDER_STATUS, default="NO")
    From_Order4Sure = models.CharField(max_length=25, choices=FROM_ORDER4SURE, default="NO")
    complete = models.BooleanField(default=False)
    
    class Meta: 
        
        verbose_name_plural = "Customer's Requirements"
    
    




    def __str__(self):
        return self.name
    
class Vendor_brands(models.Model):
    brand_interest = models.CharField(max_length=26)
    vendor_id= models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    class Meta: 
        
        verbose_name_plural = "Vendor Brands"

    

    
class Vendor_category(models.Model):
    category_interest = models.CharField(max_length=26)
    vendor_id= models.CharField(max_length=26)
    is_active = models.BooleanField(default=True)
    class Meta: 
        
        verbose_name_plural = "Vendor Categories"

class Bid(models.Model):
    product_image = models.ImageField(upload_to='Vendor/Product_Image',null=True, blank=True )
    Bid_id = models.AutoField(primary_key=True)
    customer_id= models.CharField(max_length=25)
    vendor_id = models.CharField(max_length=25)
    requirement_id =  models.IntegerField()
    name = models.CharField(max_length=255, verbose_name = "Product")
    bid_rate = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)	
    quantity =  models.IntegerField()
    expected_delivery = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(90)])
    product_expiry = 	 models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    supply_pincode= models.IntegerField()
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    signature_id = models.CharField(_("Signature ID"), max_length=128, null=False, blank=False)
    PaymentStatus = models.CharField(max_length=255, choices=PAYMENT_STATUS, default="PENDING" )
    From_Order4Sure = models.CharField(max_length=25, choices=FROM_ORDER4SURE, default="NO") 
    complete = models.BooleanField(default=False)



   

    
    
    
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField()
    customer_id= models.CharField(max_length=50)
    vendor_id = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=50)
    requirement_id =  models.IntegerField(unique=True)
    bid_id =  models.IntegerField()
    name=  models.CharField(max_length=255,verbose_name = "Product" )
    quantity =  models.IntegerField()
    pincode = models.IntegerField()
    order_amount = models.IntegerField()
    expected_delivery =  models.DateField()
    delivery_contact= models.IntegerField()
    delivery_address =  models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=255, default='Active')
    customer_payment_status = models.CharField(max_length=255, choices=PAYMENT_CHOICES, default="NOT PAID" )
    customer_payment_image = models.FileField(upload_to= 'Customer/Order_Payment', null=True, blank=True)
    customer_payment_proof = models.BooleanField(default=False)
    customer_payment_approved = models.BooleanField(default=False)
    From_Order4Sure = models.CharField(max_length=25, choices=FROM_ORDER4SURE, default="NO") 
    completed = models.BooleanField(default=False)


class Completed_Order(models.Model):
    invoice = models.FileField(upload_to='Complete_Order/Invoice', null=True, blank=True)
    customer_id= models.CharField(max_length=50)
    vendor_id = models.CharField(max_length=50)
    requirement_id =  models.IntegerField()
    bid_id =  models.IntegerField()
    name=  models.CharField(max_length=255, verbose_name = "Product")
    quantity =  models.IntegerField()
    pincode = models.IntegerField()
    order_amount = models.IntegerField()
    expected_delivery =  models.DateField()
    delivery_contact= models.IntegerField()
    delivery_address =  models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=255, default='Complete')
    customer_payment_status = models.CharField(max_length=255, default='Complete')
    vendor_payment_status = models.CharField(max_length=255, default='Complete')
    customer_payment_image = models.FileField(upload_to= 'Customer/Complete_Order_Payment', null=True, blank=True)
    invoice_uploaded = models.BooleanField(default=False)
    class Meta: 
        
        verbose_name_plural = "Complete Orders"

 


class Contact_Us(models.Model):
    Email = models.CharField(max_length=255 )
    Name = models.CharField(max_length=255 )
    Subject = models.CharField(max_length=255 )
    Message = models.TextField()
    class Meta: 
        
        verbose_name_plural = "Contact Us"


class Product(models.Model):
    Vendor = models.CharField(max_length=50)
    image1 = models.ImageField(upload_to='Nirbhik_Products', null=True, blank=True)
    image2 = models.ImageField(upload_to='Nirbhik_Products', null=True, blank=True)
    image3 = models.ImageField(upload_to='Nirbhik_Products', null=True, blank=True)
    image4 = models.ImageField(upload_to='Nirbhik_Products', null=True, blank=True)
    image5 = models.ImageField(upload_to='Nirbhik_Products', null=True, blank=True)
    name = models.CharField(max_length=500,verbose_name = "Product", null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    mrp = models.IntegerField(null=True, blank=True)
    GST = models.IntegerField(null=True, blank=True)
    quantity = models.CharField(max_length=8, null=True, blank=True, default=1)
    step_up_quantity = models.CharField(max_length=8,null=True, blank=True, default=1)
    category = models.CharField( max_length=500,null=True, blank=True)
    Brand = models.CharField( max_length=50,null=True, blank=True)
    Length = models.CharField( max_length=50,verbose_name = "Length(cm)",null=True, blank=True)
    Width = models.CharField( max_length=50,verbose_name = "Width(cm)",null=True, blank=True)
    Height = models.CharField( max_length=50,verbose_name = "Height(cm)",null=True, blank=True)
    Weight  = models.CharField( max_length=50,verbose_name = "Weight(kg)",null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    SKU = models.CharField(max_length=255, null=True, blank=True)
    slug = models.TextField(null=True, blank=True)
    in_stock = models.CharField(max_length=50, choices=FROM_ORDER4SURE, default="YES")
    created = models.DateTimeField(editable=False, default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    @staticmethod
    def get_product_by_ids(ids):
        return Product.objects.filter(id__in = ids)

   



    


class preorder(models.Model):
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_image= models.ImageField(upload_to = 'Customer/Product_Requirement_Image', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name = "Product" )
    category = models.CharField(max_length=25)
    brand = models.CharField(max_length=25)
    price = models.CharField(max_length=25)
    mrp = models.CharField(max_length=25)
    quantity= models.PositiveIntegerField()
    step_up_quantity = models.CharField(max_length=8)
    product_ref_no = models.CharField(max_length=255, default='None', null=True, blank=True)
    description = models.TextField()
    slug = models.CharField(max_length=255, unique=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add =True)
    
    def __str__(self):
        return self.name


class Order_From_Order4Sure(models.Model):
    order_id = models.AutoField(primary_key=True)
    invoice = models.FileField(upload_to='Complete_Order/Store_Invoice', null=True, blank=True)
    order_date = models.DateField()
    product_image = models.ImageField(upload_to = 'Order/Add_to_Cart', null=True, blank=True)
    customer_id= models.CharField(max_length=50)
    vendor_id = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=50)
    name=  models.CharField(max_length=255,verbose_name = "Product" )
    quantity =  models.IntegerField()
    pincode = models.IntegerField()
    order_amount = models.IntegerField()
    GST = models.CharField(max_length=50, blank=True, null=True)
    Drug = models.CharField(max_length=50, blank=True, null=True)
    expected_delivery =  models.DateField()
    delivery_contact= models.IntegerField()
    delivery_address =  models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=255, default='Active')
    customer_payment_status = models.CharField(max_length=255, choices=PAYMENT_CHOICES, default="NOT PAID" )
    customer_payment_image = models.FileField(upload_to= 'Customer/Order_Payment', null=True, blank=True)
    customer_payment_proof = models.BooleanField(default=False)
    customer_payment_approved = models.BooleanField(default=False)
    From_Order4Sure = models.CharField(max_length=25, choices=FROM_ORDER4SURE, default="YES") 
    completed = models.BooleanField(default=False)

    class Meta: 
        
        verbose_name_plural = "From_Order4Sure"

    def __str__(self):
        return self.delivery_address + ' ' + self.customer_id
    

class Banner(models.Model):
    Image1 = models.ImageField(upload_to = 'Home/Banner', null=True, blank=True)
    Image2 = models.ImageField(upload_to = 'Home/Banner', null=True, blank=True)
    Image3 = models.ImageField(upload_to = 'Home/Banner', null=True, blank=True)
    Image4 = models.ImageField(upload_to = 'Home/Banner', null=True, blank=True)
   




class vendor_products_file(models.Model):
    vendor_id = models.CharField(max_length=50)
    productfile = models.FileField(upload_to='Vendor_products', null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.vendor_id


