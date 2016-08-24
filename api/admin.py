from django.contrib import admin

from .models.support import Support
from .models.company import Company 


admin.site.register(Company)
admin.site.register(Support)
