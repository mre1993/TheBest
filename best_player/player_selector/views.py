from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Vote, BestHomo
from .forms import VoteForm, ParentSelectionForm, ChildSelectionForm
from django.db.models import Count, F
from collections import defaultdict
from django.http import JsonResponse


@login_required
def vote(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data['player']
            # Check if the user has already voted for this player
            if not Vote.objects.filter(
                player=player,
                user=request.user
            ).exists():
                Vote.objects.create(player=player, user=request.user)
                return redirect('player:vote_success')
            else:
                return render(request, 'vote.html', {
                    'form': form,
                    'error': f'You have already voted for "{player}" in this category.'
                })
    else:
        form = VoteForm()
    return render(request, 'vote.html', {'form': form})
        



@login_required
def new_besthomo_view(request):
    if request.method == 'POST':
        form = ParentSelectionForm(request.POST)
        if form.is_valid():
            request.session['besthomo_name'] = form.cleaned_data['name']
            request.session['place_parent'] = form.cleaned_data['place_parent'].id
            request.session['time_parent'] = form.cleaned_data['time_parent'].id
            request.session['field_parent'] = form.cleaned_data['field_parent'].id

            return redirect('player:new_besthomo2')
    else:
        form = ParentSelectionForm()

    return render(request, 'new_besthomo.html', {'form': form})

@login_required
def new_besthomo_view2(request):
    parent_selections = {
        "place_parent": request.session.get("place_parent"),
        "time_parent": request.session.get("time_parent"),
        "field_parent": request.session.get("field_parent"),
    }

    if request.method == 'POST':
        form = ChildSelectionForm(request.POST, parent_selections=parent_selections)
        if form.is_valid():
            # Get selected child objects
            place_child = form.cleaned_data.get('place_child')
            time_child = form.cleaned_data.get('time_child')
            field_child = form.cleaned_data.get('field_child')

            # Create a new BestHomo instance and link selected items
            besthomo = BestHomo.objects.create(name=request.session.get("besthomo_name"))
            if place_child:
                besthomo.place.add(place_child)
            if time_child:
                besthomo.time.add(time_child)
            if field_child:
                besthomo.field.add(field_child)

            return redirect('player:vote')
    else:
        form = ChildSelectionForm(parent_selections=parent_selections)

    return render(request, 'new_besthomo2.html', {'form': form})


def vote_success_view(request):
    grouped_votes = defaultdict(list)

    votes = (
        Vote.objects
        .select_related('player')
        .prefetch_related('player__place', 'player__time', 'player__field')
        .annotate(
            place_name=F('player__place__name'),
            field_name=F('player__field__name'),
            time_name=F('player__time__name')
        )
        .values(
            'player__name',
            'place_name',
            'field_name',
            'time_name'
        )
        .annotate(vote_count=Count('id'))
    )

    for vote in votes:
        place_name = vote.get('place_name', 'Unknown Place')
        field_name = vote.get('field_name', 'Unknown Field')
        time_name = vote.get('time_name', 'Unknown Time')

        key = f"Best {field_name} of {time_name} in {place_name}"
        grouped_votes[key].append({
            'name': vote['player__name'],
            'vote_count': vote['vote_count']
        })

    return render(request, 'vote_success.html', {'grouped_votes': grouped_votes})


def fetch_votes(request):
    grouped_votes = defaultdict(list)

    votes = (
        Vote.objects
        .select_related('player')
        .prefetch_related('player__place', 'player__time', 'player__field')
        .annotate(
            place_name=F('player__place__name'),
            field_name=F('player__field__name'),
            time_name=F('player__time__name')
        )
        .values(
            'player__name',
            'place_name',
            'field_name',
            'time_name'
        )
        .annotate(vote_count=Count('id'))
    )

    for vote in votes:
        place_name = vote.get('place_name', 'Unknown Place')
        field_name = vote.get('field_name', 'Unknown Field')
        time_name = vote.get('time_name', 'Unknown Time')

        key = f"Best {field_name} of {time_name} in {place_name}"
        grouped_votes[key].append({
            'name': vote['player__name'],
            'vote_count': vote['vote_count']
        })

    return JsonResponse({'grouped_votes': grouped_votes})
