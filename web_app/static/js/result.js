// Result Page JavaScript for Obesity Risk Assessment

// Add some interactive effects
function setupResultAnimations() {
    // Animate the result value
    const resultValue = document.querySelector('.result-value');
    if (resultValue) {
        resultValue.style.opacity = '0';
        resultValue.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            resultValue.style.transition = 'all 0.6s ease-out';
            resultValue.style.opacity = '1';
            resultValue.style.transform = 'scale(1)';
        }, 300);
    }

    // Add click effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
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

// Add print functionality
function printResult() {
    window.print();
}

// Add category-specific animations
function setupCategoryAnimations() {
    const categoryIndicator = document.querySelector('.category-indicator');
    if (categoryIndicator) {
        // Add a subtle bounce animation
        categoryIndicator.style.animation = 'bounce 0.6s ease-out';
    }
}

// Add CSS for bounce animation
function addBounceAnimation() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }
    `;
    document.head.appendChild(style);
}

// Initialize the result page
function initResultPage() {
    addBounceAnimation();
    setupResultAnimations();
    setupCategoryAnimations();
    
    console.log('Result page initialized successfully!');
}

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    initResultPage();
});

// Export functions for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        setupResultAnimations,
        printResult,
        initResultPage
    };
} 