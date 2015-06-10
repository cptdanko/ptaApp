from django.conf.urls import patterns, url
from pta import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
	#url(r'^$', views.index, name='index'),
	url(r'^$', views.login, name='login'),
	url(r'^login$', views.login, name='login'),
	url(r'^pictureCards/$', views.pictureCards, name='pictureCards'),
	url(r'^logout/$', logout, {'template_name':'pta/logout.html'}),
	url(r'^search/$', views.search, name='search'),
	url(r'^reports/$', views.reports, name='reports'),
	#url(r'^index/$', views.index, name='index'),
	url(r'^questionResponses/(?P<fromDate>\d+)/(?P<toDate>\d+)/$', views.questionResponses, name='questionResponses'),
	#url(r'^search/$', views.search, name='search'),
	url(r'^questionnaire/(?P<patient>\d+)/$', views.questionnaire, name='questionnaire'),
	url(r'^patientRpt/(?P<patient>\d+)/(?P<reportType>\w+)/$', views.patientRpt, name='patientReport'),
	url(r'^staffRpt/(?P<staff>\d+)/(?P<reportType>\w+)/$', views.staffRpt, name='staffReport')
)