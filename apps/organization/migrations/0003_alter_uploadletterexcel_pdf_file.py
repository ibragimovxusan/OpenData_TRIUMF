# Generated by Django 4.2.5 on 2023-10-24 06:18

import apps.organization.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_uploadletterpdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadletterexcel',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='UploadLetterPDF', validators=[apps.organization.models.UpLoadLetterExcel.validate_even_number]),
        ),
    ]