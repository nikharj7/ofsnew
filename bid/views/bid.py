from multiprocessing import context
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from datetime import datetime, timedelta
from ..decorators import vendor_required, customer_required
import smtplib
from django.conf import settings
from ..models import  Category, User, Banner, vendor_Detail, Brands, customer_Detail, Product, Customer_Requirement, Bid, Order, Order_From_Order4Sure
from django.contrib import messages
import random
from bid.models import Contact_Us, preorder, Product
from django.core.paginator import Paginator
from bid.templatetags import cart
from datetime import date
from django.db.models import Min
from datetime import timedelta
from django.utils import timezone
from datetime import date, datetime, time, timedelta





class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def Search(request):
    cart = request.session.get('cart')
    if not cart:
        request.session.cart = {}
    pp = Product.objects.all()
    cat = Category.objects.all()[:8]
    query = request.GET['query']
    if len(query)>80:
        allProducts = Product.objects.none()
    else:
        allProductsProducts = Product.objects.filter(name__icontains=query) 
        allProductsDescription = Product.objects.filter(description__icontains=query)
        allProductsPrice = Product.objects.filter(price__icontains=query)
        allProducts = allProductsProducts.union(allProductsDescription, allProductsPrice)
    
    if allProducts.count() == 0:
        messages.warning(request, "No search results. Please refine your query.")
    allprod = Product.objects.all().order_by("-price")[0:5]
    pp = Product.objects.all()
    if request.method == "POST":
        prod = request.POST.get('carttt') 
        qty = request.POST.get('qwe')   
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(prod)
            if quantity:
                if qty:
                    cart[prod] = quantity+int(qty)
            else:
                cart[prod] = int(qty)
        else:
            cart = {}
            cart[prod] = int(qty)
        request.session['cart'] = cart
        params = {'allProducts': allProducts, 'pp':pp, 'query':query, 'allprod':allprod, 'cart':cart, 'searchP':searchP, 'products':products}
        return render(request, 'search.html', params)
    if request.session.get('cart'):
        ids = (list(request.session.get('cart').keys()))
        products = Product.get_product_by_ids(ids)
        pp = Product.objects.all()
        params = {'allProducts': allProducts, 'query':query, 'pp':pp, 'allprod':allprod, 'products':products}
        return render(request, 'search.html', params)
    searchP = Product.objects.all()
    params = {'allProducts': allProducts, 'searchP':searchP, 'query':query, 'cat':cat, 'pp':pp, 'allprod':allprod,}
    return render(request, 'search.html', params)

def product(request, slug):
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                searchP = Product.objects.all()
                cat = Category.objects.all()[:8]
                allprod = Product.objects.all().order_by("-price")[0:5]
                pp = Product.objects.all()
                post = Product.objects.filter(slug=slug).first()
                if request.method == "POST":
                    prod = request.POST.get('carttt') 
                    qty = request.POST.get('qtybutton')
                    
                    cart = request.session.get('cart')
                    if cart:
                        quantity = cart.get(prod)
                        if quantity:
                            if qty:
                                cart[prod] = quantity+int(qty)
                        else:
                            cart[prod] = int(qty)
                    else:
                        cart = {}
                        cart[prod] = int(qty)
                    request.session['cart'] = cart
                    return redirect('Cart_products')
               
                context = {'data':data,'post':post, 'searchP':searchP, 'cat':cat, 'allprod':allprod, 'pp':pp}
                return render(request, 'product-details.html', context )

            else:
                if request.user.is_vendor:
                    if vendor_Detail.objects.filter(vendor_id=request.user.id):
                        data = vendor_Detail.objects.get(vendor_id=request.user.id)
                        searchP = Product.objects.all()
                        cat = Category.objects.all()[:8]
                        allprod = Product.objects.all().order_by("-price")[0:5]
                        pp = Product.objects.all()
                        post = Product.objects.filter(slug=slug).first()
                        if request.method == "POST":
                            prod = request.POST.get('carttt') 
                            qty = request.POST.get('qtybutton')
                            
                            cart = request.session.get('cart')
                            if cart:
                                quantity = cart.get(prod)
                                if quantity:
                                    if qty:
                                        cart[prod] = quantity+int(qty)
                                else:
                                    cart[prod] = int(qty)
                            else:
                                cart = {}
                                cart[prod] = int(qty)
                            request.session['cart'] = cart
                            return redirect('Cart_products')
                    
                        context = {'data':data,'post':post, 'searchP':searchP, 'cat':cat, 'allprod':allprod, 'pp':pp}
                        return render(request, 'product-details.html', context )


    post = Product.objects.filter(slug=slug).first()
    searchP = Product.objects.all()
    cat = Category.objects.all()[:8]
    allprod = Product.objects.all().order_by("-price")[0:5]
    pp = Product.objects.all()
    if request.method == "POST":
        prod = request.POST.get('carttt') 
        qty = request.POST.get('qtybutton')
                    
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(prod)
            if quantity:
                if qty:
                    cart[prod] = quantity+int(qty)
            else:
                cart[prod] = int(qty)
        else:
            cart = {}
            cart[prod] = int(qty)
        request.session['cart'] = cart
        return redirect('Cart_products')

    context = {'post':post, 'searchP':searchP, 'cat':cat, 'allprod':allprod, 'pp':pp}
    return render(request, 'product-details.html', context )


