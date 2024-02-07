from django.contrib import admin

# Register your models here.
from .models import Post, Reply, Profile, Events, Calendar

admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Profile)
admin.site.register(Events)
admin.site.register(Calendar)