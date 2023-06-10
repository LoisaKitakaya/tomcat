from .schema import schema
from django.urls import path
from django.contrib import admin
from ariadne_django.views import GraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema), name="graphql"),
]

admin.site.site_header = "SaaS Admin Panel"
admin.site.site_title = "SaaS Admin"
