from django.contrib import admin
from authentication.models import User



admin.site.site_title = 'Mahney Elbana'       # default: "Django site admin"
admin.site.site_header = 'Mahney'           # default: "Django Administration"
admin.site.index_title = 'Mahney DashBoard'  # default: "Site administration"

class UserAdmin(admin.ModelAdmin):
    
    list_display = ['email', 'username','email_verified' , 'is_staff' ,]
    
    list_filter = ['username', 'email']

    search_fields = ['email']


admin.site.register(User ,UserAdmin)

