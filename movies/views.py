from django.shortcuts import render, redirect
from .models import Movie, Review
from django.contrib.auth.decorators import login_required

def index(request):
    search_term = request.GET.get('search_term')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all().prefetch_related('genres')  # Add prefetch for performance
    template_data = {}
    template_data['name'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    # Using prefetch_related for optimized query performance
    movie = Movie.objects.prefetch_related('genres', 'review_set').get(id=id)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = movie.review_set.all()
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)