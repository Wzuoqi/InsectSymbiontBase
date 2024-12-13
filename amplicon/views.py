from django.shortcuts import render, get_object_or_404
from .models import Amplicon
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def amplicons(request):
    # Get all Amplicon objects
    amplicons_list = Amplicon.objects.all()

    # Handle quick filter
    filter_type = request.GET.get('filter', 'all')
    if filter_type == '16s':
        amplicons_list = amplicons_list.filter(classification='16S')
    elif filter_type == 'others':
        amplicons_list = amplicons_list.exclude(classification='16S')

    # Define search fields
    search_fields = ['run', 'assay_type', 'biosample', 'center_name', 'instrument', 'library_layout', 'bioproject', 'classification', 'geo_loc_name_country', 'geo_loc_name_country_continent', 'geo_loc_name', 'host', 'env_broad_scale', 'env_local_scale', 'env_medium', 'host_sex']

    # Handle advanced search
    query = Q()
    for field in search_fields:
        value = request.GET.get(field)
        if value:
            query &= Q(**{f"{field}__icontains": value})

    # Handle basic search
    search_query = request.GET.get('search', '')
    if search_query:
        basic_query = Q()
        for field in search_fields:
            basic_query |= Q(**{f"{field}__icontains": search_query})
        query &= basic_query

    amplicons_list = amplicons_list.filter(query)

    # Handle sorting
    sort_by = request.GET.get('sort_by', 'run')
    if sort_by not in ['run', 'host', 'geo_loc_name_country', 'collection_date']:
        sort_by = 'run'
    amplicons_list = amplicons_list.order_by(sort_by)

    # Pagination
    paginator = Paginator(amplicons_list, 20)  # Show 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'search_query': search_query,
        'filter_type': filter_type,
    }

    return render(request, "amplicons.html", context)

def amplicon_detail(request, amplicon_id):
    amplicon = get_object_or_404(Amplicon, id=amplicon_id)
    context = {
        'amplicon': amplicon,
    }
    return render(request, 'amplicon_detail.html', context)
