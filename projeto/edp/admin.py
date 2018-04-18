from django.contrib import admin
from .models import Edp, Habilidade

# Register your models here.
admin.autodiscover()

admin.site.register(Edp)
admin.site.register(Habilidade)