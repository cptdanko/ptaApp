from django.contrib import admin
from pta.models import *
#from django.contrib.auth.models import User
#from django.contrib.auth.admin import UserAdmin

admin.site.register(Patient)
admin.site.register(Staff)
admin.site.register(Question)
admin.site.register(Role)
admin.site.register(PTAQuestionaire)
admin.site.register(Answer)
admin.site.register(Language)
admin.site.register(PatientResponses)
admin.site.register(PictureCard)
admin.site.register(PatientPics)
