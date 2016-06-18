from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NewCaseCreateView.as_view(), name='home'),
    url(r'^$', views.NewCaseCreateView.as_view(), name='add'),
    url(r'^rejestr$', views.LetterListView.as_view(), name='list'),
    url(r'^sprawa-(?P<case_pk>\d+)/$', views.LetterCreateView.as_view(), name="add"),
    url(r'^(?P<pk>\d+)/wyslij/$', views.LetterSendView.as_view(), name="send"),
    url(r'^(?P<pk>\d+)/edytuj/$', views.LetterUpdateView.as_view(), name="edit"),
]
