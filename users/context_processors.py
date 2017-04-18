from .forms import LoginForm

def login_form(request):
    form = LoginForm(request.POST or None)
    return {
        'form': form,
    }