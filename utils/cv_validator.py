import re
from typing import Dict, List, Tuple

class CVValidator:
    def __init__(self):
        self.min_length = 200
        self.max_length = 10000
        self.required_sections = ['doświadczenie', 'experience', 'praca', 'work', 'wykształcenie', 'education']
        self.suspicious_patterns = [
            r'lorem ipsum',
            r'placeholder',
            r'sample text',
            r'example@example\.com',
            r'john doe',
            r'jane doe'
        ]
    
    def validate_cv(self, cv_text: str) -> Dict:
        """Comprehensive CV validation"""
        results = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'suggestions': [],
            'quality_score': 0
        }
        
        # Length validation
        if len(cv_text) < self.min_length:
            results['errors'].append(f"CV jest zbyt krótkie ({len(cv_text)} znaków). Minimum: {self.min_length}")
            results['is_valid'] = False
        elif len(cv_text) > self.max_length:
            results['warnings'].append(f"CV jest bardzo długie ({len(cv_text)} znaków). Może być trudne do przetworzenia.")
        
        # Check for required sections
        missing_sections = self._check_required_sections(cv_text)
        if missing_sections:
            results['warnings'].append(f"Brakuje sekcji: {', '.join(missing_sections)}")
        
        # Check for suspicious patterns
        suspicious_found = self._check_suspicious_patterns(cv_text)
        if suspicious_found:
            results['warnings'].append(f"Wykryto podejrzane wzorce: {', '.join(suspicious_found)}")
        
        # Check for contact information
        contact_info = self._check_contact_info(cv_text)
        if not contact_info['has_email']:
            results['suggestions'].append("Dodaj adres email")
        if not contact_info['has_phone']:
            results['suggestions'].append("Dodaj numer telefonu")
        
        # Calculate quality score
        results['quality_score'] = self._calculate_quality_score(cv_text, results)
        
        return results
    
    def _check_required_sections(self, cv_text: str) -> List[str]:
        """Check for required CV sections"""
        text_lower = cv_text.lower()
        missing = []
        
        has_experience = any(section in text_lower for section in ['doświadczenie', 'experience', 'praca zawodowa'])
        has_education = any(section in text_lower for section in ['wykształcenie', 'education', 'edukacja'])
        
        if not has_experience:
            missing.append("Doświadczenie zawodowe")
        if not has_education:
            missing.append("Wykształcenie")
        
        return missing
    
    def _check_suspicious_patterns(self, cv_text: str) -> List[str]:
        """Check for suspicious patterns that might indicate fake/template content"""
        found_patterns = []
        text_lower = cv_text.lower()
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, text_lower):
                found_patterns.append(pattern)
        
        return found_patterns
    
    def _check_contact_info(self, cv_text: str) -> Dict:
        """Check for contact information"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?[0-9]{1,3}[-.\s]?)?[0-9]{3}[-.\s]?[0-9]{3}[-.\s]?[0-9]{3,4}'
        
        has_email = bool(re.search(email_pattern, cv_text))
        has_phone = bool(re.search(phone_pattern, cv_text))
        
        return {
            'has_email': has_email,
            'has_phone': has_phone
        }
    
    def _calculate_quality_score(self, cv_text: str, validation_results: Dict) -> int:
        """Calculate CV quality score (0-100)"""
        score = 50  # Base score
        
        # Length score
        if 500 <= len(cv_text) <= 3000:
            score += 20
        elif 200 <= len(cv_text) <= 5000:
            score += 10
        
        # Deduct points for errors/warnings
        score -= len(validation_results['errors']) * 10
        score -= len(validation_results['warnings']) * 5
        
        # Add points for suggestions followed
        score += (3 - len(validation_results['suggestions'])) * 5
        
        return max(0, min(100, score))

cv_validator = CVValidator()
