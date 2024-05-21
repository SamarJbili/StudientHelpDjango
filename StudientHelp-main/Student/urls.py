from django.urls import path # type: ignore
from . import views
from .views import EvenementCulturelUpdateView, EvenementScientifiqueUpdateView, TransportUpdateView,LogementUpdateView,MesPostView,eventCultView,eventScView,StageCreateView, LogementCreateView, EvenementScientifiqueCreateView,EvenementCulturelCreateView,TransportCreateView,LogementListView,StageListView,TransportListView,CommentCreateView,PostDetailView,acceuilView,DeleteView


urlpatterns = [
    # URLs for posts
    path('', acceuilView.as_view(), name='acceuil'),
    path('inscription/',views.inscription, name = 'inscription'), 
    path('change-password/',views.change_password, name='change_password'),
    

    path('create-stage/', StageCreateView.as_view(), name='create-stage'),
    path('create-logement/', LogementCreateView.as_view(), name='create-logement'),
    path('create-evenementCulturel/', EvenementCulturelCreateView.as_view(), name='create-evenementCult'),
    path('create-evenementSc/', EvenementScientifiqueCreateView.as_view(), name='create-evenementSc'),
    path('create-transport/', TransportCreateView.as_view(), name='create-transport'),


    path('logement/', LogementListView.as_view(), name='logement-list'),
    path('eventCult/', eventCultView.as_view(), name='eventCult-list'),
    path('eventSc/', eventScView.as_view(), name='eventSc-list'),

    path('stage/', StageListView.as_view(), name='stage-list'),
    path('transport/', TransportListView.as_view(), name='transport-list'),


    path('inscription/',views.register, name = 'register'), 
    path('change-password/',views.change_password, name='change_password'),

    path('search/',views.search, name='search'),

    path('mespost/', MesPostView.as_view(), name='mespost-view'),

    path('inputform/',views.inputform, name='inputform'),
    path('about/', views.about, name='about'),

    path('<int:pk>/deletelog/',DeleteView.as_view(), name='delete_post'),
    

    path('<int:pk>/updatelogement/', LogementUpdateView.as_view(), name='logement-update'),
    path('<int:pk>/updatetransport/', TransportUpdateView.as_view(), name='transport-update'),
    path('<int:pk>/updateeventsc/', EvenementScientifiqueUpdateView.as_view(), name='eventSc-update'),
    path('<int:pk>/updateeventcult/', EvenementCulturelUpdateView.as_view(), name='eventCult-update'),
    path('<int:pk>/updateStage/', LogementUpdateView.as_view(), name='Stage-update'),



    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add-comment'),

    path('like/<int:post_id>/', views. like, name='like_post'),

    path('notifications/', views.notifications, name='notifications'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
