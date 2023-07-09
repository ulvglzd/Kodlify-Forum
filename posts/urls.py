from django.urls import path
from .views import post_answer_view, up_unup_post, PostDelete, PostUpdate

app_name = 'posts'

urlpatterns = [
    path('', post_answer_view, name='post-view'),
    path('uped/', up_unup_post, name='up-post-view'),
    path('<pk>/delete/', PostDelete.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdate.as_view(), name='post-update'),
]