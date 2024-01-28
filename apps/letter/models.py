from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from apps.account.models import BaseAbstractDate
from apps.organization.models import UpLoadLetterExcel, Courier, Organization, UploadLetterPDF


class Letter(MPTTModel):
    STATUS = (
        ('process', 'Process'),
        ('cancel', 'Cancel'),
        ('finish', 'Finish'),
        ('new', 'New'),
        ('archived', 'Archived')
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    receiver_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    personal_id = models.BigIntegerField(null=True, blank=True)
    image = models.FileField(upload_to='Letter', null=True, blank=True)
    pdf_file = models.FileField(upload_to='Letter', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, default='new')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )
    courier = models.ForeignKey(
        Courier,
        on_delete=models.CASCADE,
        related_name='attached',
        null=True, blank=True
    )
    upload_file = models.ForeignKey(
        UpLoadLetterExcel,
        on_delete=models.CASCADE,
        related_name='letters',
        null=True, blank=True
    )
    upload_zip_file = models.ForeignKey(
        UploadLetterPDF,
        on_delete=models.CASCADE,
        related_name='zip_letters',
        null=True, blank=True
    )
    reason = models.ForeignKey(
        'Reason',
        on_delete=models.CASCADE,
        related_name='letters',
        null=True, blank=True
    )
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            return self.name
        return "Letter"

    class MPTTMeta:
        order_insertion_by = ['name']


class Reason(BaseAbstractDate):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Counter(BaseAbstractDate):
    letter_counter = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.letter_counter}"
