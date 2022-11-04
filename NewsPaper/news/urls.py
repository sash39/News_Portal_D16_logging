from django.urls import path
from .views import (
    PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, ArticleCreate
)


urlpatterns = [
   path('', PostsList.as_view(), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   #path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   #path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]