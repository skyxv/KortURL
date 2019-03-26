from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import LoginForm


class Login(View):
    """
    登录
    """

    def get(self, request):
        return render(request, 'login.html', {"saved_username": self.saved_username(request)})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = HttpResponseRedirect(reverse("index"))
                if self.select_rem(request):
                    return self.set_cookie(response, 'username', username)
                else:
                    return response
            else:
                return render(request, 'login.html', {"error": {"username": ["用户名或密码错误"]},
                                                      "saved_username": self.saved_username(request)})
        else:
            return render(request, 'login.html', {"error": form.errors,
                                                  "saved_username": self.saved_username(request)})

    @staticmethod
    def select_rem(request):
        if "check" in request.POST:
            return True

    @staticmethod
    def set_cookie(response, key, value):
        response.set_cookie(key, value)
        return response

    @staticmethod
    def get_cookie(request, key):
        return request.COOKIES.get(key, None)

    def saved_username(self, request):
        return self.get_cookie(request, 'username')


class Logout(View):

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("logout"))
