from django.db import migrations


def remove_legacy_activity_wording(apps, schema_editor):
    Hut = apps.get_model('village', 'Hut')
    Hut.objects.filter(slug='folk-music').update(
        activity='Repeat a short rhythm pattern and connect it to a village setting.'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('village', '0002_seed_mvp_huts'),
    ]

    operations = [
        migrations.RunPython(remove_legacy_activity_wording, migrations.RunPython.noop),
    ]
