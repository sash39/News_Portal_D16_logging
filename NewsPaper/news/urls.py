from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, ArticleCreate
from news.views import CategoryListView
from .views import subscribe, IndexView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60*5)(PostsList.as_view()), name='news_list'),
    path('<int:pk>', cache_page(60)(PostDetail.as_view()), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('', IndexView.as_view()),


]
