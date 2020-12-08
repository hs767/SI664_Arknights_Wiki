from django.urls import path, reverse_lazy
from . import views

app_name='ops'
urlpatterns = [
    path('', views.OperatorListView.as_view()),
    path('operators', views.OperatorListView.as_view(), name='all'),
    path('operator/<int:pk>', views.OperatorDetailView.as_view(), name='operator_detail'),
    path('operator/create',
        views.OperatorCreateView.as_view(success_url=reverse_lazy('ops:all')), name='operator_create'),
    path('operator/<int:pk>/update',
        views.OperatorUpdateView.as_view(success_url=reverse_lazy('ops:all')), name='operator_update'),
    path('operator/<int:pk>/delete',
        views.OperatorDeleteView.as_view(success_url=reverse_lazy('ops:all')), name='operator_delete'),
    path('operator/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='operator_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ops')), name='operator_comment_delete'),
    path('operator/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='operator_favorite'),
    path('operator/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='operator_unfavorite'),
    #path('operator/<int:pk>/rating',
    #    views.RatingCreateView.as_view(), name='opeartor_rating_create'),
    #path('rating/<int:pk>/delete',
    #    views.RatingDeleteView.as_view(success_url=reverse_lazy('ops')), name='operator_rating_delete'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined

