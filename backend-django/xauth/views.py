from django.shortcuts import render

def password_reset_confirm(request, uid, token):
    return render(
        request,
        'auth/password_reset_confirm.html',
        context={'uid': uid, 'token': token}
    )


def password_reset_confirm_success(request):
    return render(request, 'auth/password_reset_confirm_success.html')