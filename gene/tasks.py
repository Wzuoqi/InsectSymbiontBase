from celery import shared_task

@shared_task
def index_gene_chunk(start, end):
    docs = []
    genes = Gene.objects.all()[start:end]
    for gene in genes:
        try:
            doc = {
                '_index': 'genes',
                '_id': gene.id,
                '_source': GeneDocument.prepare(GeneDocument(), gene)
            }
            docs.append(doc)
        except Exception as e:
            logger.error(f"Error processing gene {gene.id}: {str(e)}")

    if docs:
        bulk(connections.get_connection(), docs)
    return len(docs)