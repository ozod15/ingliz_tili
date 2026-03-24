from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Verb, UserProfile, TestResult, UserProgress
from .forms import SimpleRegistrationForm
import random


def home(request):
    """Home page with game-like UI."""
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        recent_tests = TestResult.objects.filter(user=request.user)[:5]
        # Calculate XP progress (percentage within current level)
        xp_in_level = profile.xp % 100
        xp_progress = xp_in_level
        return render(request, 'home.html', {
            'profile': profile,
            'recent_tests': recent_tests,
            'xp_progress': xp_progress,
        })
    return render(request, 'home.html')


def user_login(request):
    """Simple login."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please enter username and password')
    
    return render(request, 'registration/login.html')


def user_register(request):
    """Simple registration with auto login."""
    if request.method == 'POST':
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = SimpleRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def quiz(request):
    """Quiz selection page."""
    return render(request, 'quiz.html')


@login_required
def simple_quiz(request):
    """Simple quiz - one question at a time with form submission."""
    
    # Get or initialize session data
    if 'quiz_verbs' not in request.session:
        # Start new quiz - get 10 random verbs
        all_verbs = list(Verb.objects.all())
        if not all_verbs:
            messages.error(request, "No verbs in database!")
            return redirect('quiz')
        
        quiz_verbs = random.sample(all_verbs, min(10, len(all_verbs)))
        request.session['quiz_verbs'] = [v.id for v in quiz_verbs]
        request.session['quiz_index'] = 0
        request.session['quiz_score'] = 0
        request.session['quiz_answered'] = []
    
    # Get current verb
    verb_ids = request.session.get('quiz_verbs', [])
    index = request.session.get('quiz_index', 0)
    
    if index >= len(verb_ids):
        # Quiz finished - redirect to results
        return redirect('quiz_result_simple')
    
    try:
        verb = Verb.objects.get(id=verb_ids[index])
    except Verb.DoesNotExist:
        messages.error(request, "Verb not found!")
        return redirect('quiz')
    
    # Handle answer submission
    feedback = None
    is_correct = None
    
    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip().lower()
        
        if answer:
            # Check answer (past_simple)
            correct_answer = verb.past_simple.lower()
            is_correct = (answer == correct_answer)
            
            if is_correct:
                request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
                feedback = {'type': 'success', 'message': '✅ Correct!'}
            else:
                feedback = {'type': 'danger', 'message': f'❌ Wrong! Correct answer: {verb.past_simple}'}
            
            # Record answered
            answered = request.session.get('quiz_answered', [])
            answered.append({
                'verb_id': verb.id,
                'base_form': verb.base_form,
                'user_answer': answer,
                'correct_answer': verb.past_simple,
                'is_correct': is_correct
            })
            request.session['quiz_answered'] = answered
            
            # Check if should go to next or show same question
            if 'next' in request.POST:
                request.session['quiz_index'] = index + 1
                return redirect('simple_quiz')
    
    # Calculate progress
    total = len(verb_ids)
    progress = int((index / total) * 100)
    
    return render(request, 'simple_quiz.html', {
        'verb': verb,
        'question_num': index + 1,
        'total_questions': total,
        'progress': progress,
        'score': request.session.get('quiz_score', 0),
        'feedback': feedback,
        'is_correct': is_correct,
        'show_answer': feedback is not None,
    })


def get_adaptive_verb(user):
    """Get next verb based on user performance (adaptive learning)."""
    
    # Get user's progress for all verbs
    user_progress = UserProgress.objects.filter(user=user)
    
    # Get recent questions from session (avoid immediate repetition)
    # This is a simplified version - in production you'd store this more robustly
    
    # Find weak verbs (wrong_count > 0)
    weak_verbs = list(user_progress.filter(wrong_count__gt=0).order_by('-wrong_count', 'times_shown'))
    
    # If user has weak verbs, prioritize them (70% chance)
    if weak_verbs and random.random() < 0.7:
        # Pick from weak verbs (higher chance for more difficult ones)
        return weak_verbs[0].verb
    
    # Otherwise, get a random verb they haven't mastered
    # Get verbs with < 80% accuracy OR new verbs
    all_verbs = list(Verb.objects.all())
    learned_verb_ids = set(user_progress.filter(correct_count__gte=3, wrong_count=0).values_list('verb_id', flat=True))
    
    # Filter to get challenging verbs
    challenging_verbs = [v for v in all_verbs if v.id not in learned_verb_ids]
    
    if challenging_verbs:
        return random.choice(challenging_verbs)
    
    # Fallback: random verb
    return random.choice(all_verbs)


@login_required
def smart_quiz(request):
    """Smart adaptive quiz - learns from user mistakes."""
    
    # Get or initialize session
    if 'smart_quiz_verbs' not in request.session:
        request.session['smart_quiz_verbs'] = []
        request.session['smart_quiz_index'] = 0
        request.session['smart_quiz_score'] = 0
        request.session['smart_quiz_answered'] = []
        request.session['smart_quiz_recent'] = []  # Track recent to avoid repetition
    
    verb_ids = request.session.get('smart_quiz_verbs', [])
    index = request.session.get('smart_quiz_index', 0)
    recent = request.session.get('smart_quiz_recent', [])
    
    # Get new verb if needed
    if index >= len(verb_ids) or not verb_ids:
        # Get adaptive verb
        verb = get_adaptive_verb(request.user)
        
        # Avoid immediate repetition
        while verb.id in recent[-3:] and len(verb_ids) < 50:
            verb = get_adaptive_verb(request.user)
        
        verb_ids.append(verb.id)
        recent.append(verb.id)
        if len(recent) > 10:
            recent = recent[-10:]
        
        request.session['smart_quiz_verbs'] = verb_ids
        request.session['smart_quiz_recent'] = recent
    
    try:
        verb = Verb.objects.get(id=verb_ids[index])
    except (Verb.DoesNotExist, IndexError):
        verb = get_adaptive_verb(request.user)
        verb_ids = [verb.id]
        request.session['smart_quiz_verbs'] = verb_ids
    
    # Handle answer
    feedback = None
    is_correct = None
    
    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip().lower()
        
        if answer:
            correct_answer = verb.past_simple.lower()
            is_correct = (answer == correct_answer)
            
            # Update user progress
            progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                verb=verb,
                defaults={'correct_count': 0, 'wrong_count': 0, 'times_shown': 0}
            )
            progress.times_shown += 1
            
            if is_correct:
                progress.correct_count += 1
                request.session['smart_quiz_score'] = request.session.get('smart_quiz_score', 0) + 1
                feedback = {'type': 'success', 'message': '✅ Correct! Great job!'}
            else:
                progress.wrong_count += 1
                feedback = {'type': 'danger', 'message': f'❌ Wrong! Correct: {verb.past_simple}'}
            
            progress.last_shown = timezone.now()
            progress.save()
            
            # Record answer
            answered = request.session.get('smart_quiz_answered', [])
            answered.append({
                'verb_id': verb.id,
                'base_form': verb.base_form,
                'user_answer': answer,
                'correct_answer': verb.past_simple,
                'is_correct': is_correct
            })
            request.session['smart_quiz_answered'] = answered
            
            # Next question
            if 'next' in request.POST:
                request.session['smart_quiz_index'] = index + 1
                return redirect('smart_quiz')
    
    # Get user stats
    user_progress = UserProgress.objects.filter(user=request.user)
    total_correct = sum(p.correct_count for p in user_progress)
    total_wrong = sum(p.wrong_count for p in user_progress)
    total_attempts = total_correct + total_wrong
    overall_accuracy = int((total_correct / total_attempts * 100)) if total_attempts > 0 else 0
    weak_count = user_progress.filter(wrong_count__gt=0).count()
    
    # Progress
    total = max(len(verb_ids), 10)
    progress = int((index / total) * 100)
    
    return render(request, 'smart_quiz.html', {
        'verb': verb,
        'question_num': index + 1,
        'progress': progress,
        'score': request.session.get('smart_quiz_score', 0),
        'feedback': feedback,
        'is_correct': is_correct,
        'show_answer': feedback is not None,
        # Stats
        'total_correct': total_correct,
        'total_wrong': total_wrong,
        'overall_accuracy': overall_accuracy,
        'weak_count': weak_count,
        'is_adaptive': True,
    })


@login_required
def smart_quiz_result(request):
    """Show smart quiz results."""
    score = request.session.get('smart_quiz_score', 0)
    answered = request.session.get('smart_quiz_answered', [])
    total = len(answered)
    
    percentage = int((score / total) * 100) if total > 0 else 0
    xp_earned = score * 10
    
    # Save result
    if total > 0:
        TestResult.objects.create(
            user=request.user,
            test_type='smart',
            score=score,
            total_questions=total,
            xp_earned=xp_earned
        )
        
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.total_tests += total
        profile.correct_answers += score
        profile.add_xp(xp_earned)
    
    # Clear session
    request.session.pop('smart_quiz_verbs', None)
    request.session.pop('smart_quiz_index', None)
    request.session.pop('smart_quiz_score', None)
    request.session.pop('smart_quiz_answered', None)
    request.session.pop('smart_quiz_recent', None)
    
    return render(request, 'smart_result.html', {
        'score': score,
        'total': total,
        'percentage': percentage,
        'xp_earned': xp_earned,
        'results': answered,
    })


@login_required
def quiz_result_simple(request):
    """Show quiz results."""
    score = request.session.get('quiz_score', 0)
    answered = request.session.get('quiz_answered', [])
    total = len(answered)
    
    percentage = int((score / total) * 100) if total > 0 else 0
    
    # XP earned
    xp_earned = score * 10
    
    # Save to database
    if total > 0:
        TestResult.objects.create(
            user=request.user,
            test_type='fill',
            score=score,
            total_questions=total,
            xp_earned=xp_earned
        )
        
        # Update user profile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.total_tests += total
        profile.correct_answers += score
        profile.add_xp(xp_earned)
    
    # Clear session
    request.session.pop('quiz_verbs', None)
    request.session.pop('quiz_index', None)
    request.session.pop('quiz_score', None)
    request.session.pop('quiz_answered', None)
    
    return render(request, 'simple_result.html', {
        'score': score,
        'total': total,
        'percentage': percentage,
        'xp_earned': xp_earned,
        'results': answered,
    })


# Keep the old quiz system for compatibility
@login_required
def start_quiz(request):
    """Start a quiz - old system."""
    test_type = request.GET.get('type', 'fill')
    num_questions = int(request.GET.get('num', 10))
    
    verbs = list(Verb.objects.all())
    if len(verbs) < num_questions:
        num_questions = len(verbs)
    
    selected_verbs = random.sample(verbs, num_questions)
    
    questions = []
    for verb in selected_verbs:
        if test_type == 'fill':
            questions.append({
                'id': verb.id,
                'base_form': verb.base_form,
                'past_simple': verb.past_simple,
                'past_participle': verb.past_participle,
                'pronunciation': verb.pronunciation,
                'translation': verb.translation,
            })
        elif test_type == 'choice':
            wrong_options = random.sample([v for v in verbs if v.id != verb.id], min(3, len(verbs)-1))
            options = [verb.past_simple] + [v.past_simple for v in wrong_options]
            random.shuffle(options)
            questions.append({
                'id': verb.id,
                'base_form': verb.base_form,
                'correct_answer': verb.past_simple,
                'options': options,
                'translation': verb.translation,
            })
        elif test_type == 'translate':
            questions.append({
                'id': verb.id,
                'base_form': verb.base_form,
                'past_simple': verb.past_simple,
                'past_participle': verb.past_participle,
                'translation': verb.translation,
            })
    
    request.session['quiz_questions'] = questions
    request.session['quiz_type'] = test_type
    request.session['quiz_score'] = 0
    request.session['quiz_answers'] = []
    
    return render(request, 'quiz_play.html', {
        'questions': questions,
        'test_type': test_type,
        'num_questions': num_questions,
    })


@login_required
@require_POST
def submit_answer(request):
    """Submit quiz answer via AJAX."""
    from django.views.decorators.csrf import csrf_exempt
    import json
    
    try:
        data = json.loads(request.body)
        question_id = int(data.get('question_id'))
        user_answer = data.get('answer', '').strip().lower()
        
        questions = request.session.get('quiz_questions', [])
        test_type = request.session.get('quiz_type', 'fill')
        
        question = next((q for q in questions if q.get('id') == question_id), None)
        if not question:
            return JsonResponse({'error': 'Question not found'}, status=400)
        
        correct = False
        correct_answer = ''
        
        if test_type == 'fill':
            correct_past = question.get('past_simple', '').lower()
            correct_participle = question.get('past_participle', '').lower()
            
            user_parts = user_answer.split('/')
            if len(user_parts) == 2:
                user_past = user_parts[0].strip().lower()
                user_participle = user_parts[1].strip().lower()
                correct = (user_past == correct_past and user_participle == correct_participle)
            else:
                correct = (user_answer == correct_past or user_answer == correct_participle)
            
            correct_answer = f"{question.get('past_simple')} / {question.get('past_participle')}"
            
        elif test_type == 'choice':
            correct_answer = question.get('correct_answer', '').lower()
            correct = (user_answer == correct_answer)
            
        elif test_type == 'translate':
            correct_answer = question.get('translation', '').lower()
            correct = (user_answer == correct_answer)
        
        if correct:
            request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
        
        answers = request.session.get('quiz_answers', [])
        answers.append({
            'question_id': question_id,
            'user_answer': user_answer,
            'correct': correct,
            'correct_answer': correct_answer,
        })
        request.session['quiz_answers'] = answers
        
        return JsonResponse({
            'correct': correct,
            'correct_answer': correct_answer,
            'current_score': request.session.get('quiz_score', 0),
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def quiz_result(request):
    """Show quiz results with XP - old system."""
    questions = request.session.get('quiz_questions', [])
    answers = request.session.get('quiz_answers', [])
    test_type = request.session.get('quiz_type', 'fill')
    score = request.session.get('quiz_score', 0)
    total = len(questions)
    
    # XP earned: 10 XP per correct answer
    xp_earned = score * 10
    
    if total > 0:
        test_result = TestResult.objects.create(
            user=request.user,
            test_type=test_type,
            score=score,
            total_questions=total,
            xp_earned=xp_earned
        )
        
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.total_tests += total
        profile.correct_answers += score
        profile.add_xp(xp_earned)
    
    results = []
    for answer in answers:
        question = next((q for q in questions if q.get('id') == answer['question_id']), None)
        if question:
            results.append({
                'question': question,
                'user_answer': answer['user_answer'],
                'correct_answer': answer['correct_answer'],
                'is_correct': answer['correct'],
            })
    
    percentage = round((score / total) * 100, 1) if total > 0 else 0
    
    request.session.pop('quiz_questions', None)
    request.session.pop('quiz_type', None)
    request.session.pop('quiz_score', None)
    request.session.pop('quiz_answers', None)
    
    return render(request, 'result.html', {
        'score': score,
        'total': total,
        'percentage': percentage,
        'xp_earned': xp_earned,
        'results': results,
        'test_type': test_type,
    })


@login_required
def profile(request):
    """Profile page with settings."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    test_results = TestResult.objects.filter(user=request.user)[:10]
    
    # Calculate XP progress (percentage within current level)
    xp_in_level = profile.xp % 100
    xp_progress = xp_in_level
    
    # Get avatar emoji
    avatar_emoji = {
        'avatar1': '👨‍🎓', 'avatar2': '👩‍🏫', 'avatar3': '🚀',
        'avatar4': '⭐', 'avatar5': '🔥', 'avatar6': '💎',
        'avatar7': '🏆', 'avatar8': '🌟'
    }
    
    return render(request, 'profile.html', {
        'profile': profile,
        'test_results': test_results,
        'avatar_emoji': avatar_emoji,
        'xp_progress': xp_progress,
    })


