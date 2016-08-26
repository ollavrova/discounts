from agreements.models import Agreement, Period, Company
from django.contrib import admin


class PeriodAdmin(admin.ModelAdmin):
    list_display = ['agreement', 'status', 'start_date', 'end_date']
    search_fields = ['agreement', 'status', 'start_date', 'end_date']
    ordering = ('start_date', 'status')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name']
    ordering = ('-name', )

    def search_country(self):
        return


class PeriodInline(admin.TabularInline):
    model = Period
    extra = 1


class AgreementAdmin(admin.ModelAdmin):
    inlines = [
        PeriodInline
    ]
    list_display = ['negotiator', 'company', 'start_date', 'end_date']
    search_fields = ['start_date', 'end_date', 'company__name', 'negotiator__username']
    ordering = ('negotiator', 'company', 'start_date')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Agreement, AgreementAdmin)
