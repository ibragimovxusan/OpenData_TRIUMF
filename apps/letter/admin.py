from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from import_export.admin import ImportExportModelAdmin
from apps.letter.models import Letter, Reason, Counter
from apps.organization.models import Courier
from .resorce import LetterRecoreces
from django.contrib import admin
# from api.bot.bot import msg, load_data


class ParentNullListFilter(admin.SimpleListFilter):
    title = 'Parents'
    parameter_name = 'parent__isnull'

    def lookups(self, request, model_admin):
        return (
            ('null', 'Has no parent'),
            ('not_null', 'Has parent'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'null':
            return queryset.filter(parent__isnull=True)
        elif self.value() == 'not_null':
            return queryset.filter(parent__isnull=False)


def attach_letter(modeladmin, request, queryset):
    # courier_id = request.POST.get('courier_dropdown')

    for letter in queryset:
        letter.status = 'process'
        letter.courier = Courier.objects.get(id=29)
        letter.save()


attach_letter.short_description = 'Attach selected letters to courier'


def archived_cancel_letters(modeladmin, request, queryset):
    for letter in queryset:
        letter.status = 'archived'
        letter.save()


archived_cancel_letters.short_description = 'Archived selected cancel letters'


def archived_finish_letters(modeladmin, request, queryset):
    for letter in queryset:
        letter.status = 'archived'
        letter.is_delivered = True
        letter.save()


archived_finish_letters.short_description = 'Archived selected finish letters'


def return_new_letters(modeladmin, request, queryset):
    for letter in queryset:
        letter.courier = None
        letter.status = 'new'
        letter.save()


def return_finish_letters(modeladmin, request, queryset):
    for letter in queryset:
        letter.status = 'finish'
        letter.reason = None
        letter.save()


return_finish_letters.short_description = 'Return selected finish letters'


def return_cencel_letters(modeladmin, request, queryset):
    for letter in queryset:
        letter.status = 'cancel'
        letter.save()


return_cencel_letters.short_description = 'Return selected cancel letters'


def send_archive_letters_to_channel(modeladmin, request, queryset):
    file_path = "media/archived/letters.xlsx"
    print(file_path, "======================file_path")
    # load_data(file_path)
    # coro = msg(file_path)
    # asyncio.run(coro)
    # os.remove(file_path)


return_new_letters.short_description = 'Return selected new letters'
send_archive_letters_to_channel.short_description = 'send_archive_letters_to_channel'


class LetterAdmin(DraggableMPTTAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    actions = [archived_finish_letters, archived_cancel_letters, attach_letter, return_new_letters,
               return_cencel_letters, return_finish_letters, send_archive_letters_to_channel]
    resource_classes = [LetterRecoreces]
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'courier', 'address', 'status', 'upload_file', 'reason', 'id')
    list_filter = ('status', ParentNullListFilter, 'updated_at', 'created_at', 'is_delivered')
    search_fields = ('personal_id', 'name', 'receiver_name', 'address', 'id', 'courier__full_name', 'reason__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('name', 'address', 'upload_file', 'parent', 'created_at', 'updated_at', 'personal_id')
    list_editable = ('status', 'courier', 'reason')  # Allow editing status directly from the list view
    list_per_page = 500

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'courier':
            kwargs['queryset'] = Courier.objects.all()  # Replace 'Courier' with your actual Courier model name
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


fieldsets = (
    (None, {
        'fields': ('name', 'receiver_name', 'address')
    }),
    ('Files', {
        'fields': ('image', 'pdf_file')
    }),
    ('Details', {
        'fields': ('description', 'status')
    }),
    ('Hierarchy', {
        'fields': ('parent',)
    }),
    ('Relations', {
        'fields': ('courier', 'upload_file', 'reason')
    }),
    ('Other', {
        'fields': ('is_delivered',)
    }),
    ('Timestamps', {
        'fields': ('created_at', 'updated_at'),
        'classes': ('collapse',),
    }),
)


def get_readonly_fields(self, request, obj=None):
    readonly_fields = self.readonly_fields
    if obj:  # If editing an existing object
        readonly_fields += ('created_at',)
    return readonly_fields


class ReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


admin.site.register(Letter, LetterAdmin)
admin.site.register(Reason, ReasonAdmin)
admin.site.register(Counter)
