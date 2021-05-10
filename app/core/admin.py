from core import models
from core.models import Schedule, ScheduleTime
from django.contrib import admin


class ScheduleTimeInline(admin.StackedInline):
    model = ScheduleTime


class ScheduleAdmin(admin.ModelAdmin):
    fields = ['dia', 'medico']
    inlines = [ScheduleTimeInline]
    list_display = ('dia', 'medico_nome', 'horarios')
    ordering = ['dia', 'medico']
    date_hierarchy = 'dia'

    @admin.display(ordering='medico')
    def medico_nome(self, obj):
        return obj.medico.nome

    @admin.display()
    def horarios(self, obj: Schedule):
        return ', '.join((str(h.horario) for h in obj.horarios.all()))


class MedicAdmin(admin.ModelAdmin):
    name = 'Medico'
    verbose_name = 'Medicos'
    list_display = ('nome',)


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('nome',)


admin.site.register(models.Appointment)
admin.site.register(models.Schedule, ScheduleAdmin)
admin.site.register(models.Medic, MedicAdmin)
admin.site.register(models.Specialty, SpecialtyAdmin)
