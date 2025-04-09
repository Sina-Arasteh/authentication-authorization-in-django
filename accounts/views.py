from django.shortcuts import render


def index_page(request):
    """Renders the index page."""
    return render(request, 'accounts/index.html')
