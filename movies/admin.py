from django.contrib import admin

from .models import Movie, Review


class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class ReviewAdmin(admin.ModelAdmin):
    ordering = ['data']
    search_fields = ['comment', 'data']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)