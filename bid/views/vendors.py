from dataclasses import field
from re import T
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect, render, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.db.models import Min
from django.db.models import F, Window
from django.db.models.functions import Rank

from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from ..decorators import vendor_required, customer_required,email_verification_required
from ..forms import  vendorSignUpForm
from ..models import  PAYMENT_STATUS, Brands, Order_From_Order4Sure, vendor_products_file, Category,Completed_Order, Customer_Requirement, User, vendor_Detail, Vendor_brands, Vendor_category, Bid, Order
import random
from django.conf import settings
import smtplib
import razorpay
from django.views.decorators.csrf import csrf_exempt
from datetime import  datetime, timedelta
from django.db.models import F, Window
from django.db.models.functions import Rank

# razorpay auth
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class vendorSignUpView(CreateView):
    model = User
    form_class = vendorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'vendor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        
        return redirect('vendors:vendor_email_verify')



def profile(request):
    return HttpResponseRedirect("vendor_details")

@login_required
@vendor_required
@email_verification_required
def vendor_details(request):
    
    user = request.user
    if request.method == "POST":
        Vendor_id = User.objects.get(id=request.user.id)
        Orgnization  = request.POST['org']
        Name  = request.POST['fname']
        Address  = request.POST['address']
        Pincode = request.POST['pincode']
        State  = request.POST['state']
        City  = request.POST['city']
        GST  = request.POST['gst']
        License  = request.POST['license']
        Document  = request.FILES['doc']
        Phone = request.POST['phone']
        Banking = request.POST['Banking']
        Account = request.POST['Account']
        IFSC = request.POST['IFSC']
        Cheque = request.FILES['Cheque']
        Branch = request.POST['Branch']

        vendor_info = vendor_Detail(Branch=Branch,vendor_id=Vendor_id, Banking_Name=Banking, Account_Number =Account, IFSC = IFSC, Cheque=Cheque,  Orgnization_Name=Orgnization, Full_Name=Name,  Address=Address, Pincode=Pincode, State=State, City=City, GST_IN=GST, License_Number=License, Document=Document, Phone=Phone )

        vendor_info.save()
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.connect(settings.EMAIL_HOST, 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
        msg = f'from: OrderforSure <info@orderforsure.com>\nTo: order4sure.in@gmail.com\nSubject: New Vendor Registration \n\n Hello Admin, \n\n There is new vendor registration on your site. The new registered user is {user}. Please verify vendor details and if its sutaible for our site please approve the user ASAP.'
        s.sendmail('OrderforSure <info@orderforsure.com>', 'order4sure.in@gmail.com', msg)
        return redirect('vendors:view_profile')
    
    return render(request, 'bid/vendors/vendors_details.html')


    
@login_required
@vendor_required
@email_verification_required
def view_profile(request):
    if vendor_Detail.objects.filter(vendor_id=request.user):
        data1=vendor_Detail.objects.get(vendor_id=request.user)
        data=data1
        
        data_dict={
        'data':data
        }
       
        if data.status:
            messages.success(request, 'Profile is verified.')
            return render(request, 'bid/vendors/vendor_add_form.html', data_dict)
        else:
            messages.error(request, 'Profile is under review.')
            return render(request, 'bid/vendors/vendor_add_form.html', data_dict)
    else:
        return redirect('vendors:vendor_profile')


@method_decorator([login_required, vendor_required], name='dispatch')
class vendorInterests(ListView):
    model = vendor_Detail
    fields=['city']
    context_object_name = 'data'
    template_name = 'bid/vendors/interest.html'
    

    def get_queryset(self):
        
        vendor= self.request.user
        vendor_brands = Vendor_brands.objects.values_list('brand_interest', flat=True).filter(vendor_id=vendor)
        
        vendor_category = Vendor_category.objects.values_list('category_interest', flat=True).filter(vendor_id=vendor)
        brands = Brands.objects.filter(name__in=vendor_brands)
        category= Category.objects.filter(name__in=vendor_category)
        all_brands= Brands.objects.all()
        all_category= Category.objects.all()
        
           

        
    
        
        data={'brands':brands, 'vendor':vendor, "category":category, 'all_brands':all_brands, 'all_category':all_category}
    
        return data
   
        

@login_required
@vendor_required
@email_verification_required
def submit_interests(request):
    if request.method == "POST":
            interested_brand = request.POST.getlist('brand_interests')
           

            

           
            interested_category = request.POST.getlist('category_interests')
           
           
        
            Vendor_category.objects.filter(vendor_id= request.user.id).delete()
            Vendor_brands.objects.filter(vendor_id= request.user.id).delete()
            vendor_ID= request.user
           
           
            for brands in interested_brand:
              
                data= Brands.objects.get(name=brands)     
             
                Vendor_brands.objects.create(brand_interest= data,vendor_id= vendor_ID) 
            for category in interested_category:
                data= Category.objects.get(name=category)
               
             
                Vendor_category.objects.create(category_interest= data, vendor_id = vendor_ID)
       
      
    return redirect('vendors:vendorInterestsView' )




        
@login_required
@vendor_required
@email_verification_required
def BidListView(request):
    data=vendor_Detail.objects.get(vendor_id=request.user)
    vendor=request.user
    

    vendor_brands = Vendor_brands.objects.values_list('brand_interest').filter(vendor_id=vendor)
    vendor_category = Vendor_category.objects.values_list('category_interest').filter(vendor_id=vendor)
    hello = ''
    for i in vendor_brands:
        hello = ''.join(map(str, i))
    nav = Customer_Requirement.objects.filter(brand__icontains = hello).exclude(requirement_status="REJECTED").order_by("-product_id")
    hello1 = ''
    for j in vendor_category:
        hello1 = ''.join(map(str, j))
    pid = Customer_Requirement.objects.filter(product_id__in= vendor_brands).exclude(requirement_status="REJECTED")
    idd = Customer_Requirement.objects.all()
    for i in nav:
        i.product_id
    data1=Customer_Requirement.objects.get(product_id=i.product_id)
    data2 = Customer_Requirement.objects.filter(category__icontains = hello1).exclude(requirement_status="REJECTED")
    for i in data2:
        i.product_id
    data1=Customer_Requirement.objects.get(product_id=i.product_id)
    print(data1)
    
    closed = Customer_Requirement.objects.filter(Ordered = "YES")
    
    data3 = Customer_Requirement.objects.filter(bidding_expiry__lt=datetime.now())
    for y in data3:
        if y.requirement_status == "ON HOLD":
            pass
        else:
            y.requirement_status = "EXPIRED"
            y.save()
    
    if request.method == "POST":
        biddd = Bid.objects.filter(vendor_id=request.user, requirement_id=data1.product_id)
        check_exist = biddd.exists()
        if check_exist:
            time_hai = data1.bidding_expiry - timedelta(minutes=5)
            if time_hai.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
                data1.bidding_expiry  = datetime.now() + timedelta(minutes=5)
                data1.save()
                return redirect('vendors:requirement_detail',data1.product_id )
            else:
                return redirect('vendors:requirement_detail',data1.product_id )

        else:
            time_hai = data1.bidding_expiry - timedelta(minutes=5)
            if time_hai.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
                data1.bidding_expiry  = datetime.now() + timedelta(minutes=5)
                data1.save()
                mrp = data1.mrp
                exp_days = data1.Exp_delivery_days
                quantity = data1.quantity
                vendor_id = vendor
                customer_id = data1.customer
                supplier_pin = data.Pincode
                p_id  = data1.product_id
                ccc = True


                amount = 200
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                razorpay_order = client.order.create({"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})

                                
                bid = Bid(amount=razorpay_order['amount'], provider_order_id=razorpay_order['id'],customer_id=customer_id, product_image=i.product_image_1, bid_rate=100, product_expiry=datetime.now(), quantity=quantity, vendor_id=vendor_id,requirement_id = p_id,mrp=mrp,expected_delivery=exp_days,supply_pincode=supplier_pin,complete=True, name=i.name)
                bid.save()
                        
                data1.complete = ccc
                data1.save()
                s = smtplib.SMTP(settings.EMAIL_HOST)
                s.connect(settings.EMAIL_HOST, 587)
                s.starttls()
                s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
                            
                msg = f'from: OrderforSure <info@orderforsure.com>\nTo: order4sure.in@gmail.com\nSubject: New Vendor Bid Form {vendor} \n\n Hello Admin, \n\n There is new vendor bid on your site against {customer_id}. The new bid form {vendor}. Please verify bid details and if its sutaible for our site please approve the user ASAP. Bid details as follow : \n\n Product ID : {data1.product_id}  Product Name : {data1}\n\n You can search in Database for more details with Product ID.'
                s.sendmail('OrderforSure <info@orderforsure.com>', 'order4sure.in@gmail.com', msg)
                return render(request,"bid/vendors/bid_list.html",{"razorpay_key": settings.RAZORPAY_KEY_ID,"razorpay_order": razorpay_order, "callback_url": "http://" + "127.0.0.1:8000" + "/vendors/callback/"})
            else:
                mrp = data1.mrp
                exp_days = data1.Exp_delivery_days
                quantity = data1.quantity
                vendor_id = vendor
                customer_id = data1.customer
                supplier_pin = data.Pincode
                p_id  = data1.product_id
                ccc = True


                amount = 200
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                razorpay_order = client.order.create({"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})

                                
                bid = Bid(amount=razorpay_order['amount'], provider_order_id=razorpay_order['id'],customer_id=customer_id, product_image=i.product_image_1, bid_rate=100, product_expiry=datetime.now(), quantity=quantity, vendor_id=vendor_id,requirement_id = p_id,mrp=mrp,expected_delivery=exp_days,supply_pincode=supplier_pin,complete=True, name=i.name)
                bid.save()
                        
                data1.complete = ccc
                data1.save()
                s = smtplib.SMTP(settings.EMAIL_HOST)
                s.connect(settings.EMAIL_HOST, 587)
                s.starttls()
                s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
                            
                msg = f'from: OrderforSure <info@orderforsure.com>\nTo: order4sure.in@gmail.com\nSubject: New Vendor Bid Form {vendor} \n\n Hello Admin, \n\n There is new vendor bid on your site against {customer_id}. The new bid form {vendor}. Please verify bid details and if its sutaible for our site please approve the user ASAP. Bid details as follow : \n\n Product ID : {data1.product_id}  Product Name : {data1}\n\n You can search in Database for more details with Product ID.'
                s.sendmail('OrderforSure <info@orderforsure.com>', 'order4sure.in@gmail.com', msg)
                return render(request,"bid/vendors/bid_list.html",{"razorpay_key": settings.RAZORPAY_KEY_ID,"razorpay_order": razorpay_order, "callback_url": "http://" + "127.0.0.1:8000" + "/vendors/callback/"})


    context = {'data':data, 'data2':data2, 'pid':pid, 'nav':nav,  'closed':closed,}
    return render(request, 'bid/vendors/bid_list.html', context)

            
            



    
    
    
@login_required
@vendor_required
@email_verification_required 
def requirement_detail(request, pk):
    data=vendor_Detail.objects.get(vendor_id=request.user)
    vendor = request.user
    data1=Customer_Requirement.objects.get(product_id=pk)
    nav=data1
   
    biddd=Bid.objects.filter(requirement_id=pk)

    


    ddd = Bid.objects.filter(vendor_id=request.user, requirement_id=data1.product_id).last()
    

       
 
        
    
    

    
    
    
    
    
    
  
    cusid = data1.customer
    
    user = request.user
    
    data_dict={
    'data':data,
    'nav':nav,
    'biddd':biddd,
    'ddd':ddd,
    # 'ranking':ranking,
    
    


    }
    if request.method == "POST":
        
        venrate = request.POST['number']
       
        
        ccc = True
        if int(venrate) > int(nav.start_price):
            messages.warning(request, 'You cant Bid more than start price.')
            data1.lowest_bid = data1.start_price
            data1.save()

        else:
            
            data1.lowest_bid = venrate
            data1.save()
            data1.complete = ccc
            data1.save()
            ddd.bid_rate = venrate
            ddd.save()
                
                

        
    return render(request, 'bid/vendors/requirement_detail.html',data_dict)



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
                order_db = Bid.objects.get(provider_order_id=order_id)
                hello = order_db.requirement_id
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
                    return render(request, 'bid/vendors/paymentsuccess.html')
                except:
                    order_db.PaymentStatus = "FAILURE"
                    order_db.save()
                    return render(request, 'bid/vendors/paymentfailure.html')
            else:
                order_db.PaymentStatus = "SUCCESS"
                order_db.save()
                return render(request, 'bid/vendors/paymentsuccess.html')
            
        except:
            return redirect('vendors:requirement_detail',hello )
    else:
        return redirect('/')


@login_required
@vendor_required
@email_verification_required 
def MyBidsList(request):
    
    data=vendor_Detail.objects.get(vendor_id=request.user)
    data1=Bid.objects.values_list('requirement_id', flat=True).filter(vendor_id=request.user)
    bidid = Bid.objects.values_list('Bid_id', flat=True).filter(vendor_id=request.user)
  
    nav = Customer_Requirement.objects.filter(product_id__in=data1).order_by('-product_id').exclude(From_Order4Sure="YES")
    data2 = Bid.objects.filter(Bid_id__in=bidid)
    
    data_dict={
    'data':data,
    'data2':data2,
    'nav':nav

    }
   
    return render(request, 'bid/vendors/mybid_list.html',data_dict)




    
@login_required
@vendor_required
@email_verification_required    
def VendorBid(request):
    nav=vendor_Detail.objects.get(vendor_id=request.user)
    id = request.POST.get('id')
   
    data= Customer_Requirement.objects.get(product_id=id)
    data_dict={
    'data':data,
    'nav':nav
    }
    
    return render(request, 'bid/vendors/bid_detail.html',data_dict)

@login_required
@vendor_required
@email_verification_required        
def SubmitBid(request): 
         
    if request.method=='POST':
        requirement_ID= request.POST.get('data_id')
        data= Customer_Requirement.objects.get(product_id=requirement_ID)
        customer_id= data.customer_id
        curr_low_bid= data.lowest_bid
        vendor_id = request.user.id
        bid_rate = float(request.POST.get('bid_price'))
        pincode = request.POST.get('dispatch_pincode')
        mrp = request.POST.get('mrp')
        estimated_delivery = 	 request.POST.get('estimated_delivery')
        product_expiry = 	request.POST.get('product_expiry')
        if(curr_low_bid>bid_rate):
                curr_low_bid= bid_rate
                user=Customer_Requirement.objects.get(product_id=requirement_ID)
                user.lowest_bid= curr_low_bid
                user.save()
        bid_detail= Bid(bid_rate=bid_rate,mrp=mrp, name = data.name, product_expiry=product_expiry,expected_delivery=estimated_delivery,vendor_id=vendor_id,requirement_id=requirement_ID,customer_id=customer_id, supply_pincode= pincode)
        bid_detail.save()
    return redirect('vendors:mybids')
    
@login_required
@vendor_required
@email_verification_required
def OrdersList(request):
    data = vendor_Detail.objects.get(vendor_id=request.user)
    ven = Order.objects.filter(vendor_id=request.user).order_by('-requirement_id')
    ven1 = Order_From_Order4Sure.objects.filter(vendor_id=request.user).order_by('-order_id')

    
    pay = Order.objects.filter(customer_payment_approved=False)
  
    
    data1=Bid.objects.values_list('requirement_id', flat=True).filter(vendor_id=request.user)
    bidid = Bid.objects.values_list('Bid_id', flat=True).filter(vendor_id=request.user)
    nav = Customer_Requirement.objects.filter(product_id__in=data1)
    data2 = Bid.objects.filter(Bid_id__in=data1)
    iii = Completed_Order.objects.filter(invoice_uploaded = True)
        
    
    
   

   
    
    context = {'data':data, 'ven':ven, 'ven1':ven1, 'pay':pay, 'data2':data2, 'iii':iii}
    if request.method == "POST":
        comp = request.POST['complete']
        bill = request.FILES['invoice']
        id = request.POST['idd']
        comp_order = Order.objects.get(order_id=id)
        customer_id = comp_order.customer_id
        vendor_id = comp_order.vendor_id
        requirement_id =  comp_order.requirement_id
        name=  comp_order.name
        quantity =  comp_order.quantity
        pincode = comp_order.pincode
        order_amount = comp_order.order_amount
        expected_delivery = comp_order. expected_delivery
        delivery_contact= comp_order.delivery_contact
        bid_id =  comp_order.bid_id
        delivery_address =  comp_order.delivery_address
        pay = comp_order.customer_payment_image

        
        
        ordersa = Completed_Order(invoice_uploaded=True,invoice=bill,customer_payment_image=pay,customer_id=customer_id, vendor_id=vendor_id,requirement_id=requirement_id,name=name,quantity=quantity,pincode=pincode,order_amount=order_amount,expected_delivery=expected_delivery,delivery_contact=delivery_contact,bid_id=bid_id,delivery_address=delivery_address)
        ordersa.save()
        comp_order.completed = True
        comp_order.save()


        messages.success(request, "Thank You From Order4Sure and Congratulations for your order has been Completed. ")
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.connect(settings.EMAIL_HOST, 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
        msg = f'from: OrderforSure <info@orderforsure.com>\nTo: order4sure.in@gmail.com  \nSubject: Your Invoice from {vendor_id} \n\n You can download Invoice from your dashboard in Bid Order section.'
        s.sendmail('OrderforSure <info@orderforsure.com>', 'order4sure.in@gmail.com', msg)
        




         
    return render(request, 'bid/vendors/orders.html', context)


global pin
pin = 0
@login_required
@vendor_required
def vendor_email_verify(request):
    global pin
    value = User.objects.get(id=request.user.id)
    if request.method == "POST":
        otp = request.POST['OTP']
        if (int(otp)==int(pin)):
            value.email_verified = True
            value.username = value.email
            value.save()
            return redirect('vendors:vendor_details')
        else:
            value.delete()
            return redirect('signup')
    else:
        pin = random.randint(121121, 982379)
       
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.connect(settings.EMAIL_HOST, 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
        msg = f'from: OrderforSure <info@orderforsure.com>\nTo: {value}\nSubject: OTP Verification\n\n Your Verification OTP is {pin}'
        s.sendmail('OrderforSure <info@orderforsure.com>', f'{value}', msg)
    
    return render(request, 'registration/vendors_email_verify.html')


def delete_interest(request):
    if request.method=="POST":
        if 'xd' in request.POST:
            iii = request.POST['xd']
            hello = Vendor_brands.objects.filter(vendor_id = request.user, brand_interest=iii)
            hello.delete()
        if 'cd' in request.POST:
            yyy = request.POST['cd']
            hello2 = Vendor_category.objects.filter(vendor_id= request.user, category_interest=yyy)
            hello2.delete()
        
       
        
        
            
    return redirect('vendors:vendorInterestsView')



@login_required
@vendor_required
@email_verification_required
def OrdersList1(request):
    data = vendor_Detail.objects.get(vendor_id=request.user)
    ven1 = Order_From_Order4Sure.objects.filter(vendor_id=request.user).order_by('-order_id')
    context = {'data':data, 'ven1':ven1,}
    if request.method == "POST":
        comp = request.POST['complete']
        bill = request.FILES['bill']
        id = request.POST['idd']
        comp_order = Order_From_Order4Sure.objects.get(order_id=id)
        customer_id = comp_order.customer_id
        vendor_id = comp_order.vendor_id
        requirement_id =  id
        name=  comp_order.name
        quantity =  comp_order.quantity
        pincode = comp_order.pincode
        order_amount = comp_order.order_amount
        expected_delivery = comp_order. expected_delivery
        delivery_contact= comp_order.delivery_contact
        bid_id =  id
        delivery_address =  comp_order.delivery_address
        pay = comp_order.customer_payment_image

        
        
        ordersa = Completed_Order(invoice_uploaded=True,invoice=bill,customer_payment_image=pay,customer_id=customer_id, vendor_id=vendor_id,requirement_id=requirement_id,name=name,quantity=quantity,pincode=pincode,order_amount=order_amount,expected_delivery=expected_delivery,delivery_contact=delivery_contact,bid_id=bid_id,delivery_address=delivery_address)
        ordersa.save()
        comp_order.invoice = bill
        comp_order.save()
        comp_order.completed = True
        comp_order.save()


        messages.success(request, "Thank You From Order4Sure and Congratulations for your order has been Completed. ")
        s = smtplib.SMTP(settings.EMAIL_HOST)
        s.connect(settings.EMAIL_HOST, 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
    
        msg = f'from: OrderforSure <info@orderforsure.com>\nTo: order4sure.in@gmail.com \nSubject: Your Invoice from {vendor_id} \n\n You can download Invoice from your dashboard in Store Order section.'
        s.sendmail('OrderforSure <info@orderforsure.com>', 'order4sure.in@gmail.com', msg)
        return redirect('vendors:orders')

@login_required
@vendor_required
@email_verification_required
def upload_products(request):
    if request.method == "POST":
        std = request.FILES['files']
        user333 = request.user
        new = vendor_products_file( productfile=std, vendor_id=user333)
        new.save()

    return render(request, 'upprod.html')

