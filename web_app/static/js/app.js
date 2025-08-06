// Obesity Risk Assessment - Main JavaScript

// Range slider configurations
const rangeConfigs = {
    'fcvc': {
        suffix: ' times/day',
        labels: ['Never', 'Sometimes', 'Always']
    },
    'ncp': {
        suffix: ' meals',
        labels: ['1 meal', '2 meals', '3 meals', '4 meals']
    },
    'ch2o': {
        suffix: ' liters/day',
        labels: ['1L', '1.5L', '2L', '2.5L', '3L', '3.5L', '4L', '4.5L', '5L']
    },
    'faf': {
        suffix: ' days/week',
        labels: ['Never', '1-2 days', '2-4 days', '4-5 days']
    },
    'tue': {
        suffix: ' hours/day',
        labels: ['0-2 hours', '3-5 hours', '5+ hours']
    }
};

// Form sections configuration - only include required fields
const formSections = {
    'personal': ['gender', 'age', 'height', 'weight'],
    'health': ['family_history_with_overweight', 'favc', 'fcvc', 'ncp', 'caec', 'smoke', 'ch2o', 'scc'],
    'lifestyle': ['faf', 'tue', 'calc', 'mtrans']
};

// Update range value displays with better descriptions
function updateRangeValue(inputId, valueId, config) {
    const input = document.getElementById(inputId);
    const value = document.getElementById(valueId);
    
    if (!input || !value) return;
    
    input.addEventListener('input', function() {
        const val = parseInt(this.value);
        const label = config.labels[val - (inputId === 'faf' || inputId === 'tue' ? 0 : 1)];
        value.textContent = `${label} (${this.value}${config.suffix})`;
    });
}

// Initialize all range inputs
function initializeRangeSliders() {
    Object.keys(rangeConfigs).forEach(inputId => {
        updateRangeValue(inputId, inputId + 'Value', rangeConfigs[inputId]);
    });
}

// Check if a section is complete - more flexible logic
function isSectionComplete(sectionFields) {
    let completedFields = 0;
    let totalRequiredFields = 0;
    
    sectionFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && field.hasAttribute('required')) {
            totalRequiredFields++;
            
            // Check if field has a value (including default values for range sliders)
            let hasValue = false;
            if (field.type === 'range') {
                // Range sliders always have a value (default or user-set)
                hasValue = true;
            } else {
                // For other inputs, check if they have a non-empty value
                hasValue = field.value.trim() !== '';
            }
            
            if (hasValue) {
                completedFields++;
            }
        }
    });
    
    // Section is complete if at least 75% of required fields are filled
    const completionRate = totalRequiredFields > 0 ? (completedFields / totalRequiredFields) : 0;
    console.log(`Section completion: ${completedFields}/${totalRequiredFields} = ${completionRate.toFixed(2)}`);
    
    return totalRequiredFields > 0 && completionRate >= 0.75;
}

// Update step indicators based on form completion
function updateStepIndicators() {
    const steps = document.querySelectorAll('.step');
    
    // Check each section
    const personalComplete = isSectionComplete(formSections.personal);
    const healthComplete = isSectionComplete(formSections.health);
    const lifestyleComplete = isSectionComplete(formSections.lifestyle);
    
    console.log('Step completion status:', {
        personal: personalComplete,
        health: healthComplete,
        lifestyle: lifestyleComplete
    });
    
    // Update step indicators
    if (steps.length >= 3) {
        // Personal Info step
        if (personalComplete) {
            steps[0].classList.add('active');
        } else {
            steps[0].classList.remove('active');
        }
        
        // Health Data step
        if (healthComplete) {
            steps[1].classList.add('active');
        } else {
            steps[1].classList.remove('active');
        }
        
        // Lifestyle step
        if (lifestyleComplete) {
            steps[2].classList.add('active');
        } else {
            steps[2].classList.remove('active');
        }
    }
}

// Progress bar functionality
function updateProgress() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    const requiredFields = form.querySelectorAll('[required]');
    const filledFields = Array.from(requiredFields).filter(field => field.value.trim() !== '');
    const progress = (filledFields.length / requiredFields.length) * 100;
    
    const progressFill = document.getElementById('progressFill');
    if (progressFill) {
        progressFill.style.width = progress + '%';
    }
    
    // Also update step indicators
    updateStepIndicators();
}

// Add event listeners for progress tracking
function setupProgressTracking() {
    document.querySelectorAll('input, select').forEach(field => {
        field.addEventListener('input', updateProgress);
        field.addEventListener('change', updateProgress);
    });
}

// Form validation with better UX
function setupFormValidation() {
    const form = document.getElementById('predictionForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const requiredFields = this.querySelectorAll('[required]');
        let isValid = true;
        let firstInvalidField = null;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#e74c3c';
                field.style.boxShadow = '0 0 0 3px rgba(231, 76, 60, 0.1)';
                if (!firstInvalidField) firstInvalidField = field;
            } else {
                field.style.borderColor = '#e1e8ed';
                field.style.boxShadow = 'none';
            }
        });

        if (!isValid) {
            e.preventDefault();
            firstInvalidField.focus();
            alert('Please fill in all required fields marked with *');
        }
    });
}

// Add smooth animations and effects
function setupAnimations() {
    // Add ripple effect to buttons
    document.querySelectorAll('.btn, .submit-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Initialize the application
function initApp() {
    // Initialize all components
    initializeRangeSliders();
    setupProgressTracking();
    setupFormValidation();
    setupAnimations();
    
    // Initialize progress and step indicators with a small delay
    setTimeout(() => {
        updateProgress();
        updateStepIndicators();
    }, 100);
    
    console.log('Obesity Risk Assessment app initialized successfully!');
}

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    initApp();
});

// Export functions for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        updateRangeValue,
        updateProgress,
        setupFormValidation,
        initApp
    };
} 