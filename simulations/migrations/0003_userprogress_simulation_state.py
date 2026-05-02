from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0002_seed_mvp_simulations'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprogress',
            name='quiz_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='simulation_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='simulation_score',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
