from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import bid, vendors, customers
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', bid.home, name='home'),
    # path('product/<str:slug>', bid.product, name='product'),
    path('Contact', bid.Contact, name='Contact'),
    path('About', bid.About, name='About'),
    path('Store', bid.Store, name='Store'),
    path('Search', bid.Search, name='Search'),
    path('Cart_products', bid.Cart_products, name='Cart_products'),
    path('Checkout', bid.Checkout, name='Checkout'),
    path('vendor_product/<str:slug>', bid.vendor_product, name='vendor_product'),
    path('payment', bid.payment, name='payment'),
    path('orders', bid.orders, name='Orders'),
    path('terms_and_conditions', bid.terms_and_conditions, name='terms_and_conditions'),
    path('Privacy_Policy', bid.Privacy_Policy, name='Privacy_Policy'),
    path('addtocart', bid.addtocart, name='addtocart'),
    path('removeprod', bid.removeprod, name='removeprod'),
    path('Track_Order', bid.Track_Order, name='Track_Order'),
    path('Success', bid.Success, name='Success'),
    path('howitworks', bid.howitworks, name='howitworks'),
    path('listed_Vendors', bid.listed_Vendors, name='listed_Vendors'),
    path('listed_Vendors_details/<str:slug>', bid.listed_Vendors_details, name='listed_Vendors_details'),

    







    











  
    
    path('vendors/', include(([
        path('', vendors.profile, name='vendor_profile'),
        path('vendor_details', vendors.vendor_details, name='vendor_details'),
        path('vendorInterests/', vendors.vendorInterests.as_view(), name='vendorInterestsView'),
        path('vendorInterests/submit_interests', vendors.submit_interests, name='submit_interests'),
        path('profile/', vendors.view_profile, name='view_profile'),
        path('BidList/', vendors.BidListView, name='BidList'),
        path('BidList/<int:pk>/', vendors.requirement_detail, name='requirement_detail'),
        path('BidList/submit', vendors.SubmitBid, name='submit_bid'),
        path('VendorBid/', vendors.VendorBid, name='BidForm'),
        path('MyBids/', vendors.MyBidsList, name='mybids'),
        path('Orders', vendors.OrdersList, name='orders'),
        path('Store_Orders', vendors.OrdersList1, name='Store_orders'),
        path('vendor_email_verify', vendors.vendor_email_verify, name='vendor_email_verify'),
        path('callback/', vendors.callback, name='callback'),
        path('delete_interest', vendors.delete_interest, name='delete_interest'),
        path('upload_products', vendors.upload_products, name='upload_products'),
       

        


        
    ], 'bid'), namespace='vendors')),
    path('customers/', include(([
        # ADD URL HERE FOR OTP VERIFICATION
        # ==================================
        
        path('', customers.profile, name='customer_profile'),
       
        path('customer_details', customers.customer_details, name='customer_details'),
        path('view_profile', customers.view_profile, name='view_profile'),
        path('customer_requirement/', customers.customer_requirement, name='customer_requirement'),
        path('PastRequirents/', customers.View_requirement, name='View_requirement'),
        path('PastRequirents/<int:pk>/', customers.requirement_detail, name='requirement_detail'),
        path('PastRequirents/<int:id>/TopBids', customers.TopBids, name='topbids'),
        path('OrderConfirmation/<int:pk>/', customers.OrderConfirmation, name='orderconfirmationpage'),
        path('CompleteOrder/<int:pk>', customers.CompleteOrder, name='completeorder'),
        path('Orders', customers.OrdersList, name='orders'),
        path('customer_email_verify', customers.customer_email_verify, name='customer_email_verify'),
        path('payment/<int:id>', customers.Payment, name='customerpayment'),
        path('callback/', customers.callback, name='callback'),
        path('PaymentSuccess/', customers.PaymentSuccess, name='PaymentSuccess'),
        path('PaymentFailure/', customers.PaymentFailure, name='PaymentFailure'),
        

        


    ], 'bid'), namespace='customers')),
    
    

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)