"""
URL configuration for codesphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from store import views

from django .conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/',views.SignUpView.as_view(),name="sign-up"),
    path("login/",views.SignInView.as_view(),name="sign-in"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("logout/",views.LogOutView.as_view(),name="log-out"),
    path("profile/change",views.UserProfileEditView.as_view(),name="profile-edit"),
    path("project/add",views.ProjectAddView.as_view(),name="add"),
    path("myworks/all/",views.MyProjectListView.as_view(),name="myworks-all"),
    path("project/<int:pk>/update/",views.MyprojectUpdateView.as_view(),name="project-update"),
    path("project/<int:pk>/detail/",views.ProjectDetailView.as_view(),name="project-detail"),
    path("project/<int:pk>/add-to-wishlist",views.AddToWishListView.as_view(),name="wish-list"),
    path("wishlist/all/",views.WishListView.as_view(),name="add-to-wish"),
    path("wishlist-delete/<int:pk>/remove/",views.WishListItemDeleteView.as_view(),name="wishlist-delete"),

    path("check/out/",views.CheckOutView.as_view(),name="check-out"),

    path("verify/",views.PaymentVerificationView.as_view(),name="verify"),

    path("orders/all/",views.MyOrdersView.as_view(),name="orders"),

    path("password/reset",views.PasswordResetView.as_view(),name="reset"),

    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 