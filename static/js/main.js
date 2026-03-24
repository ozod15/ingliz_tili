/**
 * English Verbs Learning App - Main JavaScript
 */

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('English Verbs Learning App ready');
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// ============================================
// AUDIO PRONUNCIATION FEATURE
// ============================================

/**
 * Speak a word using the browser's SpeechSynthesis API
 */
function speakWord(word) {
    if (!word) return;
    
    // Cancel any ongoing speech
    speechSynthesis.cancel();
    
    // Create utterance
    const utterance = new SpeechSynthesisUtterance(word);
    
    // Set properties for better pronunciation
    utterance.lang = 'en-GB'; // British English
    utterance.rate = 0.9;     // Slightly slower for clarity
    utterance.pitch = 1;
    utterance.volume = 1;
    
    // Speak the word
    speechSynthesis.speak(utterance);
}

/**
 * Make elements with class 'speakable' clickable for pronunciation
 */
function initSpeakableElements() {
    const speakableElements = document.querySelectorAll('.speakable');
    
    speakableElements.forEach(function(element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            const word = this.getAttribute('data-word') || this.textContent;
            speakWord(word);
        });
        
        element.style.cursor = 'pointer';
        
        if (!element.getAttribute('title')) {
            element.setAttribute('title', 'Click to hear pronunciation');
        }
    });
}

// Initialize speakable elements when page loads
document.addEventListener('DOMContentLoaded', initSpeakableElements);

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Get CSRF token from cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Export functions to global scope
window.speakWord = speakWord;
window.initSpeakableElements = initSpeakableElements;
window.getCookie = getCookie;
