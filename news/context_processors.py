from products.models import Category
from .forms import JoinForm

def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}
    
def news_form(request):
    form = JoinForm(request.POST or None)
    return {
        'form': form,
    }
