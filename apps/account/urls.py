from django.urls import path
from .views import Register, Login, Logout, \
    AccountEdit, AccountProfilePhotoUpdate, AccountDetailUpdate, \
    ActivateView, AccountVerify

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path('logout/', Logout.as_view(), name='logout'),
    path("edit", AccountEdit.as_view(), name="account.edit"),
    path("profilephoto/update", AccountProfilePhotoUpdate.as_view(), name="account.profilephoto.update"),
    path("update", AccountDetailUpdate.as_view(), name="account.update"),
    path("verify/<str:email>", AccountVerify.as_view(), name="account.verify"),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='account.activate'),
]
