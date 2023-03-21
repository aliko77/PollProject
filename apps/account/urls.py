from django.urls import path
from .views import Register, Login, Logout, AccountEdit, AccountProfilePhotoUpdate, AccountDetailUpdate

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path('logout/', Logout.as_view(), name='logout'),
    path("edit", AccountEdit.as_view(), name="account.edit"),
    path("profilephoto/update", AccountProfilePhotoUpdate.as_view(), name="account.profilephoto.update"),
    path("update", AccountDetailUpdate.as_view(), name="account.update")
]
