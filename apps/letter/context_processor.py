from django.shortcuts import get_object_or_404

from apps.organization.models import Organization


def data(request):
    organization = get_object_or_404(Organization, user=request.user)

    return {
        'organization': organization
    }