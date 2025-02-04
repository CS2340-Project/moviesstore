from django.contrib import admin
from .models import Movie, Review, Genre

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['data']

class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'director', 'release_date', 'rating', 'price', 'availability_status']
    list_filter = ['rating', 'genres', 'availability_status']
    ordering = ['name']
    search_fields = ['name', 'director', 'cast']
    filter_horizontal = ['genres']
    inlines = [ReviewInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image', 'price')
        }),
        ('Movie Details', {
            'fields': ('director', 'cast', 'duration', 'release_date', 'genres')
        }),
        ('Classification', {
            'fields': ('rating', 'user_rating', 'language', 'country')
        }),
        ('Additional Info', {
            'fields': ('trailer_url', 'is_featured', 'availability_status')
        }),
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'rating', 'data']
    list_filter = ['rating', 'is_spoiler', 'data']
    ordering = ['data']
    search_fields = ['comment', 'movie__name', 'user__username']
    readonly_fields = ['data']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre)