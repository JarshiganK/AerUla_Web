from decimal import Decimal

from django.db import migrations


PRODUCTS = [
    ('clay-serving-bowl', 'pottery', 'Clay Serving Bowl', Decimal('2400.00'), 'available', 'A hand-shaped bowl inspired by everyday village pottery and shared meals.', 'Nallur Clay Studio', 'Local clay, natural mineral finish', 12, 1),
    ('handmade-water-pot', 'pottery', 'Handmade Water Pot', Decimal('4800.00'), 'limited', 'A traditional cooling vessel connected to the pottery learning path.', 'Kopay Pottery Collective', 'Fired red clay', 4, 2),
    ('woven-palmyrah-basket', 'palmyrah', 'Woven Palmyrah Basket', Decimal('3200.00'), 'available', 'A sturdy woven basket made with prepared palmyrah strips.', 'Vaddukoddai Weavers', 'Dried palmyrah leaf', 10, 3),
    ('village-spice-mix', 'cooking', 'Village Spice Mix', Decimal('1250.00'), 'available', 'A small-batch spice blend for recreating the cooking hut flavor profile.', 'Ammamma Kitchen', 'Roasted spices', 20, 4),
    ('folk-song-booklet', 'folk-music', 'Folk Song Booklet', Decimal('1800.00'), 'preview', 'A printed starter booklet for village songs, rhythms, and performance notes.', 'Community Archive', 'Printed booklet', 0, 5),
]


def seed_products(apps, schema_editor):
    Hut = apps.get_model('village', 'Hut')
    Product = apps.get_model('marketplace', 'Product')
    for slug, hut_slug, name, price, status, summary, artisan, materials, stock, display_order in PRODUCTS:
        Product.objects.update_or_create(
            slug=slug,
            defaults={
                'hut': Hut.objects.get(slug=hut_slug),
                'name': name,
                'price': price,
                'currency': 'LKR',
                'status': status,
                'summary': summary,
                'artisan': artisan,
                'materials': materials,
                'stock': stock,
                'is_published': True,
                'display_order': display_order,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('village', '0002_seed_mvp_huts'),
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_products, migrations.RunPython.noop),
    ]
