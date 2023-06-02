from import_export import resources
from bid.models import Brands, Category, Product
from django.conf.global_settings import DATETIME_INPUT_FORMATS
from import_export.fields import Field

class BrandResource(resources.ModelResources):
    class Meta:
        model = Brands

class CategoryResource(resources.ModelResources):
    class Meta:
        model = Category

class ProductResource(resources.ModelResources):
    Vendor = fields.Field(
        column_name='Vendor',
        attribute='Vendor',
        widget=widgets.ForeignKeyWidget(User, 'email'))
    class Meta:
        model = Product
        fields = ('Vendor','image','name','price','category','brand','description','slug','expiry_date','created')
        import_order = fields
        skip_unchanged = False
        report_skipped = True





        