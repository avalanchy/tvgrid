from itertools import zip_longest

from django.http import HttpResponse

from imdb.models import Title


def index(request):
    return HttpResponse("Banner and search input.")


def grid(request, title_id):
    try:
        title = Title.objects.filter(id=title_id, title_type=Title.Type.TV_SERIES).get()
    except Title.DoesNotExist:
        return HttpResponse('No such ID.')
    episodes = title.episodes.order_by('season_number', 'episode_number').prefetch_related('title__rating')

    rows = []
    for episode in episodes:
        if episode.episode_number == 1:
            rows.append([episode])
        else:
            rows[episode.season_number - 1].append(episode)

    transposed_rows = list(map(list, zip_longest(*rows)))

    html = f'<html><body><h1>{title.primary_title}</h1><table>'
    for row in transposed_rows:
        html += '<tr>'
        for episode in row:
            if hasattr(episode, 'title'):
                if hasattr(episode.title, 'rating'):
                    html += f'<td>{episode.title.rating.average_rating}</td>'
                else:
                    html += f'<td>?</td>'
            else:
                html += f'<td>-</td>'
        html += '</tr>'
    html += '</table></body></html>'

    return HttpResponse(html)
