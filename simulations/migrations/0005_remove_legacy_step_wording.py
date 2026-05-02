from django.db import migrations


def remove_legacy_step_wording(apps, schema_editor):
    SimulationStep = apps.get_model('simulations', 'SimulationStep')
    SimulationStep.objects.filter(text='Answer a short listening quiz').update(
        text='Connect the rhythm to its cultural setting'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0004_remove_quizquestion_hut_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_legacy_step_wording, migrations.RunPython.noop),
    ]
