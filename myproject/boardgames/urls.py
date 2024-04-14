from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# from views import board_games_list

app_name = 'boardgames'
urlpatterns = [
    path('', views.board_games_list, name='home'),
    # path('boardgames/', include('boardgames.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('index', views.board_games_list, name='index'),
    path('boardgame/<int:pk>/', views.detail, name='boardgame_detail'),
    path('signup/', views.signup, name='signup'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('library/', views.library, name='library'),
    path('boardgame/<int:pk>/add-to-library/', views.add_to_library, name='add_to_library'),
    path('boardgame/<int:pk>/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('login/', views.login_view, name='login'),
    path('boardgame/<int:pk>/add-to-library/', views.add_to_library, name='add_to_library'),
    path('search/', views.search, name='search'),
    path('<int:pk>/recommendations/', views.recommendations, name='recommendations'),
    path('<int:game_id>/remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('<int:game_id>/add_review/', views.add_review, name='add_review'),
    path('<int:game_id>/join_community/', views.join_community, name='join_community'),
    path('<int:pk>/', views.detail, name='detail'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('clubs/', views.club_list, name='club_list'),
    # path('recommendations/', views.recommendations_user, name='recommendations_user'),
    path('recommendations/<int:user_id>/', views.recommendations_user, name='recommendations_user'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneCustomView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmCustomView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', views.PasswordResetCompleteCustomView.as_view(), name='password_reset_complete'),
    path('<int:game_id>/add_review/', views.add_review, name='add_review'),
    path('<int:game_id>/join_community/', views.join_community, name='join_community'),
    path('join-club/', views.join_club, name='join_club'),
    # path('user-profile/', views.user_profile, name='user_profile'),
    path('user-profile/<int:user_id>/', views.user_profile, name='user_profile'),

]
