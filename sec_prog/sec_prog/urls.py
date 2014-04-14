from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login,logout
from django.contrib import admin
from views import shop, checkout, proceedOrder
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sec_prog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(regex=r'^$',
        view=login,
        kwargs={'template_name': 'main.html'},
        name='login'),

    url(regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': '/'},
        name='logout'),

    url(regex=r'^shop1/$',
        view=shop,
        name='shop'),

    url(regex=r'^checkout/',
        view=checkout,
        #kwargs={'template_name': 'checkout.html'},
        name='checkout'),

    url(regex=r'^proceedOrder/$',
        view= proceedOrder,
        name='proceedOrder'),
)
