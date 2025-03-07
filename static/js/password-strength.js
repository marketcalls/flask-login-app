document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    if (!passwordInput) return;

    const strengthMeter = document.getElementById('password-strength-meter');
    const strengthText = document.getElementById('password-strength-text');
    
    // Password requirement elements
    const reqLength = document.getElementById('req-length');
    const reqUppercase = document.getElementById('req-uppercase');
    const reqLowercase = document.getElementById('req-lowercase');
    const reqNumber = document.getElementById('req-number');
    const reqSpecial = document.getElementById('req-special');

    passwordInput.addEventListener('input', function() {
        const password = passwordInput.value;
        const result = calculatePasswordStrength(password);
        
        // Update strength meter
        strengthMeter.style.width = result.score + '%';
        strengthMeter.className = 'h-2 rounded-full ' + getColorClass(result.score);
        strengthText.textContent = result.strengthText;
        
        // Update requirement indicators
        updateRequirement(reqLength, password.length >= 12);
        updateRequirement(reqUppercase, /[A-Z]/.test(password));
        updateRequirement(reqLowercase, /[a-z]/.test(password));
        updateRequirement(reqNumber, /[0-9]/.test(password));
        updateRequirement(reqSpecial, /[!@#$%^&*()\-_=+{};:,<.>]/.test(password));
    });

    function calculatePasswordStrength(password) {
        // Initialize with a base score of 0
        let score = 0;
        let strengthText = 'Not entered';

        if (password.length === 0) {
            return { score: 0, strengthText: 'Not entered' };
        }

        // Length check (up to 40%)
        const lengthScore = Math.min(password.length * 3, 40);
        score += lengthScore;

        // Complexity checks (up to 60%)
        if (/[A-Z]/.test(password)) score += 10; // Uppercase
        if (/[a-z]/.test(password)) score += 10; // Lowercase
        if (/[0-9]/.test(password)) score += 15; // Numbers
        if (/[!@#$%^&*()\-_=+{};:,<.>]/.test(password)) score += 25; // Special chars

        // Check for common patterns and reduce score
        if (/(.)\1{2,}/.test(password)) score -= 10; // Repeated characters
        if (/^(12345|qwerty|asdfgh|password|admin)/.test(password.toLowerCase())) score -= 20;

        // Ensure score is between 0-100
        score = Math.max(0, Math.min(score, 100));

        // Determine strength text
        if (score < 20) strengthText = 'Very Weak';
        else if (score < 40) strengthText = 'Weak';
        else if (score < 60) strengthText = 'Moderate';
        else if (score < 80) strengthText = 'Strong';
        else strengthText = 'Very Strong';

        return { score, strengthText };
    }

    function getColorClass(score) {
        if (score < 20) return 'bg-red-500';
        if (score < 40) return 'bg-orange-500';
        if (score < 60) return 'bg-yellow-500';
        if (score < 80) return 'bg-lime-500';
        return 'bg-green-500';
    }

    function updateRequirement(element, isValid) {
        if (!element) return;
        
        if (isValid) {
            element.classList.remove('text-gray-500');
            element.classList.add('text-green-500');
        } else {
            element.classList.remove('text-green-500');
            element.classList.add('text-gray-500');
        }
    }
});
