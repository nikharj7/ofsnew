# from dataclasses import fields
# from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
# from django.forms.utils import ValidationError

# from bid.models import (Answer, Question, vendor, vendorAnswer,
#                               Subject, User)
from bid import models
# from bid.views.vendors import vendorInterests              
from .models import Brands, Category, Customer_Requirement, User,  vendor_Detail, Vendor_brands, Vendor_category


class customerSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['email']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True

        if commit:
            user.save()
        return user


class vendorSignUpForm(UserCreationForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=Subject.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['email']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        # vendor = vendor.objects.create(user=user)
        # vendor.interests.add(*self.cleaned_data.get('interests'))
        return user





class VendorInterestsForm(forms.ModelForm):
    
    brand_interests = forms.ModelMultipleChoiceField(
        queryset=Brands.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    category_interests = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    # @transaction.atomic
    # def save(self):
    #     print('done')
    #     brand = Vendor_brands.objects.create(id=self.id)
    #     brand.add(*self.cleaned_data.get('brand_interests'))
    #     category = Vendor_category.objects.create(id=1)
        
    #     category.category_interest.add(*self.cleaned_data.get('category_interests'))
    
class DateInput(forms.DateInput):
    input_type = 'date'
    
    
class Customer_need(forms.ModelForm):
    class Meta:
        model = Customer_Requirement
        fields = ('name', 'category', 'brand','description','start_price','Exp_delivery_days','quantity','delivery_contact','delivery_address','product_ref_no','delivery_pincode')
        widgets = {
            'Exp_delivery_days': forms.DateInput(attrs={'type': 'date'})
        }
        
        

        