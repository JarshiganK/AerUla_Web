from django.db import models
from django.conf import settings

from village.models import Hut


class SimulationStep(models.Model):
    hut = models.ForeignKey(Hut, on_delete=models.CASCADE, related_name='simulation_steps')
    text = models.CharField(max_length=180)
    correct_order = models.PositiveSmallIntegerField()
    preview_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['correct_order']
        unique_together = [('hut', 'correct_order'), ('hut', 'preview_order')]

    def __str__(self):
        return f'{self.hut.short_name}: {self.text}'


class QuizQuestion(models.Model):
    hut = models.OneToOneField(Hut, on_delete=models.CASCADE, related_name='quiz_question')
    question = models.CharField(max_length=220)

    def __str__(self):
        return self.question


class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=180)
    is_correct = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.text


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hut_progress')
    hut = models.ForeignKey(Hut, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(default=0)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('user', 'hut')]

    def __str__(self):
        return f'{self.user} - {self.hut}'