def vendor_product(request,slug):
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                vendor_prods = Product.objects.filter(slug=slug).first()
                prod4 = Product.objects.filter(slug=vendor_prods.slug).first()
                if prod4.short_description:
                    prod4 = prod4.short_description.replace("_x000D_", "")
                    vendor_prods.short_description = prod4
                    vendor_prods.save()
                prod3 = Product.objects.filter(slug=vendor_prods.slug).first()
                if prod3.description:
                    prod3 = prod3.description.replace("_x000D_", "")
                    vendor_prods.description = prod3
                    vendor_prods.save()
                if request.method == "POST":
                    pimg = vendor_prods.image1
                    desc = vendor_prods.description
                    pname = vendor_prods.name
                    price = vendor_prods.price
                    pr = vendor_prods.SKU
                    cate = vendor_prods.category
                    mrp = vendor_prods.mrp
                    brand = vendor_prods.Brand
                    qty = vendor_prods.quantity
                    step_qty = vendor_prods.step_up_quantity
                    customer = request.user
                    slug = vendor_prods.slug
                    pre = preorder(step_up_quantity=step_qty,mrp=mrp,product_ref_no=pr,price=price,description=desc,brand=brand,slug=slug,product_image=pimg,name=pname,category=cate,quantity=qty,customer=customer)
                    pre.save()
                    return redirect('customers:customer_requirement')
                products = ''
                if request.session.get('cart'):
                    ids = (list(request.session.get('cart').keys()))
                    products = Product.get_product_by_ids(ids)
                allprod = Product.objects.all().order_by("-price")[0:5]
                context = {'data':data,'vendor_prods':vendor_prods, 'allprod':allprod, 'products':products}
                return render(request, 'vendor-product-details.html', context )
            else:
                if request.user.is_vendor:
                    if vendor_Detail.objects.filter(vendor_id=request.user.id):
                        data = vendor_Detail.objects.get(vendor_id=request.user.id)
                        vendor_prods = Product.objects.filter(slug=slug).first()
                        prod4 = Product.objects.filter(slug=vendor_prods.slug).first()
                        if prod4.short_description:
                            prod4 = prod4.short_description.replace("_x000D_", "")
                            vendor_prods.short_description = prod4
                            vendor_prods.save()
                        prod3 = Product.objects.filter(slug=vendor_prods.slug).first()
                        if prod3.description:
                            prod3 = prod3.description.replace("_x000D_", "")
                            vendor_prods.description = prod3
                            vendor_prods.save()

                        if request.method == "POST":
                            prod = request.POST['carttt']
                            qty = request.POST['qwe']
                            
                            cart = request.session.get('cart')
                            if cart:
                                quantity = cart.get(prod)
                                if quantity:
                                    if qty:
                                        cart[prod] = quantity+int(qty)
                                else:
                                    cart[prod] = int(qty)
                            else:
                                cart = {}
                                cart[prod] = int(qty)
                            request.session['cart'] = cart
                            return redirect('Cart_products')
                        products = ''
                        if request.session.get('cart'):
                            ids = (list(request.session.get('cart').keys()))
                            products = Product.get_product_by_ids(ids)
                        allprod = Product.objects.all().order_by("-price")[0:5]
                        context = {'data':data,'vendor_prods':vendor_prods, 'allprod':allprod, 'products':products,}
                        return render(request, 'vendor-product-details.html', context )

    vendor_prods = Product.objects.filter(slug=slug).first()
    prod4 = Product.objects.filter(slug=vendor_prods.slug).first()
    if prod4.short_description:
        prod4 = prod4.short_description.replace("_x000D_", "")
        vendor_prods.short_description = prod4
        vendor_prods.save()
    prod3 = Product.objects.filter(slug=vendor_prods.slug).first()
    if prod3.description:
        prod3 = prod3.description.replace("_x000D_", "")
        vendor_prods.description = prod3
        vendor_prods.save()


    if request.method == "POST":
        prod = request.POST['carttt']
        qty = request.POST['qwe']
                    
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(prod)
            if quantity:
                if qty:
                    cart[prod] = quantity+int(qty)
            else:
                cart[prod] = int(qty)
        else:
            cart = {}
            cart[prod] = int(qty)
        request.session['cart'] = cart
        return redirect('Cart_products')
    products = ''
    if request.session.get('cart'):
        ids = (list(request.session.get('cart').keys()))
        products = Product.get_product_by_ids(ids)
    allprod = Product.objects.all().order_by("-price")[0:5]
    
    context = {'vendor_prods':vendor_prods, 'products':products, 'allprod':allprod}
    return render(request, 'vendor-product-details.html', context)

