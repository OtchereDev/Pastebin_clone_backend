from api.models import CodeFolder, CodePaste,UserSettings,UserProfile
from django.contrib import admin

admin.site.register(CodePaste)
admin.site.register(CodeFolder)
admin.site.register(UserProfile)
admin.site.register(UserSettings)
