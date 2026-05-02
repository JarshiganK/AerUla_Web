from django.db import migrations


SIMULATIONS = {
    'pottery': {
        'steps': ['Prepare and clean the clay', 'Shape the vessel by hand', 'Dry it in shade before firing', 'Fire the pot until it hardens'],
        'question': 'Why is drying the pot before firing important?',
        'options': ['It helps the clay harden evenly', 'It adds paint to the surface', 'It replaces the firing process'],
    },
    'palmyrah': {
        'steps': ['Collect mature palmyrah leaves', 'Dry and split the leaves into strips', 'Weave strips into a repeating pattern', 'Trim and finish the final product'],
        'question': 'What makes palmyrah important to village craft traditions?',
        'options': ['Many parts of the tree can be used', 'It only grows inside factories', 'It cannot be shaped by hand'],
    },
    'cooking': {
        'steps': ['Choose fresh local ingredients', 'Prepare spices and aromatics', 'Cook slowly for balanced flavor', 'Serve as a shared village meal'],
        'question': 'What does the cooking hut emphasize beyond the recipe?',
        'options': ['Shared memory and hospitality', 'Only imported ingredients', 'Eating without preparation'],
    },
    'fishing': {
        'steps': ['Read the weather and water conditions', 'Prepare nets and tools', 'Choose a safe fishing time', 'Sort the catch for home and market'],
        'question': 'What should fishers check before leaving shore?',
        'options': ['Weather and water conditions', 'Only the color of the boat', 'Nothing before travel'],
    },
    'folk-music': {
        'steps': ['Listen to the rhythm pattern', 'Identify the repeated beat', 'Connect the song to its setting', 'Answer a short listening quiz'],
        'question': 'How does folk music support cultural memory?',
        'options': ['It carries stories through performance', 'It removes local language', 'It is only used for written exams'],
    },
}


def seed_simulations(apps, schema_editor):
    Hut = apps.get_model('village', 'Hut')
    SimulationStep = apps.get_model('simulations', 'SimulationStep')
    QuizQuestion = apps.get_model('simulations', 'QuizQuestion')
    QuizOption = apps.get_model('simulations', 'QuizOption')

    for slug, data in SIMULATIONS.items():
        hut = Hut.objects.get(slug=slug)
        preview_order = data['steps'][1::2] + data['steps'][::2]
        preview_index = {text: index for index, text in enumerate(preview_order, start=1)}
        for index, step in enumerate(data['steps'], start=1):
            SimulationStep.objects.update_or_create(
                hut=hut,
                correct_order=index,
                defaults={'text': step, 'preview_order': preview_index[step]},
            )
        question, _ = QuizQuestion.objects.update_or_create(
            hut=hut,
            defaults={'question': data['question']},
        )
        for index, option in enumerate(data['options'], start=1):
            QuizOption.objects.update_or_create(
                question=question,
                display_order=index,
                defaults={'text': option, 'is_correct': index == 1},
            )


class Migration(migrations.Migration):

    dependencies = [
        ('village', '0002_seed_mvp_huts'),
        ('simulations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_simulations, migrations.RunPython.noop),
    ]
