from core import models
from core.models import ScheduleTime, Schedule
from django.contrib import admin

# Register your models here.
admin.site.register(models.Appointment)  # TODO: disable


# admin.site.register(models.Schedule)
# admin.site.register(models.ScheduleTime)


class ScheduleTimeInline(admin.StackedInline):
	model = ScheduleTime


class ScheduleAdmin(admin.ModelAdmin):
	fields = ['dia', 'medico']
	inlines = [ScheduleTimeInline]
	list_display = ('dia', 'medico_nome', 'horarios')
	ordering = ['dia', 'medico']

	@admin.display(ordering='medico')
	def medico_nome(self, obj):
		return obj.medico.nome

	@admin.display()
	def horarios(self, obj: Schedule):
		return ', '.join((str(h.horario) for h in obj.horarios.all()))

class MedicAdmin(admin.ModelAdmin):
	list_display = ('nome',)

class SpecialtyAdmin(admin.ModelAdmin):
	list_display = ('nome',)

admin.site.register(models.Schedule, ScheduleAdmin)
admin.site.register(models.Medic, MedicAdmin)
admin.site.register(models.Specialty, SpecialtyAdmin)
