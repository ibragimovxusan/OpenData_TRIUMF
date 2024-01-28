import datetime
from datetime import timedelta
from io import BytesIO
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from PyPDF4 import PdfFileMerger
from apps.account.models import User
from django.core.exceptions import ValidationError


class Adele(models.Model):
    name = models.CharField(max_length=225, null=True)
    excel_file = models.FileField(null=True, blank=True, upload_to='adele/Excel/')
    pdf_file = models.FileField(null=True, blank=True, upload_to='adele/PDF/')

    def __str__(self):
        if self.name:
            return f'{self.name}'
        return f"{self.id}"


class Organization(models.Model):
    inn = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    icon = models.FileField(upload_to='Organization', null=True, blank=True)
    district = models.CharField(max_length=223, null=True)
    price = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    adeles = models.ManyToManyField(Adele, related_name='organization', blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'


class InComeOrganization(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    this_month = models.BooleanField(default=False)
    total_letter = models.PositiveIntegerField(null=True, blank=True)
    delivered = models.PositiveIntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    upload_file = models.ForeignKey(
        'UpLoadLetterExcel',
        on_delete=models.CASCADE,
        null=True,
        related_name='incomesorgannization',
        blank=True
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='incomes',
        null=True, blank=True
    )
    this_month = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


STATUS = (
    ('process', 'Process'),
    ('failed', 'Failed'),
    ('finished', 'Finished'),
)


class UpLoadLetterExcel(models.Model):

    def validate_even_number(instance):
        get_file_type = str(instance).split('.')[-1]
        if get_file_type not in ['pdf', 'xls', 'xlsx']:
            raise ValidationError('Ruhsat berilmagan file yuklayabsiz')

    name = models.CharField(max_length=255, null=True)
    count = models.PositiveIntegerField(null=True, blank=True)
    excel_file = models.FileField(null=True, blank=True, upload_to='UpLoadLetterExcel',
                                  validators=[validate_even_number])
    pdf_file = models.FileField(null=True, blank=True, upload_to='UploadLetterPDF', validators=[validate_even_number])
    response = models.FileField(null=True, blank=True, upload_to="UpLoadLetterExcelResponse",
                                validators=[validate_even_number])
    status = models.CharField(choices=STATUS, max_length=100, default='process')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        related_name='uploadexcels',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.organization.name}'


class UploadLetterPDF(models.Model):
    def validate_even_number(instance):
        get_file_type = str(instance).split('.')[-1]
        if get_file_type not in ['zip', 'pdf', 'xls', 'xlsx']:
            raise ValidationError('Ruhsat berilmagan file yuklayabsiz')

    name = models.CharField(max_length=255, null=True)
    count = models.PositiveIntegerField(null=True, blank=True)
    zip_file = models.FileField(null=True, blank=True, upload_to="UploadLetterPDFResponse",
                                validators=[validate_even_number])
    pdf_file = models.FileField(null=True, blank=True, upload_to='UploadLetterPDF', validators=[validate_even_number])
    status = models.CharField(choices=STATUS, max_length=10, default='process')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='upload_zip_files',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def letter_count(self):
        return self.zip_letters.all().count()

    @property
    def daily_pdf(self):
        now = datetime.datetime.now()
        previous_day = now - timedelta(days=1)
        target_time = now.replace(hour=14, minute=0, second=0, microsecond=0)
        old_time = previous_day.replace(hour=14, minute=0, second=0, microsecond=0)

        pdf_buffer = PdfFileMerger()

        pdf_letters = []
        if now == target_time:
            upload_letters = UploadLetterPDF.objects.filter(
                Q(created_at__lte=old_time) & Q(created_at__gte=target_time) | Q(created_at=now.date()))
            if upload_letters:
                for pdf_letter in upload_letters:
                    for letter in pdf_letter.zip_letters.all():
                        pdf_letters.append(letter.pdf_file.url)

                    self.pdf_file = pdf_buffer.merge(pdf_letters)
                    self.status = 'finished'
                    self.save()
                    return "Success"
            else:
                self.status = 'failed'
                self.save()
                return "Fail"


class UploadSingleLetter(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    pdf_file = models.FileField(null=True, blank=True, upload_to='UploadSingleLetter')
    pay_by_check = models.FileField(null=True, blank=True, upload_to='Checks')
    person = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class UploadError(models.Model):
    log = models.TextField(null=True, blank=True)
    uploadexcel = models.ForeignKey(
        UpLoadLetterExcel,
        on_delete=models.CASCADE,
        related_name='uploaderrors',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Courier(models.Model):
    AUTO_TYPE = (
        ('piyoda', 'Piyoda'),
        ('velosipet', 'Velosipet'),
        ('mashina', 'Mashina'),
    )
    full_name = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.FileField(upload_to='Courier', null=True, blank=True)
    jshr = models.PositiveIntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    language = models.CharField(null=True, blank=True, default='uz', max_length=100)
    auto_type = models.CharField(choices=AUTO_TYPE, max_length=100, default='piyoda')
    phone = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='courier',
        null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.full_name


class InComeCourier(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    total_letter = models.PositiveIntegerField(null=True, blank=True)
    delivered = models.PositiveIntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    upload_file = models.ForeignKey(
        UpLoadLetterExcel,
        on_delete=models.CASCADE,
        related_name='incomescourier',
        null=True, blank=True
    )
    courier = models.ForeignKey(
        Courier,
        related_name='incomes',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    this_month = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Partner(models.Model):
    partner_name = models.CharField(max_length=225, null=True, blank=True)
    logo = models.ImageField(upload_to="partners_logo/")

    def __str__(self):
        return self.partner_name
