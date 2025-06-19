# products/context_processors.py

from .models import Category

def categories_menu(request):
    """
    Adiciona as categorias principais para o menu de navegação.
    """
    # Busca apenas categorias de nível superior (sem pai) para o menu principal
    # Ou ajuste para buscar todas e construir a hierarquia no template se preferir
    categories = Category.objects.filter(parent__isnull=True).order_by('name')
    return {'categories': categories}