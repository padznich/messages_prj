from django.contrib import admin

from models import Message, Comment


admin.site.register([Message, Comment])
