from django.db import migrations


HUTS = [
    ('pottery', 'Pottery Hut', 'Pottery', 'available', 'hut-pottery', 'Shape clay into everyday village vessels while learning why pottery matters in Jaffna homes.', 'Arrange the clay preparation, shaping, drying, and firing steps.', 'Clay Keeper', 'Pottery begins with river clay, patient preparation, and hand-shaped forms that become water pots, cooking vessels, and ritual objects. This hut introduces the craft as both practical work and inherited village knowledge.', 1),
    ('palmyrah', 'Palmyrah Craft Hut', 'Palmyrah', 'available', 'hut-palmyrah', 'Explore how palmyrah leaves become woven mats, baskets, and practical household goods.', 'Match leaf strips into a simple repeating craft pattern.', 'Palmyrah Weaver', 'Palmyrah is deeply tied to northern village life. Leaves, fruit, fiber, and timber all support everyday work, and weaving turns prepared leaf strips into useful goods that can travel from home workshops to markets.', 2),
    ('cooking', 'Village Cooking Hut', 'Cooking', 'available', 'hut-cooking', 'Follow a traditional cooking flow built around spices, local produce, and shared meals.', 'Choose the right ingredients for a regional village dish.', 'Kitchen Storyteller', 'The cooking hut connects ingredients, memory, and hospitality. Visitors learn how spices, grains, vegetables, and seafood come together in meals that carry family technique and regional identity.', 3),
    ('fishing', 'Fishing Life Hut', 'Fishing', 'locked', 'hut-fishing', 'Learn how coastal families read weather, tools, and tides before a fishing journey.', 'Match fishing tools to their safe village use.', 'Lagoon Guide', 'Fishing life depends on preparation and respect for the coast. This hut previews how families understand tools, weather, tides, and safety before connecting the catch to village markets and meals.', 4),
    ('folk-music', 'Folk Music Hut', 'Folk Music', 'locked', 'hut-music', 'Discover village songs, rhythms, and storytelling moments connected to festivals and work.', 'Repeat a short rhythm pattern and answer a listening quiz.', 'Rhythm Listener', 'Folk music preserves stories through rhythm, voice, and gathering. This hut previews songs connected to festivals, work, celebration, and oral memory across village life.', 5),
]


def seed_huts(apps, schema_editor):
    Hut = apps.get_model('village', 'Hut')
    for slug, name, short_name, status, position_class, summary, activity, badge_title, story, display_order in HUTS:
        Hut.objects.update_or_create(
            slug=slug,
            defaults={
                'name': name,
                'short_name': short_name,
                'status': status,
                'position_class': position_class,
                'summary': summary,
                'activity': activity,
                'badge_title': badge_title,
                'story': story,
                'display_order': display_order,
                'is_active': True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('village', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_huts, migrations.RunPython.noop),
    ]
