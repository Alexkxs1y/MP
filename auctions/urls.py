from django.urls import path

from . import views

# ofr redirecting if unsigned
from django.contrib.auth import views as auth_views

#app_name = 'auctions'

urlpatterns = [ 
    path("", views.index, name="index"),
    path("create_listing", views.create_listing, name="create_listing"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),    
    path("<int:entryid>", views.entry, name="entry"),
    path("closed/<int:entryid>", views.entry_closed, name="entry_closed"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category_listings/<int:categoryid>", views.category_listings, name="category_listings"),
    path('conversations/', views.conversations, name='conversations'),
    path('conversation/<int:conversation_id>/', views.conversation, name='conversation'),
    path('send_message/<int:conversation_id>/', views.send_message, name='send_message'),
    path("chat/list", views.chat_list_view, name="chat_list"),
    path("chat/detail/<int:conversation_id>", views.chat_detail_view, name="chat_detail"),
]

