from django.contrib import admin
from django.urls import path
from ariadne_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(schema=schema), name='graphql'),
]

admin.site.site_header = 'SaaS Admin Panel'
admin.site.site_title = 'SaaS Admin'