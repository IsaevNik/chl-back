from django.contrib import admin

from .models.support import Support
from .models.company import Company 
from .models.user_group import UserGroup 


admin.site.register(Company)
admin.site.register(Support)
admin.site.register(UserGroup)
