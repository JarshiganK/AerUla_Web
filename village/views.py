from django.shortcuts import render


HUTS = [
    {
        'slug': 'pottery',
        'name': 'Pottery Hut',
        'short_name': 'Pottery',
        'status': 'available',
        'position_class': 'hut-pottery',
        'summary': 'Shape clay into everyday village vessels while learning why pottery matters in Jaffna homes.',
        'activity': 'Arrange the clay preparation, shaping, drying, and firing steps.',
        'badge': 'Clay Keeper',
    },
    {
        'slug': 'palmyrah',
        'name': 'Palmyrah Craft Hut',
        'short_name': 'Palmyrah',
        'status': 'available',
        'position_class': 'hut-palmyrah',
        'summary': 'Explore how palmyrah leaves become woven mats, baskets, and practical household goods.',
        'activity': 'Match leaf strips into a simple repeating craft pattern.',
        'badge': 'Palmyrah Weaver',
    },
    {
        'slug': 'cooking',
        'name': 'Village Cooking Hut',
        'short_name': 'Cooking',
        'status': 'available',
        'position_class': 'hut-cooking',
        'summary': 'Follow a traditional cooking flow built around spices, local produce, and shared meals.',
        'activity': 'Choose the right ingredients for a regional village dish.',
        'badge': 'Kitchen Storyteller',
    },
    {
        'slug': 'fishing',
        'name': 'Fishing Life Hut',
        'short_name': 'Fishing',
        'status': 'locked',
        'position_class': 'hut-fishing',
        'summary': 'Learn how coastal families read weather, tools, and tides before a fishing journey.',
        'activity': 'Match fishing tools to their safe village use.',
        'badge': 'Lagoon Guide',
    },
    {
        'slug': 'folk-music',
        'name': 'Folk Music Hut',
        'short_name': 'Folk Music',
        'status': 'locked',
        'position_class': 'hut-music',
        'summary': 'Discover village songs, rhythms, and storytelling moments connected to festivals and work.',
        'activity': 'Repeat a short rhythm pattern and answer a listening quiz.',
        'badge': 'Rhythm Listener',
    },
]


def index(request):
    available_count = sum(hut['status'] == 'available' for hut in HUTS)
    context = {
        'huts': HUTS,
        'available_count': available_count,
        'total_count': len(HUTS),
        'featured_hut': HUTS[0],
    }
    return render(request, 'village/index.html', context)
