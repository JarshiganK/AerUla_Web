EXPERIENCES = [
    {
        'slug': 'pottery-workshop',
        'title': 'Pottery Workshop Visit',
        'hut_slug': 'pottery',
        'hut_name': 'Pottery Hut',
        'host': 'Kopay Pottery Collective',
        'duration': '2 hours',
        'price': 'LKR 6,500',
        'status': 'Taking requests',
        'summary': 'Meet a village pottery host, learn the vessel-making process, and try a guided clay shaping activity.',
        'includes': ['Host-led craft story', 'Hands-on clay shaping', 'Tea and discussion'],
    },
    {
        'slug': 'palmyrah-weaving-session',
        'title': 'Palmyrah Weaving Session',
        'hut_slug': 'palmyrah',
        'hut_name': 'Palmyrah Craft Hut',
        'host': 'Vaddukoddai Weavers',
        'duration': '90 minutes',
        'price': 'LKR 5,200',
        'status': 'Taking requests',
        'summary': 'Learn how dried palmyrah strips are prepared, patterned, and finished into useful goods.',
        'includes': ['Material preparation demo', 'Beginner weaving pattern', 'Finished sample to take home'],
    },
    {
        'slug': 'village-cooking-table',
        'title': 'Village Cooking Table',
        'hut_slug': 'cooking',
        'hut_name': 'Village Cooking Hut',
        'host': 'Ammamma Kitchen',
        'duration': '3 hours',
        'price': 'LKR 8,900',
        'status': 'Preview',
        'summary': 'Cook with a host family and connect ingredients, stories, and hospitality around a shared meal.',
        'includes': ['Ingredient walkthrough', 'Shared cooking session', 'Meal with host family'],
    },
]


def get_experience(slug):
    return next((experience for experience in EXPERIENCES if experience['slug'] == slug), None)
