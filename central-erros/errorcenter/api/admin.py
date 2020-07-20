from django.contrib import admin
from .models import Environment, Origin, Level, Log

admin.site.register(Environment)
admin.site.register(Origin)
admin.site.register(Level)
admin.site.register(Log)
