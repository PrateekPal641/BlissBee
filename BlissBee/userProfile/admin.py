from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Feeling)
admin.site.register(Material)
admin.site.register(Activity)
admin.site.register(ScenarioFeedback)
admin.site.register(Article)