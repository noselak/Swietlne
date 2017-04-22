from .forms import LoginForm

def login_form(request):
    form = LoginForm()
    return {
        'form': form,
    }