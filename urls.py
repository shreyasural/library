from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("qr/<str:book_id>/", views.generate_qr, name="generate_qr"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_user, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_user, name="logout"),

    path("add/", views.add_book, name="add"),
    path("search/", views.search_book, name="search"),
    path("delete/", views.delete_book, name="delete"),
    path("issue/", views.issue_book, name="issue"),
    path("return/", views.return_book, name="return"),
    path("viewbooks/", views.viewbooks, name="viewbooks"),
    path("fine/", views.fine_calculator, name="fine"),
    path("recommend/", views.recommend_books, name="recommend"),
    path('popular/', views.popular_books, name='popular_books'),
    path('trending/', views.trending_categories, name='trending_categories'),
]