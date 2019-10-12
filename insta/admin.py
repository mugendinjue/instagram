from django.contrib import admin
from .models import Profile,Like,Comment,Image,Follows

admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Follows)
