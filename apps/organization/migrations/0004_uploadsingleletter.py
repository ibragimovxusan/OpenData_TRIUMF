# Generated by Django 4.2.5 on 2023-10-24 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0003_alter_uploadletterexcel_pdf_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadSingleLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='UploadSingleLetter')),
                ('pay_by_check', models.FileField(blank=True, null=True, upload_to='Checks')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
