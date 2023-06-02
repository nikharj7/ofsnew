from http.client import HTTPResponse
from re import M
from unicodedata import category
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, time, timedelta
from django.shortcuts import  redirect, render, HttpResponseRedirect, HttpResponse
from django.views.generic import (CreateView)
                                  
import random
from django.conf import settings
from ..decorators import customer_required, email_verification_required
from ..forms import  customerSignUpForm
from ..models import  User, customer_Detail, Customer_Requirement, Vendor_brands, Vendor_category, Completed_Order, Bid, vendor_Detail, Order, Category, Brands
from bid.models import preorder
from bid import models
import smtplib
import random
from django.db.models import Min
from datetime import timedelta
from django.utils import timezone
import razorpay
from django.views.decorators.csrf import csrf_exempt
# razorpay auth
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



class customerSignUpView(CreateView):
    model = User
    form_class = customerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)
        
        

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect( 'customers:customer_email_verify')


global pin
pin = 0
@login_required
@customer_required
def customer_email_verify(request):
    global pin
    value = User.objects.get(id=request.user.id)
    if request.method =="POST":
        otp = request.POST['OTP']
        if (int(otp)==int(pin)):
            value.email_verified = True
            value.username = value.email
            value.save()
            return redirect('customers:customer_details')
        else:
            value.delete()
            messages.error(request, 'OTP is invalid..!! Please try again..!!')
            return redirect('signup')
    else:
        pin = random.randint(121121, 982379)
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.connect(settings.EMAIL_HOST, 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
        msg = f'from: OrderforSure <info@orderforsure.com>\nTo: {value}\nSubject: Order4Sure OTP Verification\n\n Your Order4Sure Verification OTP is {pin}'
        s.sendmail('OrderforSure <info@orderforsure.com>', f'{value}', msg)
        
    
    return render(request, 'registration/email_verify.html')

@login_required
@customer_required
@email_verification_required
def customer_details(request):
   
    if request.method == "POST":
        Customer_id = User.objects.get(id=request.user.id)
        Orgnization  = request.POST['org']
        Name  = request.POST['fname']
        Phone  = request.POST['phone']
        Address  = request.POST['address']
        Pincode = request.POST['pincode']
        State  = request.POST['state']
        City  = request.POST['city']
        GST  = request.POST['gst']
        License  = request.POST['license']
        Doc  = request.FILES.get('doc', False)
        emails = request.user
        customer_info = customer_Detail(customer_id=Customer_id,Orgnization_Name=Orgnization, Full_Name=Name, Phone=Phone, Address=Address, Pincode=Pincode, State=State, City=City, GST_IN=GST, License_Number=License, Document=Doc )

        customer_info.save()
        
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.connect(settings.EMAIL_HOST, 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
        msg = f'from: OrderforSure <info@orderforsure.com>\nTo: order4sure.in@gmail.com\nSubject: New Customer Registration \n\n Hello Admin, \n\n There is new customer registration on your site. The new registered user is {emails}. Please verify customer details and if its sutaible for our site please approve the user ASAP.'
        s.sendmail('OrderforSure <info@orderforsure.com>', 'order4sure.in@gmail.com', msg)
        return redirect('customers:view_profile')
       
   
    return render(request, 'bid/customers/customers_details.html' )

  


    
@login_required
@customer_required
@email_verification_required

def view_profile(request):
    if customer_Detail.objects.filter(customer_id=request.user):
        data1=customer_Detail.objects.get(customer_id=request.user)
        data=data1
        
        data_dict={
        'data':data
        }
      
        if data.status:
            messages.success(request, 'Profile is verified.')
            return render(request, 'bid/customers/customer_add_form.html', data_dict)
        else:
            messages.error(request, 'Profile is under review.')
            return render(request, 'bid/customers/customer_add_form.html', data_dict)
    else:
        return redirect('customers:customer_profile')


@login_required
@customer_required
@email_verification_required
def customer_requirement(request):
    data = customer_Detail.objects.get(customer_id=request.user)
    categories = Category.objects.all()
    brands = Brands.objects.all()
    email_s = request.user
    userid = request.user.id
    pree = preorder.objects.filter(customer=userid).exclude(complete=True).last()
    
    if request.method == "POST":
        img1 = pree.product_image
        Product_Name = pree.name
        category = pree.category
        Brand = pree.brand
        price = pree.price
        mrp = pree.mrp
        pr = pree.product_ref_no
        Description = pree.description
        Exp_delivery_days = 15
        Quantity = request.POST['qtybutton']
        Delivery_Contact = request.POST['delcon']
        Delivery_Address = request.POST['deladd']
        
        Delivery_Pincode = request.POST['delpin']
        customer= User.objects.get(id=request.user.id)
        
        amount = 200
        
        bid_expire = datetime.combine(date.today(), time(12, 00)) + timedelta(days=3)
        
        
        

        if int(price)*int(Quantity) <= 20000:
            messages.warning(request, 'Sorry We cant accept this requirement. Total amount should be more than 20000rs.')
        else:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

            idd = razorpay_order['id']

            customer_req = Customer_Requirement(mrp=mrp,product_ref_no=pr,amount=razorpay_order['amount'], provider_order_id=razorpay_order['id'],bidding_expiry=bid_expire ,product_image_1=img1,customer=customer,lowest_bid=price,name=Product_Name,category=category,brand=Brand,description=Description,start_price=price,Exp_delivery_days=Exp_delivery_days,quantity=Quantity,delivery_contact=Delivery_Contact,delivery_address=Delivery_Address,delivery_pincode=Delivery_Pincode)
            customer_req.save()
            pree.complete = True
            pree.save()
            pree.delete()
            s = smtplib.SMTP(settings.EMAIL_HOST)
            s.connect(settings.EMAIL_HOST, 587)
            s.starttls()
            s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
            msg = f'from: OrderforSure <info@orderforsure.com>\nTo: order4sure.in@gmail.com\nSubject: New Customer Requirement From {email_s} \n\n Hello Admin, \n\nThere is new customer requirement on your site. The new requirement from {email_s}. Please verify requirement details and if its sutaible for our site please approve the user ASAP.\n\n Here is Requirement Details : \nRazor pay orderID : {idd}\n Product Name : {Product_Name}\n Category : {category}\n Brand : {Brand}\n Start_Price : {price}\n Exp_delivery_days : {Exp_delivery_days}\n Quantity : {Quantity}\n Delivery Contact : {Delivery_Contact}\n Delivery Address : {Delivery_Address}\n Delivery Pincode : {Delivery_Pincode}'
            s.sendmail('OrderforSure <info@orderforsure.com>', 'order4sure.in@gmail.com', msg)



            return render(request,"bid/customers/add_requirement.html",{"razorpay_key": settings.RAZORPAY_KEY_ID,"razorpay_order": razorpay_order, "callback_url": "http://" + "127.0.0.1:8000" + "/customers/callback/"})
           
            
    
    
        
    
  
    context = {'categories':categories, 'brands':brands, 'data':data,'pree':pree}

    return render(request, 'bid/customers/add_requirement.html', context)



@csrf_exempt
def callback(request):
    
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_payment_id' : payment_id,
                'razorpay_order_id' : order_id,
                'razorpay_signature' : signature
            }
            try:
                order_db = Customer_Requirement.objects.get(provider_order_id=order_id)
            except:
                return HttpResponse("505 Not Found")
            order_db.payment_id = payment_id
            order_db.provider_order_id = order_id
            order_db.signature_id = signature
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result == None:
                amount = order_db.amount * 100
                try:
                    razorpay_client.payment_capture(payment_id, amount)
                    order_db.PaymentStatus = "SUCCESS"
                    order_db.save()
                    return render(request, 'bid/customers/paymentsuccess.html')
                except:
                    order_db.PaymentStatus = "FAILURE"
                    order_db.save()
                    return render(request, 'bid/customers/paymentfailure.html')
            else:
                order_db.PaymentStatus = "SUCCESS"
                order_db.save()
                return render(request, 'bid/customers/paymentsuccess.html')    
        except:
                messages.success(request, 'Your Requirement has been submited, Admin is checking for Approval. We will inform you in 24hrs.')
                return redirect('customers:View_requirement')
    else:
        return redirect('/')


   

    

@login_required
@customer_required
@email_verification_required
def View_requirement(request):
    emails = request.user
    data = customer_Detail.objects.get(customer_id=request.user)
    userid = User.objects.get(email=emails)
    data1=Customer_Requirement.objects.filter(customer=request.user).order_by('-product_id').exclude(From_Order4Sure="YES")
    closed = Customer_Requirement.objects.filter(Ordered = "YES")
    data2 = Customer_Requirement.objects.filter(bidding_expiry__lt=datetime.now())
    payid = Customer_Requirement.objects.filter(payment_id='')
    for notpaid in payid:
        notpaid.requirement_status = 'REJECTED'
        notpaid.save()


    for i in data2:
        if i.requirement_status == "ON HOLD":
            pass
        else:
            i.requirement_status = "EXPIRED"
            i.save()
    
    nav=data1
    data_dict={
    'data':data,
    'nav':nav,
    'data2':data2,
    'payid':payid,
    'closed':closed,
    
    }
    if request.method == "POST":
        repost = request.POST['repost']
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.connect(settings.EMAIL_HOST, 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
        msg = f'from: {settings.EMAIL_HOST_USER}\nTo: order4sure.in@gmail.com\nSubject: Repost Requirement of {data2}\n\n Hello admin,\n\n Please Approve requirement from your side this requirement is expired. Requirement information Product Name is {data2}, and my username or email is {userid} and as well as please update expiry date of requirement.   '

      
        s.sendmail(f'{settings.EMAIL_HOST_USER}', 'order4sure.in@gmail.com', msg)
        for i in data2:
            i.requirement_status = "ON HOLD"
            i.save()
    return render(request, 'bid/customers/requirement_list.html', data_dict)

@login_required
@customer_required
@email_verification_required
def requirement_detail(request, pk):
    data = customer_Detail.objects.get(customer_id=request.user)
    data1=Customer_Requirement.objects.get(product_id=pk)
   
    nav=data1

    data_dict={
    'data':data,
    'nav':nav
    }
   
    return render(request, 'bid/customers/requirement_detail.html',data_dict)
    
@login_required
@customer_required
@email_verification_required
def TopBids(request, id):
    data = customer_Detail.objects.get(customer_id=request.user)
    data1 = Customer_Requirement.objects.filter(product_id=id)

    bids=Bid.objects.filter(requirement_id=id).order_by('bid_rate').exclude(bid_rate=100)
   
    prc = bids.aggregate(Min('bid_rate'))
    res = list(prc.values())
    minprice = ("".join(str(v) for v in res))
    
    
   
    
    
   
    data_dict={
    'data':data,
    'data1':data1,
    'bids':bids,
    'minprice':minprice
    
    }

    return render(request, 'bid/customers/bid_detail.html',data_dict)


@login_required
@customer_required
@email_verification_required
def OrderConfirmation(request, pk):
    data = customer_Detail.objects.get(customer_id=request.user)
    bid_details= Bid.objects.get(Bid_id =pk)
    customer_id = bid_details
    vendor_id= bid_details.vendor_id
    user = User.objects.get(email = vendor_id)
    userid = user.id
    customer_id= bid_details.customer_id
   
    req_data= Customer_Requirement.objects.get(product_id= bid_details.requirement_id)
    order_amount= bid_details.bid_rate * req_data.quantity
    seller_detail= vendor_Detail.objects.get(vendor_id= userid)
    seo = seller_detail.Orgnization_Name[3:6]
    sea = seller_detail.Address[3:7]
    sgst = seller_detail.GST_IN[2:5]
    spin = str(seller_detail.Pincode)[2:4]
    
    data_dict={
        'bid_details':bid_details,
        'requirement_detail':req_data,
        'seo':seo,
        'sea':sea,
        'sgst':sgst,
        'spin':spin,
        'order_amount':order_amount,
        'data':data,  
    }
    
    return render(request, 'bid/customers/confirmation_page.html', data_dict)

@login_required
@customer_required
@email_verification_required
def CompleteOrder(request, pk):
  
    
    bid_details= Bid.objects.get(Bid_id=pk)
    vendor_id= bid_details.vendor_id
    customer_id= bid_details.customer_id
    requirement_id =  bid_details.requirement_id
    req_data= Customer_Requirement.objects.get(product_id= requirement_id)
    name = req_data.name

    
    quantity =  req_data.quantity
    pincode = req_data.delivery_pincode
    delivery_contact = req_data.delivery_contact
    bid_id = pk
    yes = "YES"
    expected_delivery = datetime.now()+ timedelta(days=bid_details.expected_delivery +1)
    delivery_address =  req_data.delivery_address
    order_amount= bid_details.bid_rate * req_data.quantity
    
    order_detail= Order( vendor_id=vendor_id, customer_name=customer_id,requirement_id=requirement_id,quantity=quantity,pincode=pincode,
                        delivery_contact=delivery_contact,customer_id=customer_id, 
                        bid_id= bid_id,delivery_address=delivery_address, name=name, order_amount=order_amount, expected_delivery=expected_delivery,order_date=timezone.now().date() )
        
    order_detail.save()
    req_data.Ordered = yes
    req_data.save()
    data_dict={
        'bid_details':bid_details,
        'requirement_detail':req_data,
        
        'order_amount':order_amount   
    }
    return redirect('customers:customerpayment',pk)
    

@login_required
@customer_required
@email_verification_required
def OrdersList(request):

    data = customer_Detail.objects.get(customer_id=request.user)
    orders = Order.objects.filter(customer_id=request.user).order_by('-bid_id')
    data1 = Bid.objects.values_list('requirement_id', flat=True).filter(customer_id=request.user)
    iii = Completed_Order.objects.filter(invoice_uploaded = True)
    nav = Customer_Requirement.objects.filter(product_id__in=data1)
    if request.method == "POST":
        download = request.POST.get('download')
        sss = Completed_Order.objects.get(bid_id=download)
        eee = sss.invoice
        context = {'data':data, 'orders':orders, 'data1':data1,'eee':eee, }
        return render(request, 'bid/customers/orders.html', context)
        

    
    
        
        
 
    
    
    
    
   
    context = {'data':data, 'orders':orders, 'data1':data1, 'iii':iii, }
    return render(request, 'bid/customers/orders.html', context)
    






def profile(request):
    return HttpResponseRedirect("customer_details")

@login_required
@customer_required
@email_verification_required
def Payment(request, id):
    order = Order.objects.get(bid_id=id)
  
    emailss = request.user
    if request.method == "POST":
        pay = request.FILES['pay']
        order.customer_payment_image = pay
        order.customer_payment_status = 'CHECKING FOR TRANSACTION'
        order.customer_payment_proof = True
        order.save()
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.connect(settings.EMAIL_HOST, 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
        msg = f'from: {settings.EMAIL_HOST_USER}\nTo: order4sure.in@gmail.com\nSubject: Payment Recevied From Customer ({emailss})  \n\n Hello admin,\n\n We received a payment from {emailss}. Please verify payment details and update the payment status of Order ID : {order.order_id}.   '

      
        s.sendmail(f'{settings.EMAIL_HOST_USER}', 'order4sure.in@gmail.com', msg)
        return redirect('customers:orders')
    context = {'order':order,}
    return render(request, 'bid/customers/Payment.html', context)

    




def PaymentSuccess(request):
    data = customer_Detail.objects.get(customer_id=request.user)
    return render(request, 'bid/customers/paymentsuccess.html', {'data':data})
    

def PaymentFailure(request):
    data = customer_Detail.objects.get(customer_id=request.user)
    return render(request, 'bid/customers/paymentfailure.html', {'data':data})