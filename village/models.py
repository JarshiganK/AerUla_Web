from django.db import models


class Hut(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_LOCKED = 'locked'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_LOCKED, 'Locked'),
    ]

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    position_class = models.CharField(max_length=80)
    summary = models.TextField()
    activity = models.CharField(max_length=180)
    badge_title = models.CharField(max_length=120)
    story = models.TextField()
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    @property
    def badge(self):
        return self.badge_title

    @property
    def image(self):
        return HUT_MEDIA.get(self.slug, HUT_MEDIA['default'])

    @property
    def image_url(self):
        return self.image['url']

    @property
    def image_alt(self):
        return self.image['alt']

    @property
    def image_credit(self):
        return self.image['credit']

    @property
    def image_source_url(self):
        return self.image['source_url']

    @property
    def simulation_scene(self):
        return HUT_SCENES.get(self.slug, HUT_SCENES['default'])

    @property
    def simulation_360(self):
        return HUT_360_MEDIA.get(self.slug, HUT_360_MEDIA['default'])


HUT_MEDIA = {
    'pottery': {
        'url': 'https://commons.wikimedia.org/wiki/Special:FilePath/Tradtional_Sri_Lankan_Pottery.jpg?width=1200',
        'alt': 'Traditional Sri Lankan pottery vessel with red and white clay decoration.',
        'credit': 'Traditional Sri Lankan Pottery, VinPrasad, CC BY-SA 4.0',
        'source_url': 'https://commons.wikimedia.org/wiki/File:Tradtional_Sri_Lankan_Pottery.jpg',
    },
    'palmyrah': {
        'url': 'https://commons.wikimedia.org/wiki/Special:FilePath/Palmyra_Product_Shop-Jaffna-1.jpg?width=1200',
        'alt': 'Palmyrah leaf products displayed in a Jaffna shop.',
        'credit': 'Palmyra Product Shop-Jaffna-1, Mayooranathan, Wikimedia Commons',
        'source_url': 'https://commons.wikimedia.org/wiki/File:Palmyra_Product_Shop-Jaffna-1.jpg',
    },
    'cooking': {
        'url': 'https://commons.wikimedia.org/wiki/Special:FilePath/Traditional_Jaffna_Rice_and_Curry.JPG?width=1200',
        'alt': 'Traditional Jaffna rice and curry served in Point Pedro, Sri Lanka.',
        'credit': 'Traditional Jaffna Rice and Curry, Mayooresan, Wikimedia Commons',
        'source_url': 'https://commons.wikimedia.org/wiki/File:Traditional_Jaffna_Rice_and_Curry.JPG',
    },
    'fishing': {
        'url': 'https://commons.wikimedia.org/wiki/Special:FilePath/Fisherman_hauling_nets_Sri_Lanka_Photo208.jpg?width=1200',
        'alt': 'Sri Lankan fishermen hauling nets near the coast.',
        'credit': 'Fisherman hauling nets Sri Lanka Photo208, Wikimedia Commons',
        'source_url': 'https://commons.wikimedia.org/wiki/File:Fisherman_hauling_nets_Sri_Lanka_Photo208.jpg',
    },
    'folk-music': {
        'url': 'https://commons.wikimedia.org/wiki/Special:FilePath/Traditional_drum_player.jpg?width=1200',
        'alt': 'Traditional Sri Lankan drum player performing at a ceremony.',
        'credit': 'Traditional drum player, Yumeshan Lakshitha, Wikimedia Commons',
        'source_url': 'https://commons.wikimedia.org/wiki/File:Traditional_drum_player.jpg',
    },
    'default': {
        'url': 'https://commons.wikimedia.org/wiki/Special:FilePath/Sri_Lankan_Rice_and_Curry.jpg?width=1200',
        'alt': 'Sri Lankan cultural food and craft reference image.',
        'credit': 'Sri Lankan Rice and Curry, Lankan Foodie, Wikimedia Commons',
        'source_url': 'https://commons.wikimedia.org/wiki/File:Sri_Lankan_Rice_and_Curry.jpg',
    },
}


HUT_SCENES = {
    'pottery': {
        'surface': 'Clay wheel',
        'tool': 'Shaping hand',
        'material': 'River clay',
    },
    'palmyrah': {
        'surface': 'Weaving mat',
        'tool': 'Leaf strip',
        'material': 'Palmyrah fiber',
    },
    'cooking': {
        'surface': 'Hearth pot',
        'tool': 'Spice ladle',
        'material': 'Curry base',
    },
    'fishing': {
        'surface': 'Lagoon net',
        'tool': 'Net marker',
        'material': 'Tide route',
    },
    'folk-music': {
        'surface': 'Drum circle',
        'tool': 'Rhythm beat',
        'material': 'Call pattern',
    },
    'default': {
        'surface': 'Village bench',
        'tool': 'Practice tool',
        'material': 'Learning material',
    },
}


HUT_360_MEDIA = {
    'pottery': {
        'video_url': '/media/simulations/360/pottery.mp4',
        'duration_required': 20,
        'coverage_required': 240,
        'hotspots': [
            {'id': 'clay-wheel', 'label': 'Clay wheel', 'yaw': -32, 'pitch': -4},
            {'id': 'drying-shelf', 'label': 'Drying shelf', 'yaw': 58, 'pitch': 6},
            {'id': 'kiln-fire', 'label': 'Kiln fire', 'yaw': 142, 'pitch': -2},
        ],
    },
    'default': {
        'video_url': '/media/simulations/360/village.mp4',
        'duration_required': 20,
        'coverage_required': 240,
        'hotspots': [
            {'id': 'work-area', 'label': 'Work area', 'yaw': -25, 'pitch': 0},
            {'id': 'materials', 'label': 'Materials', 'yaw': 72, 'pitch': 4},
            {'id': 'host-guide', 'label': 'Host guide', 'yaw': 154, 'pitch': 0},
        ],
    },
}
