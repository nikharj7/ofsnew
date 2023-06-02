from django.contrib import admin
from bid.models import preorder, Banner, vendor_products_file,  User,Brands,Category,Product,Order_From_Order4Sure,customer_Detail,Contact_Us,Completed_Order,vendor_Detail,Customer_Requirement,Vendor_brands,Vendor_category,Bid, Order

from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)





# Register your models here.
# from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_vendor', 'is_customer', 'email_verified')
    search_fields = ('email', 'is_vendor', 'is_customer', 'email_verified')

admin.site.register(User, UserAdmin)

admin.site.register(preorder)



class BrandAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Brands, BrandAdmin)

admin.site.register(Banner)




class CategoryAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)
admin.site.register(customer_Detail)
admin.site.register(vendor_Detail)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('Email','Name','Subject','Message')
admin.site.register(Contact_Us, ContactAdmin)

class CustomerRequirementAdmin(admin.ModelAdmin):
    list_display = ('customer','name', 'category', 'brand', 'quantity', 'start_price', 'requirement_status','PaymentStatus' )
    search_fields = ('customer','name', 'category', 'brand', 'quantity', 'start_price', 'requirement_status','payment_id', 'provider_order_id', 'signature_id' )
admin.site.register(Customer_Requirement, CustomerRequirementAdmin)
admin.site.register(Vendor_brands)
admin.site.register(Vendor_category)

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ("Vendor","name", "price",  'mrp', 'quantity', 'step_up_quantity', 'category', 'Brand', 'Length', 'Height', 'Width', 'Weight', 'SKU', 'slug')
admin.site.register(Product, ProductAdmin)


class BidAdmin(admin.ModelAdmin):
    list_display = ("Bid_id","customer_id", "vendor_id",  'bid_rate', 'mrp', 'expected_delivery', 'product_expiry', 'supply_pincode', 'PaymentStatus')
    search_fields = ("Bid_id","customer_id", "vendor_id",  'bid_rate', 'mrp', 'expected_delivery', 'product_expiry', 'supply_pincode')

admin.site.register(Bid, BidAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('bid_id', 'customer_id', 'vendor_id', 'customer_payment_status', 'customer_name', 'delivery_contact','delivery_address', )
    search_fields = ('bid_id', 'customer_id', 'vendor_id', 'name', 'quantity', 'order_amount', 'customer_payment_status',  'delivery_address', 'pincode')
admin.site.register(Order, OrderAdmin )



class Completed_OrderAdmin(admin.ModelAdmin):
    list_display = ('bid_id', 'customer_id', 'vendor_id', 'name', 'quantity', 'order_amount', 'customer_payment_status', 'vendor_payment_status', 'delivery_address', 'pincode')
    search_fields = ('bid_id', 'customer_id', 'vendor_id', 'name', 'quantity', 'order_amount', 'customer_payment_status', 'vendor_payment_status', 'delivery_address', 'pincode')
admin.site.register(Completed_Order, Completed_OrderAdmin )

class Order_From_Order4SureAdmin(admin.ModelAdmin):
    list_display = ( 'customer_id', 'vendor_id', 'customer_payment_status', 'customer_name', 'delivery_contact','delivery_address', )
    search_fields = ('customer_id', 'vendor_id', 'name', 'quantity', 'order_amount', 'customer_payment_status',  'delivery_address', 'pincode')

admin.site.register(Order_From_Order4Sure, Order_From_Order4SureAdmin)



admin.site.register(vendor_products_file)