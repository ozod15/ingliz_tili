from django.contrib import admin
from .models import Verb, UserProfile, TestResult, UserProgress


@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = ['base_form', 'past_simple', 'past_participle', 'translation_uz', 'translation_ru']
    search_fields = ['base_form', 'past_simple', 'past_participle', 'translation_uz', 'translation_ru']
    ordering = ['base_form']
    list_filter = ['base_form']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'xp', 'level', 'total_tests', 'correct_answers', 'accuracy']
    search_fields = ['user__username']
    list_editable = ['avatar']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'verb', 'correct_count', 'wrong_count', 'times_shown', 'accuracy']
    search_fields = ['user__username', 'verb__base_form']
    list_filter = ['user']


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test_type', 'score', 'total_questions', 'percentage', 'xp_earned', 'completed_at']
    search_fields = ['user__username']
    list_filter = ['test_type']
    readonly_fields = ['completed_at']