@login_required
@require_POST
def change_username(request):
    """Change username via AJAX."""
    import json
    try:
        data = json.loads(request.body)
        new_username = data.get('username', '').strip()
        
        if not new_username:
            return JsonResponse({'success': False, 'message': 'Username cannot be empty'})
        
        if User.objects.exclude(pk=request.user.pk).filter(username=new_username).exists():
            return JsonResponse({'success': False, 'message': 'Username already taken'})
        
        request.user.username = new_username
        request.user.save()
        
        return JsonResponse({'success': True, 'message': 'Username updated!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_POST
def change_password(request):
    """Change password via AJAX."""
    import json
    try:
        data = json.loads(request.body)
        new_password = data.get('password', '')
        
        if not new_password:
            return JsonResponse({'success': False, 'message': 'Password cannot be empty'})
        
        request.user.set_password(new_password)
        request.user.save()
        
        return JsonResponse({'success': True, 'message': 'Password updated!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_POST
def change_avatar(request):
    """Change avatar via AJAX."""
    import json
    try:
        data = json.loads(request.body)
        new_avatar = data.get('avatar', 'avatar1')
        
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.avatar = new_avatar
        profile.save()
        
        return JsonResponse({'success': True, 'message': 'Avatar updated!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def verbs_list(request):
    """View all verbs."""
    verbs = Verb.objects.all()
    return render(request, 'verbs_list.html', {'verbs': verbs})


def leaderboard(request):
    """Leaderboard page showing top users by XP."""
    profiles = UserProfile.objects.select_related('user').order_by('-xp', '-correct_answers')[:50]
    
    # Add rank to each profile
    leaderboard_data = []
    for rank, profile in enumerate(profiles, 1):
        leaderboard_data.append({
            'rank': rank,
            'username': profile.user.username,
            'xp': profile.xp,
            'level': profile.level,
            'correct_answers': profile.correct_answers,
            'avatar': profile.avatar,
        })
    
    # Get current user rank if logged in
    user_rank = None
    if request.user.is_authenticated:
        try:
            user_profile = request.user.profile
            # Calculate user's rank
            higher_xp_count = UserProfile.objects.filter(xp__gt=user_profile.xp).count()
            user_rank = higher_xp_count + 1
        except UserProfile.DoesNotExist:
            pass
    
    return render(request, 'leaderboard.html', {
        'leaderboard': leaderboard_data,
        'user_rank': user_rank,
    })
