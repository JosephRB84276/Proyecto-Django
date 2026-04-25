# config/context_processors.py
def navbar_context(request):
    return {
        'user_authenticated': request.user.is_authenticated,
        'user_name': request.user.nombres if request.user.is_authenticated else '',
    }