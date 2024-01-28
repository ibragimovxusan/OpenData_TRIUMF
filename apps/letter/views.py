from django.db.models import Q
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from apps.letter.models import Letter
from apps.organization.models import Organization, UploadLetterPDF


def root(request):
    search = request.GET.get('search')
    organization = get_object_or_404(Organization, user=request.user.id)
    districts = Letter.objects.filter(parent__isnull=True)
    letters = Letter.objects.filter(Q(parent__isnull=False) & Q(upload_zip_file__organization_id=organization.id) &
                                    Q(Q(status='new') | Q(status='finish') | Q(status='process') | Q(status='cancel')))

    if search:
        letters = letters.filter(Q(name__icontains=search) | Q(address__icontains=search) & Q(
            upload_zip_file__organization_id=organization.id))

    context = {
        'organization': organization,
        'districts': districts,
        'letters': letters,
    }

    return render(request, 'dashboard/index.html', context)


def archive(request):
    search = request.GET.get('search')
    organization = get_object_or_404(Organization, user=request.user.id)
    archives = Letter.objects.filter(Q(parent__isnull=False) & Q(upload_zip_file__organization_id=organization.id) &
                                     Q(status='archived'))

    if search:
        archives = archives.filter(Q(name__icontains=search) | Q(address__icontains=search))

    context = {
        'organization': organization,
        'letters': archives
    }

    return render(request, 'dashboard/archive.html', context)


def add_letter(request):
    districts = Letter.objects.filter(parent__isnull=True)
    organization = get_object_or_404(Organization, user=request.user.id)
    if request.method == 'POST':
        name_list = request.POST.getlist('name')
        parent_list = request.POST.getlist('parent')
        address_list = request.POST.getlist('address')
        pdf_file_list = request.FILES.getlist('pdf_file')
        # phone_number_list = request.POST.getlist('phone_number')
        # receiver_name_list = request.POST.getlist('receiver_name')

        now = datetime.now().replace(microsecond=0)
        previous_day = now - timedelta(days=1)

        target_time = now.replace(hour=14, minute=0, second=0, microsecond=0)
        old_target_time = previous_day.replace(hour=14, minute=0, second=0, microsecond=0)

        upload_pdf_letter = UploadLetterPDF.objects.filter(organization=organization,
                                                           name__exact=f"{datetime.now().date()}",
                                                           created_at__lte=old_target_time,
                                                           created_at__gte=target_time).first()

        if not upload_pdf_letter:
            upload_pdf_letter = UploadLetterPDF.objects.create(organization=organization, status='process',
                                                               name=f"{datetime.now().date()}")
        elif now > target_time:
            upload_pdf_letter = UploadLetterPDF.objects.create(organization=organization, status='process',
                                                               name=f"{datetime.now().date()} (1)")
        else:
            upload_pdf_letter = UploadLetterPDF.objects.filter(organization=organization,
                                                               name__exact=f"{datetime.now().date()}",
                                                               created_at__lte=old_target_time,
                                                               created_at__gte=target_time).first()

        for name, parent_id, address, pdf_file in zip(
                name_list, parent_list, address_list, pdf_file_list
        ):
            # Retrieve the parent Letter instance
            parent_instance = get_object_or_404(Letter, id=parent_id)

            # Create the new Letter instance
            letter = Letter.objects.create(
                name=name,
                parent=parent_instance,
                address=address,
                pdf_file=pdf_file,
                upload_zip_file=upload_pdf_letter
            )

    return render(request, 'dashboard/detail.html',
                  {'districts': districts, 'organization': organization})
