"""
Enhanced Country Detection Module for HR Advisor
Implements multiple techniques for intelligent country detection from user queries
"""

import re
from typing import Optional, Dict, List, Tuple

class CountryDetector:
    def __init__(self):
        # Comprehensive country patterns with aliases, demonyms, and common variations
        self.country_patterns = {
            'SG': {
                'names': ['singapore', 'sg', 'republic of singapore'],
                'demonyms': ['singaporean', 'singaporeans'],
                'cities': ['singapore city', 'jurong', 'tampines', 'woodlands', 'bedok'],
                'currency': ['sgd', 'singapore dollar'],
                'organizations': ['mom', 'ministry of manpower', 'cpf', 'iras']
            },
            'US': {
                'names': ['united states', 'usa', 'us', 'america', 'united states of america'],
                'demonyms': ['american', 'americans'],
                'cities': ['new york', 'los angeles', 'chicago', 'houston', 'phoenix', 'philadelphia', 'san antonio', 'san diego', 'dallas', 'san jose'],
                'currency': ['usd', 'dollar', 'dollars'],
                'organizations': ['dol', 'department of labor', 'eeoc', 'osha', 'nlrb', 'flsa', 'fmla']
            },
            'UK': {
                'names': ['united kingdom', 'uk', 'britain', 'great britain', 'england', 'scotland', 'wales', 'northern ireland'],
                'demonyms': ['british', 'english', 'scottish', 'welsh'],
                'cities': ['london', 'manchester', 'birmingham', 'leeds', 'glasgow', 'liverpool', 'newcastle', 'sheffield', 'bristol', 'edinburgh'],
                'currency': ['gbp', 'pound', 'pounds', 'sterling'],
                'organizations': ['acas', 'hmrc', 'hse', 'gov.uk', 'dwp']
            },
            'AU': {
                'names': ['australia', 'au', 'commonwealth of australia'],
                'demonyms': ['australian', 'australians', 'aussie', 'aussies'],
                'cities': ['sydney', 'melbourne', 'brisbane', 'perth', 'adelaide', 'gold coast', 'newcastle', 'canberra'],
                'currency': ['aud', 'australian dollar'],
                'organizations': ['fair work', 'ato', 'asic', 'accc']
            },
            'CA': {
                'names': ['canada', 'ca'],
                'demonyms': ['canadian', 'canadians'],
                'cities': ['toronto', 'montreal', 'vancouver', 'calgary', 'edmonton', 'ottawa', 'winnipeg', 'quebec city'],
                'currency': ['cad', 'canadian dollar'],
                'organizations': ['cra', 'service canada', 'labour canada']
            },
            'DE': {
                'names': ['germany', 'deutschland', 'de', 'federal republic of germany'],
                'demonyms': ['german', 'germans'],
                'cities': ['berlin', 'hamburg', 'munich', 'cologne', 'frankfurt', 'stuttgart', 'düsseldorf', 'dortmund'],
                'currency': ['eur', 'euro'],
                'organizations': ['bundesagentur für arbeit', 'arbeitsrecht']
            },
            'FR': {
                'names': ['france', 'fr', 'french republic'],
                'demonyms': ['french'],
                'cities': ['paris', 'marseille', 'lyon', 'toulouse', 'nice', 'nantes', 'strasbourg', 'montpellier'],
                'currency': ['eur', 'euro'],
                'organizations': ['pole emploi', 'urssaf', 'code du travail']
            },
            'IN': {
                'names': ['india', 'bharat', 'republic of india'],
                'demonyms': ['indian', 'indians'],
                'cities': ['mumbai', 'delhi', 'bangalore', 'hyderabad', 'ahmedabad', 'chennai', 'kolkata', 'pune'],
                'currency': ['inr', 'rupee', 'rupees'],
                'organizations': ['epfo', 'esic', 'labour ministry', 'pf', 'esi']
            },
            'JP': {
                'names': ['japan', 'nippon', 'nihon'],
                'demonyms': ['japanese'],
                'cities': ['tokyo', 'osaka', 'yokohama', 'nagoya', 'sapporo', 'fukuoka', 'kobe', 'kyoto'],
                'currency': ['jpy', 'yen'],
                'organizations': ['mhlw', 'hello work', 'labour standards']
            },
            'CN': {
                'names': ['china', 'prc', 'peoples republic of china'],
                'demonyms': ['chinese'],
                'cities': ['beijing', 'shanghai', 'guangzhou', 'shenzhen', 'tianjin', 'wuhan', 'dongguan', 'chengdu'],
                'currency': ['cny', 'yuan', 'rmb'],
                'organizations': ['mohrss', 'social insurance']
            },
            'MY': {
                'names': ['malaysia'],
                'demonyms': ['malaysian', 'malaysians'],
                'cities': ['kuala lumpur', 'george town', 'ipoh', 'shah alam', 'petaling jaya', 'johor bahru'],
                'currency': ['myr', 'ringgit'],
                'organizations': ['epf', 'socso', 'hrdf', 'mohr']
            },
            'TH': {
                'names': ['thailand', 'siam'],
                'demonyms': ['thai'],
                'cities': ['bangkok', 'chiang mai', 'phuket', 'pattaya', 'hat yai'],
                'currency': ['thb', 'baht'],
                'organizations': ['mol', 'social security office']
            },
            'PH': {
                'names': ['philippines', 'ph'],
                'demonyms': ['filipino', 'filipinos', 'philippine'],
                'cities': ['manila', 'quezon city', 'davao', 'cebu', 'zamboanga'],
                'currency': ['php', 'peso', 'pesos'],
                'organizations': ['dole', 'sss', 'philhealth', 'pag-ibig']
            },
            'ID': {
                'names': ['indonesia'],
                'demonyms': ['indonesian', 'indonesians'],
                'cities': ['jakarta', 'surabaya', 'bandung', 'medan', 'semarang'],
                'currency': ['idr', 'rupiah'],
                'organizations': ['bpjs', 'kemnaker', 'disnaker']
            },
            'VN': {
                'names': ['vietnam', 'viet nam'],
                'demonyms': ['vietnamese'],
                'cities': ['ho chi minh city', 'hanoi', 'da nang', 'can tho', 'bien hoa'],
                'currency': ['vnd', 'dong'],
                'organizations': ['molisa', 'social insurance']
            },
            'NZ': {
                'names': ['new zealand', 'nz', 'aotearoa'],
                'demonyms': ['new zealander', 'kiwi', 'kiwis'],
                'cities': ['auckland', 'wellington', 'christchurch', 'hamilton', 'tauranga'],
                'currency': ['nzd', 'new zealand dollar'],
                'organizations': ['mbie', 'ird', 'acc']
            },
            'HK': {
                'names': ['hong kong', 'hk', 'hongkong'],
                'demonyms': ['hong konger', 'hongkonger'],
                'cities': ['central', 'tsim sha tsui', 'causeway bay', 'wan chai'],
                'currency': ['hkd', 'hong kong dollar'],
                'organizations': ['labour department', 'mpf', 'ird']
            }
        }
        
        # HR-specific context patterns
        self.hr_context_patterns = {
            'employment_law': ['employment law', 'labor law', 'labour law', 'employment act', 'labor code', 'labour code'],
            'leave_policies': ['maternity leave', 'paternity leave', 'annual leave', 'sick leave', 'vacation days'],
            'working_time': ['working hours', 'overtime', 'work week', 'maximum hours', 'break time'],
            'termination': ['notice period', 'severance', 'termination', 'dismissal', 'redundancy'],
            'benefits': ['pension', 'retirement', 'health insurance', 'social security', 'provident fund'],
            'compliance': ['minimum wage', 'workplace safety', 'discrimination', 'harassment', 'equal opportunity']
        }
        
        # Cross-country terminology mapping - detects when users mix terms from different countries
        self.terminology_conflicts = {
            # Retirement/Pension Systems
            'superannuation': {
                'origin_country': 'AU',
                'origin_term': 'Superannuation Guarantee',
                'country_equivalents': {
                    'SG': 'Central Provident Fund (CPF)',
                    'US': '401(k) and Social Security',
                    'UK': 'Workplace Pension and State Pension',
                    'MY': 'Employees Provident Fund (EPF)',
                    'HK': 'Mandatory Provident Fund (MPF)',
                    'CA': 'Canada Pension Plan (CPP) and Registered Retirement Savings Plan (RRSP)',
                    'NZ': 'KiwiSaver'
                }
            },
            'cpf': {
                'origin_country': 'SG',
                'origin_term': 'Central Provident Fund (CPF)',
                'country_equivalents': {
                    'AU': 'Superannuation Guarantee',
                    'US': '401(k) and Social Security',
                    'UK': 'Workplace Pension and State Pension',
                    'MY': 'Employees Provident Fund (EPF)',
                    'HK': 'Mandatory Provident Fund (MPF)',
                    'CA': 'Canada Pension Plan (CPP) and RRSP',
                    'NZ': 'KiwiSaver'
                }
            },
            'epf': {
                'origin_country': 'MY',
                'origin_term': 'Employees Provident Fund (EPF)',
                'country_equivalents': {
                    'SG': 'Central Provident Fund (CPF)',
                    'AU': 'Superannuation Guarantee',
                    'US': '401(k) and Social Security',
                    'UK': 'Workplace Pension and State Pension',
                    'HK': 'Mandatory Provident Fund (MPF)',
                    'CA': 'Canada Pension Plan (CPP) and RRSP',
                    'NZ': 'KiwiSaver'
                }
            },
            '401k': {
                'origin_country': 'US',
                'origin_term': '401(k) retirement plan',
                'country_equivalents': {
                    'SG': 'Central Provident Fund (CPF)',
                    'AU': 'Superannuation Guarantee',
                    'UK': 'Workplace Pension and State Pension',
                    'MY': 'Employees Provident Fund (EPF)',
                    'HK': 'Mandatory Provident Fund (MPF)',
                    'CA': 'Canada Pension Plan (CPP) and RRSP',
                    'NZ': 'KiwiSaver'
                }
            },
            # Leave terminology
            'holiday': {
                'origin_country': 'UK',
                'origin_term': 'Holiday entitlement',
                'country_equivalents': {
                    'US': 'Vacation days or Paid Time Off (PTO)',
                    'SG': 'Annual leave',
                    'AU': 'Annual leave',
                    'CA': 'Vacation leave',
                    'NZ': 'Annual holidays'
                }
            },
            'vacation': {
                'origin_country': 'US',
                'origin_term': 'Vacation days',
                'country_equivalents': {
                    'UK': 'Holiday entitlement',
                    'SG': 'Annual leave',
                    'AU': 'Annual leave',
                    'CA': 'Vacation leave',
                    'NZ': 'Annual holidays'
                }
            },
            # Employment terminology
            'redundancy': {
                'origin_country': 'UK',
                'origin_term': 'Redundancy',
                'country_equivalents': {
                    'US': 'Layoff or termination',
                    'SG': 'Retrenchment',
                    'AU': 'Redundancy',
                    'CA': 'Layoff',
                    'NZ': 'Redundancy'
                }
            },
            'layoff': {
                'origin_country': 'US',
                'origin_term': 'Layoff',
                'country_equivalents': {
                    'UK': 'Redundancy',
                    'SG': 'Retrenchment',
                    'AU': 'Redundancy',
                    'CA': 'Layoff',
                    'NZ': 'Redundancy'
                }
            },
            'retrenchment': {
                'origin_country': 'SG',
                'origin_term': 'Retrenchment',
                'country_equivalents': {
                    'UK': 'Redundancy',
                    'US': 'Layoff or termination',
                    'AU': 'Redundancy',
                    'CA': 'Layoff',
                    'NZ': 'Redundancy'
                }
            }
        }

    def detect_country_from_query(self, query: str) -> Tuple[Optional[str], float, Dict]:
        """
        Enhanced but conservative country detection with confidence scoring and metadata
        
        Returns:
            Tuple of (country_code, confidence_score, metadata)
        """
        query_lower = query.lower().strip()
        
        # Initialize detection results
        detection_results = []
        metadata = {
            'detection_methods': [],
            'matched_patterns': [],
            'hr_context': [],
            'ambiguous_matches': [],
            'requires_clarification': False
        }
        
        # Method 1: Direct country name matching (highest confidence)
        direct_matches = self._detect_direct_country_mentions(query_lower)
        if direct_matches:
            detection_results.extend(direct_matches)
            metadata['detection_methods'].append('direct_mention')
        
        # Method 2: City-based detection (lower confidence, may be ambiguous)
        city_matches = self._detect_by_cities(query_lower)
        if city_matches:
            detection_results.extend(city_matches)
            metadata['detection_methods'].append('city_based')
        
        # Method 3: Currency-based detection (medium confidence)
        currency_matches = self._detect_by_currency(query_lower)
        if currency_matches:
            detection_results.extend(currency_matches)
            metadata['detection_methods'].append('currency_based')
        
        # Method 4: Organization/law-based detection (high confidence but needs verification)
        org_matches = self._detect_by_organizations(query_lower)
        if org_matches:
            detection_results.extend(org_matches)
            metadata['detection_methods'].append('organization_based')
        
        # Method 5: Cross-country terminology conflict detection
        terminology_conflicts = self._detect_terminology_conflicts(query_lower)
        if terminology_conflicts:
            metadata['terminology_conflicts'] = terminology_conflicts
            metadata['detection_methods'].append('terminology_conflict')
            # Don't add to detection_results as this requires clarification
        
        # Method 6: HR context analysis
        hr_context = self._analyze_hr_context(query_lower)
        metadata['hr_context'] = hr_context
        
        # Aggregate and score results
        if not detection_results:
            return None, 0.0, metadata
        
        # Count occurrences and calculate confidence
        country_scores = {}
        for country, score, pattern in detection_results:
            if country not in country_scores:
                country_scores[country] = {'total_score': 0, 'patterns': []}
            country_scores[country]['total_score'] += score
            country_scores[country]['patterns'].append(pattern)
            metadata['matched_patterns'].append(f"{country}: {pattern}")
        
        # Find best match
        best_country = max(country_scores.keys(), key=lambda k: country_scores[k]['total_score'])
        best_score = country_scores[best_country]['total_score']
        
        # Conservative confidence calculation - be more cautious
        confidence = min(best_score / 3.0, 0.85)  # Max confidence is 0.85 to encourage clarification
        
        # Check for ambiguous matches (more conservative threshold)
        sorted_countries = sorted(country_scores.items(), key=lambda x: x[1]['total_score'], reverse=True)
        if len(sorted_countries) > 1 and sorted_countries[1][1]['total_score'] >= best_score * 0.5:
            metadata['ambiguous_matches'] = [country for country, _ in sorted_countries[:3]]
            metadata['requires_clarification'] = True
            confidence = min(confidence, 0.6)  # Reduce confidence for ambiguous cases
        
        # Special handling for potentially ambiguous terms
        if any('cpf' in pattern.lower() or 'epf' in pattern.lower() or 'superannuation' in pattern.lower() 
               for pattern in metadata['matched_patterns']):
            confidence = min(confidence, 0.7)  # Be more conservative with retirement terms
            metadata['requires_clarification'] = True
        
        return best_country, confidence, metadata

    def _detect_direct_country_mentions(self, query: str) -> List[Tuple[str, float, str]]:
        """Detect direct mentions of country names"""
        matches = []
        for country_code, patterns in self.country_patterns.items():
            for name in patterns['names']:
                if re.search(r'\b' + re.escape(name) + r'\b', query):
                    matches.append((country_code, 2.0, f"country_name:{name}"))
            for demonym in patterns['demonyms']:
                if re.search(r'\b' + re.escape(demonym) + r'\b', query):
                    matches.append((country_code, 1.5, f"demonym:{demonym}"))
        return matches

    def _detect_by_cities(self, query: str) -> List[Tuple[str, float, str]]:
        """Detect countries by city mentions"""
        matches = []
        for country_code, patterns in self.country_patterns.items():
            for city in patterns['cities']:
                if re.search(r'\b' + re.escape(city) + r'\b', query):
                    matches.append((country_code, 1.0, f"city:{city}"))
        return matches

    def _detect_by_currency(self, query: str) -> List[Tuple[str, float, str]]:
        """Detect countries by currency mentions"""
        matches = []
        for country_code, patterns in self.country_patterns.items():
            for currency in patterns['currency']:
                if re.search(r'\b' + re.escape(currency) + r'\b', query):
                    matches.append((country_code, 1.5, f"currency:{currency}"))
        return matches

    def _detect_by_organizations(self, query: str) -> List[Tuple[str, float, str]]:
        """Detect countries by organization/law mentions"""
        matches = []
        for country_code, patterns in self.country_patterns.items():
            for org in patterns['organizations']:
                if re.search(r'\b' + re.escape(org) + r'\b', query):
                    matches.append((country_code, 1.8, f"organization:{org}"))
        return matches

    def _detect_terminology_conflicts(self, query: str) -> List[Dict]:
        """Detect cross-country terminology conflicts"""
        conflicts = []
        for term, conflict_info in self.terminology_conflicts.items():
            if re.search(r'\b' + re.escape(term) + r'\b', query):
                conflicts.append({
                    'term': term,
                    'origin_country': conflict_info['origin_country'],
                    'origin_term': conflict_info['origin_term'],
                    'equivalents': conflict_info['country_equivalents']
                })
        return conflicts

    def _analyze_hr_context(self, query: str) -> List[str]:
        """Analyze HR context in the query"""
        contexts = []
        for context_type, patterns in self.hr_context_patterns.items():
            for pattern in patterns:
                if pattern in query:
                    contexts.append(context_type)
                    break
        return contexts

    def get_country_suggestions(self, query: str) -> List[Dict[str, str]]:
        """Get country suggestions based on query context"""
        suggestions = []
        
        # Common countries for HR queries
        common_countries = ['SG', 'US', 'UK', 'AU', 'CA', 'MY', 'HK']
        
        for country_code in common_countries:
            country_info = self.country_patterns.get(country_code, {})
            country_name = country_info.get('names', [country_code])[0].title()
            suggestions.append({
                'code': country_code,
                'name': country_name
            })
        
        return suggestions

    def generate_clarification_response(self, query: str, detected_country: Optional[str] = None, 
                                      confidence: float = 0.0, metadata: Dict = None) -> str:
        """
        Generate a conservative clarification response that asks for confirmation
        rather than making assumptions
        """
        if metadata is None:
            metadata = {}
        
        # Handle terminology conflicts first
        terminology_conflicts = metadata.get('terminology_conflicts', [])
        if terminology_conflicts:
            conflict = terminology_conflicts[0]  # Handle the first conflict
            term = conflict['term']
            origin_country = conflict['origin_country']
            origin_term = conflict['origin_term']
            equivalents = conflict['equivalents']
            
            # Check if a specific country is mentioned in the query
            query_lower = query.lower()
            mentioned_country = None
            for country_code, patterns in self.country_patterns.items():
                for name in patterns['names']:
                    if name in query_lower:
                        mentioned_country = country_code
                        break
                if mentioned_country:
                    break
            
            if mentioned_country and mentioned_country in equivalents:
                # User is asking about term X in country Y, but term X is from country Z
                mentioned_country_name = self.country_patterns[mentioned_country]['names'][0].title()
                origin_country_name = self.country_patterns[origin_country]['names'][0].title()
                equivalent_term = equivalents[mentioned_country]
                
                return f"I notice you're asking about \"{term.upper()}\" in {mentioned_country_name}. However, \"{origin_term}\" is actually the {origin_country_name} term.\n\nIn {mentioned_country_name}, the equivalent system is called \"{equivalent_term}\".\n\nWould you like me to provide information about {equivalent_term} in {mentioned_country_name}?"
            
            # General terminology conflict without specific country
            return f"I notice you're asking about \"{term.upper()}\". This term is primarily used in {self.country_patterns[origin_country]['names'][0].title()} where it refers to \"{origin_term}\".\n\nDifferent countries have different systems:\n" + \
                   "\n".join([f"• {self.country_patterns[code]['names'][0].title()}: {equiv}" 
                             for code, equiv in list(equivalents.items())[:4]]) + \
                   f"\n\nCould you please specify which country you're interested in so I can provide accurate information?"
        
        # Handle regular country detection with conservative approach
        if detected_country and confidence > 0.4:
            country_info = self.country_patterns.get(detected_country, {})
            country_name = country_info.get('names', [detected_country])[0].title()
            
            ambiguous_matches = metadata.get('ambiguous_matches', [])
            if ambiguous_matches:
                other_countries = []
                for code in ambiguous_matches:
                    if code != detected_country:
                        other_info = self.country_patterns.get(code, {})
                        other_name = other_info.get('names', [code])[0].title()
                        other_countries.append(other_name)
                
                if other_countries:
                    return f"I detected you might be asking about {country_name}, but your query could also apply to {', '.join(other_countries[:2])}. Could you please confirm which country you're interested in?\n\nThis will help me provide accurate, country-specific information for your question: \"{query}\""
            
            return f"I detected you might be asking about {country_name}. Is this correct?\n\nIf not, please specify the country you're interested in so I can provide accurate, country-specific information for: \"{query}\""
        
        # If we have some suggestions but low confidence
        suggestions = self.get_country_suggestions(query)
        
        base_response = f"I'd be happy to help with your question: \"{query}\"\n\nHowever, employment laws vary significantly by country. Could you please specify which country you're asking about?"
        
        if suggestions:
            base_response += "\n\nBased on your query, you might be interested in:\n"
            for suggestion in suggestions[:3]:
                base_response += f"• {suggestion['name']}\n"
        
        base_response += "\nFor example:\n"
        base_response += "• \"What is the maternity leave policy in Singapore?\"\n"
        base_response += "• \"Tell me about overtime laws in the United States\"\n"
        base_response += "• \"What are the notice periods in the United Kingdom?\"\n"
        base_response += "\nThis will help me provide you with accurate, country-specific information."
        
        return base_response
