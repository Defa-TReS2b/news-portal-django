from django.urls import path, include
from .views import PostsList, PostDetail, SearchList, PostCreate, PostUpdate, PostDelete, SubscriberView

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchList.as_view()),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='product_delete'),
    path('subscribe/', SubscriberView.as_view(), name='subscribe'),
]