def Store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session.cart = {}
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                pp = Product.objects.all()
                cat = Category.objects.all().order_by("?")[:8]
                prod_brand = Brands.objects.all().order_by("?")[:8]
                product = Product.objects.all().order_by("-created")
                searchP = Product.objects.all()
                allprod = Product.objects.all().order_by("-price").order_by("?")[:5]
                paginator = Paginator(pp, 12)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                cate = request.GET.get('cate')
                catee = Product.objects.filter(category=cate)
                paginator1 = Paginator(catee, 12)
                page_number1 = request.GET.get('page')
                page_obj1 = paginator1.get_page(page_number1)
                Brandss = request.GET.get('brand')
                brand = Product.objects.filter(Brand=Brandss)
                paginator12 = Paginator(brand, 12)
                page_number12 = request.GET.get('page')
                page_obj12= paginator12.get_page(page_number12)
                pre = preorder.objects.filter(complete=False)
                for i in pre:
                    req_time = preorder.objects.filter(created_at=i.created_at + timedelta(minutes=3))
                    req_time.delete()
                

                if request.session.get('cart'):
                    ids = (list(request.session.get('cart').keys()))
                    products = Product.get_product_by_ids(ids)
                        
                    context = {'data':data,'product':product, 'brand':brand, 'prod_brand':prod_brand, 'page_obj12':page_obj12 ,'searchP':searchP, 'allprod':allprod, 'page_obj':page_obj, 'page_obj1':page_obj1, 'pp':pp, 'cat':cat, 'catee':catee,'cart':cart,'products':products}
                    return render(request, 'shop.html', context)
                context = {'data':data,'product':product, 'allprod':allprod, 'brand':brand, 'prod_brand':prod_brand, 'page_obj':page_obj, 'page_obj1':page_obj1, 'pp':pp, 'cat':cat, 'catee':catee, }
                return render(request, 'shop.html', context)
        else:
            if vendor_Detail.objects.filter(vendor_id=request.user.id):
                data = vendor_Detail.objects.get(vendor_id=request.user.id)
                pp = Product.objects.all()
                prod_brand = Brands.objects.all()[:8]
                cat = Category.objects.all()[:8]
                searchP = Product.objects.all()
                product = Product.objects.all().order_by("?")
                allprod = Product.objects.all().order_by("?")[0:5]
                paginator = Paginator(pp, 12)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                cate = request.GET.get('cate')
                catee = Product.objects.filter(category=cate)
                paginator1 = Paginator(catee, 12)
                page_number1 = request.GET.get('page')
                page_obj1 = paginator1.get_page(page_number1)
                Brandss = request.GET.get('brand')
                brand = Product.objects.filter(Brand=Brandss)
                paginator12 = Paginator(brand, 12)
                page_number12 = request.GET.get('page')
                page_obj12= paginator12.get_page(page_number12)
            
                if request.session.get('cart'):
                    ids = (list(request.session.get('cart').keys()))
                    products = Product.get_product_by_ids(ids)
                    context = {'data':data,'product':product, 'products':products, 'brand':brand, 'prod_brand':prod_brand, 'brand':brand, 'page_obj12':page_obj12 , 'searchP':searchP, 'allprod':allprod, 'page_obj':page_obj, 'page_obj1':page_obj1, 'pp':pp, 'cat':cat, 'catee':catee}
                    return render(request, 'shop.html', context)
                context = {'data':data,'product':product, 'searchP':searchP, 'brand':brand, 'prod_brand':prod_brand, 'allprod':allprod, 'page_obj':page_obj, 'page_obj1':page_obj1, 'pp':pp, 'cat':cat, 'catee':catee}
                return render(request, 'shop.html', context)
    else:
        pp = Product.objects.all()
        cat = Category.objects.all()[:8]
        prod_brand = Brands.objects.all()[:8]
        product = Product.objects.all().order_by("?")
        allprod = Product.objects.all().order_by("?")[0:5]
        searchP = Product.objects.all()
        paginator = Paginator(pp, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        cate = request.GET.get('cate')
        catee = Product.objects.filter(category=cate)
        paginator1 = Paginator(catee, 12)
        page_number1 = request.GET.get('page')
        page_obj1 = paginator1.get_page(page_number1)
        Brandss = request.GET.get('brand')
        brand = Product.objects.filter(Brand=Brandss)
        paginator12 = Paginator(brand, 12)
        page_number12 = request.GET.get('page')
        page_obj12= paginator12.get_page(page_number12)


        if request.session.get('cart'):
            ids = (list(request.session.get('cart').keys()))
            products = Product.get_product_by_ids(ids)
            context = {'product':product, 'products':products, 'brand':brand, 'prod_brand':prod_brand, 'searchP':searchP, 'allprod':allprod, 'page_obj':page_obj, 'page_obj1':page_obj1, 'pp':pp, 'cat':cat, 'catee':catee, 'brand':brand, 'page_obj12':page_obj12 ,}
            return render(request, 'shop.html', context)
    context = {'product':product, 'searchP':searchP, 'allprod':allprod, 'brand':brand, 'prod_brand':prod_brand, 'page_obj':page_obj, 'page_obj1':page_obj1, 'pp':pp, 'cat':cat, 'catee':catee}
    return render(request, 'shop.html', context)

def home(request):
    banner = Banner.objects.all()
    cart = request.session.get('cart')
    if not cart:
        request.session.cart = {}
    else:
        if request.session.get('cart'):
            ids = (list(request.session.get('cart').keys()))
            products = Product.get_product_by_ids(ids)

    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                searchP = Product.objects.all()
                product = Product.objects.all().order_by("?")[0:9]
                product1 = Product.objects.all
                banner = Banner.objects.all()
                cat = Category.objects.all()[:8]
                bar = Brands.objects.all()
                pre = preorder.objects.filter(complete=False)
                for i in pre:
                    req_time = preorder.objects.filter(created_at=i.created_at + timedelta(minutes=3))
                    req_time.delete()
                
                
                if request.session.get('cart'):
                    ids = (list(request.session.get('cart').keys()))
                    products = Product.get_product_by_ids(ids)
                    context = {'data':data, 'product':product, 'banner':banner, 'searchP':searchP, 'products':products, 'product1':product1, 'bar':bar, 'cat':cat, 'cart':cart}
                    return render(request, 'index.html', context )
                    
                context = {'data':data, 'banner':banner, 'searchP':searchP, 'product1':product1, 'product':product,  'cat':cat, 'bar':bar, 'cart':cart}
                return render(request, 'index.html', context )
                
                
            else:
                return redirect('customers:customer_profile')
        else:
            if vendor_Detail.objects.filter(vendor_id=request.user.id):
                data = vendor_Detail.objects.get(vendor_id=request.user.id)
                product = Product.objects.all().order_by("?")[0:9]
                searchP = Product.objects.all()
                product1 = Product.objects.all()
                banner = Banner.objects.all()
                bar = Brands.objects.all()
                banner = Banner.objects.all()
                cat = Category.objects.all()[:8]
                if request.session.get('cart'):
                    ids = (list(request.session.get('cart').keys()))
                    products = Product.get_product_by_ids(ids)
                    contexti = {'data':data, 'banner':banner, 'products':products, 'searchP':searchP, 'product1':product1, 'product':product, 'bar':bar, 'cat':cat}
                    return render(request, 'index.html', contexti)
                contexti = {'data':data, 'banner':banner, 'searchP':searchP, 'product1':product1, 'product':product, 'bar':bar, 'cat':cat}
                return render(request, 'index.html', contexti)
            else:
                return redirect('vendors:vendor_profile')
    else:
        product = Product.objects.all().order_by("?")[0:9]
        product1 = Product.objects.all()
        searchP = Product.objects.all()
        cat = Category.objects.all()[:8]
        bar = Brands.objects.all()
        banner = Banner.objects.all()
        if request.session.get('cart'):
            ids = (list(request.session.get('cart').keys()))
            products = Product.get_product_by_ids(ids)
            context = {'product':product, 'products':products, 'banner':banner, 'searchP':searchP, 'product1':product1, 'cat':cat, 'bar':bar}
            return render(request, 'index.html', context)
        
    context = {'product':product, 'banner':banner, 'searchP':searchP, 'product1':product1, 'cat':cat, 'bar':bar}
    return render(request, 'index.html', context)
    







def Contact(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                cat = Category.objects.all().order_by("?")[:8]
                context = {'data':data, 'cat':cat}
                if request.method == "POST":
                    email = request.POST['email']
                    name = request.POST['name']
                    subject = request.POST['subject']
                    message = request.POST['message']
                    contacts = Contact_Us(Email=email, Name=name, Subject=subject, Message=message)
                 
                    contacts.save()
                    messages.success(request, 'Your Response has been submited succesfully.')
                return render(request, 'contact.html', context )
            else:
                return redirect('customers:customer_profile')
        else:
            if vendor_Detail.objects.filter(vendor_id=request.user.id):
                data = vendor_Detail.objects.get(vendor_id=request.user.id)
                cat = Category.objects.all().order_by("?")[:8]
                if request.method == "POST":
                    email = request.POST['email']
                    name = request.POST['name']
                    subject = request.POST['subject']
                    message = request.POST['message']
                    contacts = Contact_Us(Email=email, Name=name, Subject=subject, Message=message)
                    
                    contacts.save()
                    messages.success(request, 'Your Response has been submited succesfully.')
                contexti = {'data':data, 'cat':cat}
                return render(request, 'contact.html', contexti)
    cat = Category.objects.all().order_by("?")[:8]
    return render(request, 'contact.html', {'cat':cat} )


def About(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                cat = Category.objects.all().order_by("?")[:8]
                context = {'data':data, 'cat':cat}
                return render(request, 'about.html', context )
            else:
                return redirect('customers:customer_profile')
        else:
            if vendor_Detail.objects.filter(vendor_id=request.user.id):
                data = vendor_Detail.objects.get(vendor_id=request.user.id)
                cat = Category.objects.all().order_by("?")[:8]
                contexti = {'data':data, 'cat':cat}
                return render(request, 'about.html', contexti)
    cat = Category.objects.all().order_by("?")[:8]
    return render(request, 'about.html', {'cat':cat} )

def Cart_products(request):
    if customer_Detail.objects.filter(customer_id=request.user.id):
               
        data = customer_Detail.objects.get(customer_id=request.user.id)
        if request.session.get('cart'):
            ids = (list(request.session.get('cart').keys()))
            products = Product.get_product_by_ids(ids)
          
            cart = request.session.get('cart')
                    
                    
            if not cart:
                request.session.cart = {}
            if request.method == "POST":
                prod = request.POST.get('prodd')
                qqq = request.POST.get('qwe')
                     
                remove = request.POST.get('remove')  
                add = request.POST.get('add')              

                cart = request.session.get('cart')
                        
                if cart:
                    quantity = cart.get(prod)
                            
                    if quantity:
                        if remove:
                            cart[prod] = quantity-int(qqq)
                                    
                        if add:
                            cart[prod] = quantity+int(qqq)    
                    else:
                        cart[prod] = int(qqq)
                else:
                    cart = {}
                    cart[prod] = int(qqq)
                request.session['cart'] = cart 
            if request.session.get('cart'):
                ids = (list(request.session.get('cart').keys()))
                products = Product.get_product_by_ids(ids)
            context = {'data':data, 'products':products,}
            return render(request, 'cart.html',context)  
    else:
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        if request.session.get('cart'):
            ids = (list(request.session.get('cart').keys()))
            products = Product.get_product_by_ids(ids)
            for i in products:
                i.quantity
          
            cart = request.session.get('cart')
                    
                    
            if not cart:
                request.session.cart = {}
            if request.method == "POST":
                prod = request.POST.get('prodd')
                qqq = request.POST.get('qwe')
                     
                remove = request.POST.get('remove')  
                add = request.POST.get('add')              

                cart = request.session.get('cart')
                        
                if cart:
                    quantity = cart.get(prod)
                    print(quantity)
                            
                    if quantity:
                        if remove:
                            cart[prod] = quantity-int(qqq)
                                    
                        if add:
                            cart[prod] = quantity+int(qqq)    
                    else:
                        cart[prod] = int(qqq)
                else:
                    cart = {}
                    cart[prod] = int(qqq)
                request.session['cart'] = cart 
            if request.session.get('cart'):
                ids = (list(request.session.get('cart').keys()))
                products = Product.get_product_by_ids(ids)
            context = { 'products':products,}
            return render(request, 'cart.html',context)

    return render(request, 'cart.html',)


def Checkout(request):
    cart = request.session.get('cart')
    if not cart:
        request.session.cart = {}
    else:
        ids = (list(request.session.get('cart').keys()))
        products = Product.get_product_by_ids(ids)
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                cart = request.session.get('cart')
                if not cart:
                    request.session.cart = {}
                data = customer_Detail.objects.get(customer_id=request.user.id)
                if request.session.get('cart'):
                    ids = (list(request.session.get('cart').keys()))
                    

                    products = Product.get_product_by_ids(ids)
                
                    
                        
                    context = {'data':data, 'products':products}
    context = {'products':products}
    
    return render(request, 'checkout.html', context)

@customer_required
def addtocart(request):
    if request.method == "POST":
        prod = request.POST['carttt']
        qty = request.POST['qwe']
                            
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(prod)
            if quantity:
                if qty:
                    cart[prod] = quantity+int(qty)
            else:
                cart[prod] = int(qty)
        else:
            cart = {}
            cart[prod] = int(qty)
        request.session['cart'] = cart
        messages.success(request, 'Added in Cart ')
        return redirect('Cart_products')

            
  
        
        
       


def payment(request):
    if request.session.get('cart'):
        ids = (list(request.session.get('cart').keys()))
                    

        products = Product.get_product_by_ids(ids)
    if request.method == "POST":
                    
        first_name = request.POST['ltn__name']
        last_name = request.POST['ltn__lastname']
        email = request.POST['ltn__email']
        phone = request.POST['ltn__phone']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        gst = request.POST['gst']
        drug = request.POST['drug']
        city = request.POST['city']
        state = request.POST.get('state')
        pin = request.POST['pincode']
        pay = request.FILES['pay']
        cart = request.session.get('cart')
        additional = request.POST['ltn__message']
        cusom_id = email        
        g = timezone.now().date() + timedelta(days=7)
          
        for i in products:
            quantity = cart.get(str(i.id))
            customerr = Order_From_Order4Sure(GST=gst,Drug=drug,customer_payment_image=pay,order_date=timezone.now().date(), quantity = quantity, pincode=pin, order_amount=int(quantity) * int(i.price) , expected_delivery=g, delivery_contact=phone, delivery_address=(address1 + ' ' + address2 + ' ' + city + ' ' + state), customer_id=email, vendor_id=i.Vendor, customer_name = (first_name + ' ' + last_name),name=i.name, product_image=i.image1,customer_payment_proof=True, customer_payment_status="CHECKING FOR TRANSACTION")
            customerr.save()
            success_order = Order_From_Order4Sure.objects.filter(customer_payment_proof=True).last()
            s = smtplib.SMTP(settings.EMAIL_HOST)
                        
            s.connect(settings.EMAIL_HOST, 587)
            s.starttls()
            s.login(settings.EMAIL_HOST_USERNAME, settings.EMAIL_HOST_PASSWORD)
                    
            msg = f'from: OrderforSure <info@orderforsure.com>\nTo: order4sure.in@gmail.com\nSubject: New Order Placed by Customer {cusom_id}, order date {timezone.now().date()} \n\n Hello Admin, \n\n There is new order placed by {cusom_id}. Order Details are as Follow - : \n Order Date = {timezone.now().date()} \n Order ID = {success_order.order_id} \n Vendor = {i.Vendor} \n Customer = {cusom_id} \n Customer Name = {first_name} {last_name} \n Product = {i.name} \n quantity= {quantity} \n Pincode = {pin} \n Contact = {phone} \n Address = {address1} {address2} {city} {state} {pin} '
            s.sendmail('OrderforSure <info@orderforsure.com>', 'order4sure.in@gmail.com', msg)
        
        
        messages.success(request, 'Thank you for shopping with us. Your order has been placed Succesfully. Please Check Your Email for more details.')
        
        return redirect('Success')
    else:
        return redirect('Cart_products')


def Success(request):
    cart = request.session.get('cart')
    if not cart:
        request.session.cart = {}
        return redirect('/')
    success_order = Order_From_Order4Sure.objects.filter(customer_payment_proof=True).last()
    if request.session.get('cart'):
        ids = (list(request.session.get('cart').keys()))
        products = Product.get_product_by_ids(ids)
    if request.method=="POST":
        request.session['cart'] = {}
        return redirect('/')
    context = {'success_order':success_order, 'products':products}
    return render(request, 'success.html', context, )
        
    
    

def orders(request):
    data = customer_Detail.objects.get(customer_id=request.user.id)
    orders = Order_From_Order4Sure.objects.filter(customer_id=request.user).order_by('-order_id')
   
    context = {'orders':orders, 'data':data}
    return render(request, 'cart_update.html', context)

def Privacy_Policy(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                cat = Category.objects.all()[:8]
                return render(request, 'privacy.html', {'data':data, 'cat':cat})

        else:
            if vendor_Detail.objects.filter(vendor_id=request.user.id):
                data = vendor_Detail.objects.get(vendor_id=request.user.id)
                cat = Category.objects.all()[:8]
                return render(request, 'privacy.html', {'data':data, 'cat':cat})
    else:
        cat = Category.objects.all()[:8]
        return render(request, 'privacy.html', {'cat':cat})
    cat = Category.objects.all()[:8]
    return render(request, 'privacy.html',{'data':data, 'cat':cat})
    


def terms_and_conditions(request):
    cat = Category.objects.all()[:8]
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                cat = Category.objects.all()[:8]
                return render(request, 't&c.html',{'data':data, 'cat':cat})
        else:
            if vendor_Detail.objects.filter(vendor_id=request.user.id):
                data = vendor_Detail.objects.get(vendor_id=request.user.id)
                cat = Category.objects.all()[:8]
                return render(request, 't&c.html',{'data':data, 'cat':cat})
    else:
        cat = Category.objects.all()[:8]
        return render(request, 't&c.html', {'cat':cat})
    cat = Category.objects.all()[:8]
    return render(request, 't&c.html',{'data':data, 'cat':cat})




def removeprod(request):
    if request.method == "POST":
        removep  = request.POST['prodid']
        cart = request.session.get('cart')
        if cart:
            cart.pop(removep)
        request.session['cart'] = cart
        return redirect('Cart_products')

def Track_Order(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            if customer_Detail.objects.filter(customer_id=request.user.id):
                data = customer_Detail.objects.get(customer_id=request.user.id)
                if request.method == "POST":
                    orderid = request.POST['orderid']
                    orderemail = request.POST['orderemail']
                    if Order.objects.filter(order_id=orderid, customer_id = orderemail):
                        orderss = Order.objects.get(order_id=orderid, customer_id = orderemail)
                        context = {'orderss':orderss, 'data':data}
                        return render(request, 'ordertracking.html', context)
                    else:
                        pass

                    if Order_From_Order4Sure.objects.filter(order_id=orderid, customer_id = orderemail):
                        orderss1 = Order_From_Order4Sure.objects.get(order_id=orderid, customer_id = orderemail)
                        context = {'orderss1':orderss1, 'data':data}
                        return render(request, 'ordertracking.html', context)
                    else:
                        pass
        else:
            if vendor_Detail.objects.filter(vendor_id=request.user.id):
                data = vendor_Detail.objects.get(vendor_id=request.user.id)
                if request.method == "POST":
                    orderid = request.POST['orderid']
                    orderemail = request.POST['orderemail']
                    if Order.objects.filter(order_id=orderid, customer_id = orderemail):
                        orderss = Order.objects.get(order_id=orderid, customer_id = orderemail)
                        context = {'orderss':orderss, 'data':data}
                        return render(request, 'ordertracking.html', context)
                    else:
                        pass

                    if Order_From_Order4Sure.objects.filter(order_id=orderid, customer_id = orderemail):
                        orderss1 = Order_From_Order4Sure.objects.get(order_id=orderid, customer_id = orderemail)
                        context = {'orderss1':orderss1, 'data':data}
                        return render(request, 'ordertracking.html', context)
                    else:
                        pass
    if request.method == "POST":
        orderid = request.POST['orderid']
        orderemail = request.POST['orderemail']
        if Order.objects.filter(order_id=orderid, customer_id = orderemail):
            orderss = Order.objects.get(order_id=orderid, customer_id = orderemail)
            context = {'orderss':orderss}
            return render(request, 'ordertracking.html', context)
        else:
            pass

        if Order_From_Order4Sure.objects.filter(order_id=orderid, customer_id = orderemail):
            orderss1 = Order_From_Order4Sure.objects.get(order_id=orderid, customer_id = orderemail)
            context = {'orderss1':orderss1}
            return render(request, 'ordertracking.html', context)
        else:
            pass

    return render(request, 'ordertracking.html')

def howitworks(request):
    cat = Category.objects.all().order_by("?")[:8]
    return render(request, 'howitworks.html', {'cat':cat})

def listed_Vendors(request):
    users = User.objects.filter(is_vendor=True).exclude(is_staff=True)   
    return render(request, 'listedvendor.html', {'users':users})

def listed_Vendors_details(request, slug):
    users = User.objects.filter(first_name=slug).first()
    print(users)
    return  render (request, 'vendordetail.html', {"users":users})