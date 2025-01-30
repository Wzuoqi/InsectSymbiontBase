from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Gene

def genes(request):
    # Get all search parameters
    query = request.GET.get('query', '').strip()
    source_id = request.GET.get('source_id', '').strip()
    nr_id = request.GET.get('nr_id', '').strip()
    nr_annotation = request.GET.get('nr_annotation', '').strip()
    host = request.GET.get('host', '').strip()
    go_terms = request.GET.get('go_terms', '').strip()
    kegg_ko = request.GET.get('kegg_ko', '').strip()
    kegg_pathway = request.GET.get('kegg_pathway', '').strip()
    pfams = request.GET.get('pfams', '').strip()

    genes_query = Gene.objects.all()

    # Basic search - case insensitive
    if query:
        genes_query = genes_query.filter(
            Q(nr_annotation__icontains=query) |  # icontains for case-insensitive partial match
            Q(description__icontains=query) |
            Q(preferred_name__icontains=query)
        )

    # Advanced search filters - all case insensitive
    if source_id:
        # For IDs, we might want to use iexact for exact match (but still case insensitive)
        genes_query = genes_query.filter(source_id__iexact=source_id)
    if nr_id:
        genes_query = genes_query.filter(nr_id__iexact=nr_id)
    if nr_annotation:
        genes_query = genes_query.filter(nr_annotation__icontains=nr_annotation)
    if host:
        genes_query = genes_query.filter(host__icontains=host)
    if go_terms:
        # GO terms are usually uppercase but we'll make it case insensitive
        genes_query = genes_query.filter(go_terms__icontains=go_terms)
    if kegg_ko:
        # KEGG KO IDs are usually uppercase but we'll make it case insensitive
        genes_query = genes_query.filter(kegg_ko__icontains=kegg_ko)
    if kegg_pathway:
        genes_query = genes_query.filter(kegg_pathway__icontains=kegg_pathway)
    if pfams:
        # Pfam IDs are usually uppercase but we'll make it case insensitive
        genes_query = genes_query.filter(pfams__icontains=pfams)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(genes_query, 20)  # Show 20 genes per page
    genes_page = paginator.get_page(page)

    context = {
        'genes': genes_page,
        'query': query,
        'source_id': source_id,
        'nr_id': nr_id,
        'nr_annotation': nr_annotation,
        'host': host,
        'go_terms': go_terms,
        'kegg_ko': kegg_ko,
        'kegg_pathway': kegg_pathway,
        'pfams': pfams,
        'total_count': genes_query.count(),
    }

    return render(request, 'gene_catalog.html', context)

def gene_detail(request, source_id, gene_id):
    gene = get_object_or_404(Gene, source_id=source_id, gene_id=gene_id)
    return render(request, 'gene_detail.html', {'gene': gene})
