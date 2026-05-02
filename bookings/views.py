from django.http import Http404
from django.shortcuts import render

from .forms import BookingRequestForm
from .models import BookingRequest, Experience


def index(request):
    experiences = Experience.objects.filter(is_published=True).select_related('hut')
    return render(
        request,
        'bookings/index.html',
        {
            'experiences': experiences,
            'experience_count': experiences.count(),
        },
    )


def detail(request, slug):
    try:
        experience = Experience.objects.select_related('hut').get(slug=slug, is_published=True)
    except Experience.DoesNotExist:
        raise Http404('Experience not found')

    return render(
        request,
        'bookings/detail.html',
        {
            'experience': experience,
        },
    )


def request_booking(request, slug):
    try:
        experience = Experience.objects.select_related('hut').get(slug=slug, is_published=True)
    except Experience.DoesNotExist:
        raise Http404('Experience not found')

    submitted = False
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking_request = form.save(commit=False)
            booking_request.experience = experience
            if request.user.is_authenticated:
                booking_request.user = request.user
            booking_request.status = BookingRequest.STATUS_PENDING
            booking_request.save()
            submitted = True
    else:
        form = BookingRequestForm()

    return render(
        request,
        'bookings/request.html',
        {
            'experience': experience,
            'form': form,
            'submitted': submitted,
        },
    )
