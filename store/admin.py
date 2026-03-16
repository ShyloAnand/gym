from django.contrib import admin
from .models import Product,Fit
from .models import DietUser, DietPlan

admin.site.register(Product)

admin.site.register(Fit)

admin.site.register(DietUser)
admin.site.register(DietPlan)


