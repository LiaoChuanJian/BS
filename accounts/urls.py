from django.conf.urls import url, include
from .views import *
urlpatterns = [
    url(r"^modify$", modify, name="modify"),
    url(r"^my_info$", my_info, name="my_info"),
    url(r"^login$", user_login, name="login"),
    url(r"^logout$", user_logout, name="logout"),
    url(r"^register$", do_register, name="register"),

]