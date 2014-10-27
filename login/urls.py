from django.conf.urls import patterns,url
from login import views

urlpatterns = patterns('',
url(r'^home/', views.loginorsignup),
url(r'^checkuser/', views.checkuser),
url(r'^userpage/', views.userpage),
url(r'^signout/', views.signoutview),
url(r'^blogpageview/(\d+)/$', views.blogpageview),
url(r'^createblog/', views.createblogview),
url(r'^blogpage/', views.editblogpageview),
url(r'^updateblog/', views.updateblogview),
url(r'^addcomment/', views.addcommentview),
)
