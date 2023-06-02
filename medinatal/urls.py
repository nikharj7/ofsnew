from django.urls import include, path
from django.contrib import admin
from bid.views import bid, customers, vendors
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "OrderforSure"
admin.site.site_title = "OrderforSure Admin Panel"
admin.site.index_title = "OrderforSure Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bid.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', bid.SignUpView.as_view(), name='signup'),
    path('accounts/signup/vendor/', vendors.vendorSignUpView.as_view(), name='vendor_signup'),
    path('accounts/signup/customer/', customers.customerSignUpView.as_view(), name='customer_signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)