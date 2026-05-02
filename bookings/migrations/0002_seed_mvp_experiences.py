from decimal import Decimal

from django.db import migrations


EXPERIENCES = [
    ('pottery-workshop', 'pottery', 'Pottery Workshop Visit', 'Kopay Pottery Collective', '2 hours', Decimal('6500.00'), 'taking_requests', 'Meet a village pottery host, learn the vessel-making process, and try a guided clay shaping activity.', ['Host-led craft story', 'Hands-on clay shaping', 'Tea and discussion'], 1),
    ('palmyrah-weaving-session', 'palmyrah', 'Palmyrah Weaving Session', 'Vaddukoddai Weavers', '90 minutes', Decimal('5200.00'), 'taking_requests', 'Learn how dried palmyrah strips are prepared, patterned, and finished into useful goods.', ['Material preparation demo', 'Beginner weaving pattern', 'Finished sample to take home'], 2),
    ('village-cooking-table', 'cooking', 'Village Cooking Table', 'Ammamma Kitchen', '3 hours', Decimal('8900.00'), 'preview', 'Cook with a host family and connect ingredients, stories, and hospitality around a shared meal.', ['Ingredient walkthrough', 'Shared cooking session', 'Meal with host family'], 3),
]


def seed_experiences(apps, schema_editor):
    Hut = apps.get_model('village', 'Hut')
    Experience = apps.get_model('bookings', 'Experience')
    for slug, hut_slug, title, host, duration, price, status, summary, includes, display_order in EXPERIENCES:
        Experience.objects.update_or_create(
            slug=slug,
            defaults={
                'hut': Hut.objects.get(slug=hut_slug),
                'title': title,
                'host': host,
                'duration': duration,
                'price': price,
                'currency': 'LKR',
                'status': status,
                'summary': summary,
                'includes': includes,
                'is_published': True,
                'display_order': display_order,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('village', '0002_seed_mvp_huts'),
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_experiences, migrations.RunPython.noop),
    ]
