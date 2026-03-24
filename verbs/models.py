from django.db import models
from django.contrib.auth.models import User


class Verb(models.Model):
    """English irregular verb model."""
    base_form = models.CharField(max_length=100)
    past_simple = models.CharField(max_length=100)
    past_participle = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=200)
    translation_uz = models.CharField(max_length=200, default='', verbose_name='Uzbek Translation')
    translation_ru = models.CharField(max_length=200, default='', blank=True, verbose_name='Russian Translation')
    translation_en = models.CharField(max_length=200, default='', blank=True, verbose_name='English Meaning')
    
    class Meta:
        ordering = ['base_form']
    
    def __str__(self):
        return self.base_form
    
    @property
    def translation(self):
        """For backward compatibility."""
        return self.translation_uz
    
    def get_translation(self, lang='uz'):
        """Get translation by language code."""
        if lang == 'ru':
            return self.translation_ru or self.translation_uz
        elif lang == 'en':
            return self.translation_en or self.base_form
        return self.translation_uz


class UserProfile(models.Model):
    """Extended user profile with game features."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    total_tests = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    
    AVATAR_CHOICES = [
        ('avatar1', '👨‍🎓 Student'),
        ('avatar2', '👩‍🏫 Teacher'),
        ('avatar3', '🚀 Rocket'),
        ('avatar4', '⭐ Star'),
        ('avatar5', '🔥 Fire'),
        ('avatar6', '💎 Diamond'),
        ('avatar7', '🏆 Trophy'),
        ('avatar8', '🌟 Lightning'),
    ]
    avatar = models.CharField(max_length=20, choices=AVATAR_CHOICES, default='avatar1')
    
    @property
    def accuracy(self):
        if self.total_tests == 0:
            return 0
        return round((self.correct_answers / self.total_tests) * 100, 1)
    
    def add_xp(self, amount):
        """Add XP and update level."""
        self.xp += amount
        # Level up every 100 XP
        new_level = (self.xp // 100) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level}"


class TestResult(models.Model):
    """Store test results."""
    TEST_TYPES = [
        ('fill', 'Fill in Past Forms'),
        ('choice', 'Multiple Choice'),
        ('translate', 'Translation'),
        ('smart', 'Smart Quiz'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    test_type = models.CharField(max_length=20, choices=TEST_TYPES)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    xp_earned = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def percentage(self):
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100, 1)
    
    class Meta:
        ordering = ['-completed_at']


class UserProgress(models.Model):
    """Track user performance for each verb (adaptive learning)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE, related_name='user_progress')
    correct_count = models.IntegerField(default=0)
    wrong_count = models.IntegerField(default=0)
    last_shown = models.DateTimeField(auto_now_add=True)
    times_shown = models.IntegerField(default=0)
    
    @property
    def accuracy(self):
        total = self.correct_count + self.wrong_count
        if total == 0:
            return 0
        return round((self.correct_count / total) * 100, 1)
    
    @property
    def difficulty_score(self):
        """Higher score = harder word (more wrong answers)"""
        if self.times_shown == 0:
            return 0
        # Score based on wrong percentage and frequency
        return (self.wrong_count * 10) + (self.times_shown * 2)
    
    class Meta:
        unique_together = ('user', 'verb')
        ordering = ['-wrong_count', 'times_shown']
    
    def __str__(self):
        return f"{self.user.username} - {self.verb.base_form}: {self.correct_count}/{self.correct_count + self.wrong_count}"
