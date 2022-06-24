from django.contrib import admin
from gsras.models import News, NewsImageContent, NewsMapPointFloat


# Register your models here.

class AdminNewsImageContent(admin.TabularInline):
    model = NewsImageContent


class AdminNewsMapPointFloat (admin.StackedInline):
    model = NewsMapPointFloat


@admin.register(News)
class NewsBlock (admin.ModelAdmin):
    list_display = ('title', 'body', "created")
    list_filter = ('title', 'created')
    fields = [("title", "created"), "body", ]
    inlines = [AdminNewsMapPointFloat,  AdminNewsImageContent]
    AdminNewsMapPointFloat.fields = [("lon", "lat")]


