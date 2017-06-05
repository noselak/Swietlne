from django.contrib import admin
from django.http import HttpResponse

from .models import Join, Faq

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"E-Mail"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.email),
        ])
    return response
export_csv.short_description = u"Export CSV"


class JoinAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    actions = [export_csv]
    
    class Meta:
        model = Join


admin.site.register(Join, JoinAdmin)
admin.site.register(Faq)
