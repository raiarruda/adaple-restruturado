from django.contrib import admin
from .models import Edp, Habilidade, RecursosEdp, RespostaEdp

# Register your models here.
admin.autodiscover()

admin.site.register(Edp)
admin.site.register(RecursosEdp)
admin.site.register(Habilidade)
admin.site.register(RespostaEdp)

