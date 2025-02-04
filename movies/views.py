from django.shortcuts import render
from .models import Movie

def index(request):
    search_term = request.GET.get('search_term')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all().prefetch_related('genres')  # Add prefetch for performance

    template_data = {}
    template_data['name'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',{'template_data': template_data})

def show(request, id):
    movie = Movie.objects.prefetch_related('genres', 'review_set').get(id=id)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = movie.review_set.all()
    return render(request, 'movies/show.html', {'template_data': template_data})