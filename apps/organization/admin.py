from datetime import timezone, datetime, timedelta
from PyPDF4 import PdfFileMerger
from django.contrib import admin
from apps.organization.models import Organization, Courier, InComeOrganization, InComeCourier, UpLoadLetterExcel, Adele, \
    Partner, UploadLetterPDF


class OrganizationAdmin(admin.ModelAdmin):
    filter_horizontal = ('adeles',)
    list_display = ('id', 'name', 'inn', 'price', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('created_at', 'is_active')
    list_per_page = 30


class UpLoadLetterExcelAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'count', 'excel_file', 'pdf_file', 'organization', 'created_at', 'id')
    list_filter = ('status', 'created_at', 'organization')
    list_per_page = 30
    # fieldsets = (
    #     ('Основные данные', {
    #         'fields': ('name', 'excel_file', 'pdf_file', 'organization')
    #     }),
    #     ('Дополнительные данные', {
    #         'fields': ('created_at',)
    #     }),
    # )


def generate_pdfs(modeladmin, request, queryset):
    now = datetime.now()
    previous_day = now - timedelta(days=1)
    target_time = now.replace(hour=14, minute=0, second=0, microsecond=0)
    old_time = previous_day.replace(hour=14, minute=0, second=0, microsecond=0)
    uploaded_letters = UploadLetterPDF.objects.filter(created_at__lte=old_time, created_at__gte=target_time)

    pdf_buffer = PdfFileMerger()

    letters = []

    if uploaded_letters:
        for uploaded_letter in uploaded_letters:
            for letter in uploaded_letter.zip_letters.all():
                pdf_buffer.append(open(letter.pdf_file.url, 'rb'))

            url = pdf_buffer.write(f'media/UploadLetterPDF/{uploaded_letter.id}')
            uploaded_letter.pdf_file = url
            uploaded_letter.status = 'finished'
            uploaded_letter.save()


generate_pdfs.short_description = 'PDF generatsiya qilish'


class UploadLetterPDFAdmin(admin.ModelAdmin):
    actions = [generate_pdfs]
    list_display = ('name', 'status', 'letter_count', 'zip_file', 'pdf_file', 'organization', 'created_at', 'id')
    list_filter = ('status', 'created_at', 'organization')
    list_per_page = 30


class InComeOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_paid', 'price', 'total_letter', 'delivered', 'id')
    list_filter = ('created_at',)
    list_per_page = 30


class CourierAdmin(admin.ModelAdmin):
    list_display = ('phone', 'full_name', 'jshr', 'price', 'auto_type', 'is_active', 'id')
    list_filter = ('created_at', 'is_active')
    list_per_page = 30


class InComeCourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_paid', 'price', 'total_letter', 'delivered', 'courier', 'id')
    list_filter = ('created_at',)
    list_per_page = 30


admin.site.register(Adele)
admin.site.register(InComeOrganization, InComeOrganizationAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Courier, CourierAdmin)
admin.site.register(InComeCourier)
admin.site.register(UpLoadLetterExcel, UpLoadLetterExcelAdmin)
admin.site.register(UploadLetterPDF, UploadLetterPDFAdmin)
admin.site.register(Partner)
