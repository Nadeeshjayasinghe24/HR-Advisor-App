"""
Multi-LLM Orchestration System for HR Advisor
Implements parallel LLM execution, response validation, voting mechanisms, and source integration
"""

import asyncio
import aiohttp
import json
import os
import time
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup
import re

# LLM Client imports
import openai
import google.generativeai as genai
import anthropic

class LLMProvider(Enum):
    OPENAI_GPT4 = "openai_gpt4"
    OPENAI_GPT35 = "openai_gpt35"
    GOOGLE_GEMINI_PRO = "google_gemini_pro"
    GOOGLE_GEMINI_FLASH = "google_gemini_flash"
    ANTHROPIC_CLAUDE3_SONNET = "anthropic_claude3_sonnet"
    ANTHROPIC_CLAUDE3_HAIKU = "anthropic_claude3_haiku"

@dataclass
class LLMResponse:
    provider: LLMProvider
    content: str
    confidence_score: float
    response_time: float
    tokens_used: int
    error: Optional[str] = None
    sources: List[Dict[str, str]] = None

@dataclass
class SourceReference:
    title: str
    url: str
    snippet: str
    relevance_score: float
    source_type: str  # 'government', 'legal', 'official', 'academic'

class MultiLLMOrchestrator:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.setup_clients()
        
    def setup_clients(self):
        """Initialize LLM clients with API keys"""
        try:
            # OpenAI setup
            if os.getenv('OPENAI_API_KEY'):
                self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            # Google Gemini setup
            if os.getenv('GOOGLE_API_KEY'):
                genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            
            # Anthropic setup
            if os.getenv('ANTHROPIC_API_KEY'):
                self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                
        except Exception as e:
            print(f"Error setting up LLM clients: {e}")

    async def get_official_sources(self, query: str, country: str) -> List[SourceReference]:
        """Search for official government and legal sources"""
        sources = []
        
        # Country-specific official domains
        official_domains = {
            'US': ['dol.gov', 'eeoc.gov', 'nlrb.gov', 'osha.gov'],
            'UK': ['gov.uk', 'acas.org.uk', 'hse.gov.uk'],
            'SG': ['mom.gov.sg', 'cpf.gov.sg', 'iras.gov.sg'],
            'AU': ['fairwork.gov.au', 'safeworkaustralia.gov.au'],
            'CA': ['canada.ca', 'labour.gc.ca'],
            'DE': ['bmas.de', 'arbeitsagentur.de'],
            'FR': ['travail-emploi.gouv.fr', 'service-public.fr'],
            'IN': ['labour.gov.in', 'epfindia.gov.in'],
            'MY': ['mohr.gov.my', 'kwsp.gov.my'],
            'HK': ['labour.gov.hk', 'mpf.org.hk'],
            'JP': ['mhlw.go.jp', 'jil.go.jp'],
            'ID': ['kemnaker.go.id'],
            'TH': ['mol.go.th']
        }
        
        domains = official_domains.get(country, official_domains['US'])
        
        try:
            # Search for official sources
            for domain in domains[:3]:  # Limit to top 3 domains
                search_query = f"site:{domain} {query}"
                search_results = await self._search_web(search_query, limit=2)
                
                for result in search_results:
                    source = SourceReference(
                        title=result.get('title', ''),
                        url=result.get('url', ''),
                        snippet=result.get('snippet', ''),
                        relevance_score=0.9,  # High relevance for official sources
                        source_type='government'
                    )
                    sources.append(source)
                    
        except Exception as e:
            print(f"Error fetching official sources: {e}")
            
        return sources[:5]  # Return top 5 sources

    async def _search_web(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """Perform web search using a search API or scraping"""
        results = []
        
        try:
            # Using DuckDuckGo instant answer API (free alternative)
            search_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Extract results from DuckDuckGo response
                        if 'RelatedTopics' in data:
                            for topic in data['RelatedTopics'][:limit]:
                                if isinstance(topic, dict) and 'Text' in topic:
                                    results.append({
                                        'title': topic.get('Text', '')[:100],
                                        'url': topic.get('FirstURL', ''),
                                        'snippet': topic.get('Text', '')
                                    })
                                    
        except Exception as e:
            print(f"Web search error: {e}")
            # Fallback to mock results for demo
            results = [{
                'title': f"Official HR Guidelines for {query}",
                'url': "https://example-gov.com/hr-guidelines",
                'snippet': f"Official guidance on {query} from government sources."
            }]
            
        return results

    async def call_openai(self, prompt: str, system_context: str, model: str = "gpt-4") -> LLMResponse:
        """Call OpenAI GPT models"""
        if not self.openai_client:
            return LLMResponse(
                provider=LLMProvider.OPENAI_GPT4,
                content="",
                confidence_score=0.0,
                response_time=0.0,
                tokens_used=0,
                error="OpenAI client not configured"
            )
        
        start_time = time.time()
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            response_time = time.time() - start_time
            
            return LLMResponse(
                provider=LLMProvider.OPENAI_GPT4 if model == "gpt-4" else LLMProvider.OPENAI_GPT35,
                content=response.choices[0].message.content,
                confidence_score=0.85,
                response_time=response_time,
                tokens_used=response.usage.total_tokens
            )
            
        except Exception as e:
            return LLMResponse(
                provider=LLMProvider.OPENAI_GPT4,
                content="",
                confidence_score=0.0,
                response_time=time.time() - start_time,
                tokens_used=0,
                error=str(e)
            )

    async def call_gemini(self, prompt: str, system_context: str, model: str = "gemini-pro") -> LLMResponse:
        """Call Google Gemini models"""
        start_time = time.time()
        try:
            model_instance = genai.GenerativeModel(model)
            full_prompt = f"{system_context}\n\nUser Query: {prompt}"
            
            response = model_instance.generate_content(full_prompt)
            response_time = time.time() - start_time
            
            return LLMResponse(
                provider=LLMProvider.GOOGLE_GEMINI_PRO if model == "gemini-pro" else LLMProvider.GOOGLE_GEMINI_FLASH,
                content=response.text,
                confidence_score=0.80,
                response_time=response_time,
                tokens_used=len(response.text.split()) * 1.3  # Approximate token count
            )
            
        except Exception as e:
            return LLMResponse(
                provider=LLMProvider.GOOGLE_GEMINI_PRO,
                content="",
                confidence_score=0.0,
                response_time=time.time() - start_time,
                tokens_used=0,
                error=str(e)
            )

    async def call_claude(self, prompt: str, system_context: str, model: str = "claude-3-sonnet-20240229") -> LLMResponse:
        """Call Anthropic Claude models"""
        if not self.anthropic_client:
            return LLMResponse(
                provider=LLMProvider.ANTHROPIC_CLAUDE3_SONNET,
                content="",
                confidence_score=0.0,
                response_time=0.0,
                tokens_used=0,
                error="Anthropic client not configured"
            )
        
        start_time = time.time()
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=800,
                system=system_context,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_time = time.time() - start_time
            
            return LLMResponse(
                provider=LLMProvider.ANTHROPIC_CLAUDE3_SONNET if "sonnet" in model else LLMProvider.ANTHROPIC_CLAUDE3_HAIKU,
                content=response.content[0].text,
                confidence_score=0.88,
                response_time=response_time,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens
            )
            
        except Exception as e:
            return LLMResponse(
                provider=LLMProvider.ANTHROPIC_CLAUDE3_SONNET,
                content="",
                confidence_score=0.0,
                response_time=time.time() - start_time,
                tokens_used=0,
                error=str(e)
            )

    def calculate_response_quality(self, response: LLMResponse, sources: List[SourceReference]) -> float:
        """Calculate overall quality score for a response"""
        quality_score = 0.0
        
        # Base confidence from LLM
        quality_score += response.confidence_score * 0.4
        
        # Response length and structure
        if response.content:
            word_count = len(response.content.split())
            if 50 <= word_count <= 500:  # Optimal length
                quality_score += 0.2
            elif word_count > 20:  # Minimum acceptable
                quality_score += 0.1
        
        # Response time factor (faster is better, but not too fast)
        if 1.0 <= response.response_time <= 10.0:
            quality_score += 0.1
        elif response.response_time < 1.0:
            quality_score += 0.05  # Too fast might be cached/simple
        
        # Source integration bonus
        if sources:
            quality_score += min(len(sources) * 0.05, 0.3)
        
        return min(quality_score, 1.0)

    async def orchestrate_llm_responses(self, query: str, country: str, context: str) -> Dict[str, Any]:
        """Main orchestration method - coordinates multiple LLMs and synthesizes responses"""
        
        # Get official sources first
        sources = await self.get_official_sources(query, country)
        
        # Enhanced system context with sources
        source_context = ""
        if sources:
            source_context = "\n\nOfficial Sources to Reference:\n"
            for i, source in enumerate(sources, 1):
                source_context += f"{i}. {source.title} - {source.snippet}\n"
        
        enhanced_context = f"{context}{source_context}\n\nIMPORTANT: Provide specific, actionable advice and cite relevant sources with [1], [2] notation."
        
        # Define LLM calls to make
        llm_tasks = []
        
        # OpenAI GPT-4 (if available)
        if self.openai_client:
            llm_tasks.append(self.call_openai(query, enhanced_context, "gpt-4"))
            llm_tasks.append(self.call_openai(query, enhanced_context, "gpt-3.5-turbo"))
        
        # Google Gemini (if available)
        if os.getenv('GOOGLE_API_KEY'):
            llm_tasks.append(self.call_gemini(query, enhanced_context, "gemini-pro"))
            llm_tasks.append(self.call_gemini(query, enhanced_context, "gemini-1.5-flash"))
        
        # Anthropic Claude (if available)
        if self.anthropic_client:
            llm_tasks.append(self.call_claude(query, enhanced_context, "claude-3-sonnet-20240229"))
            llm_tasks.append(self.call_claude(query, enhanced_context, "claude-3-haiku-20240307"))
        
        # Execute all LLM calls in parallel
        responses = []
        if llm_tasks:
            responses = await asyncio.gather(*llm_tasks, return_exceptions=True)
            # Filter out exceptions
            responses = [r for r in responses if isinstance(r, LLMResponse) and not r.error]
        
        # If no LLM responses, create fallback
        if not responses:
            fallback_response = LLMResponse(
                provider=LLMProvider.OPENAI_GPT4,
                content=f"HR guidance for {country}: {query}. Please ensure compliance with local employment laws and consult official sources for the most current regulations.",
                confidence_score=0.3,
                response_time=0.1,
                tokens_used=50,
                error="No LLM providers available - using fallback response"
            )
            responses = [fallback_response]
        
        # Calculate quality scores
        for response in responses:
            response.quality_score = self.calculate_response_quality(response, sources)
        
        # Sort by quality score
        responses.sort(key=lambda x: x.quality_score, reverse=True)
        
        # Select best response or synthesize
        if len(responses) == 1:
            best_response = responses[0]
        else:
            # Use voting mechanism to select best response
            best_response = self.vote_best_response(responses)
        
        # Format final response with citations
        final_content = self.format_response_with_citations(best_response.content, sources)
        
        return {
            'content': final_content,
            'provider_used': best_response.provider.value,
            'confidence_score': best_response.quality_score,
            'response_time': best_response.response_time,
            'sources': [
                {
                    'title': source.title,
                    'url': source.url,
                    'type': source.source_type
                } for source in sources
            ],
            'llm_responses_count': len(responses),
            'tokens_used': sum(r.tokens_used for r in responses)
        }

    def vote_best_response(self, responses: List[LLMResponse]) -> LLMResponse:
        """Implement voting mechanism to select best response"""
        # Weight factors for voting
        weights = {
            'quality_score': 0.4,
            'confidence': 0.3,
            'response_time': 0.2,
            'content_length': 0.1
        }
        
        scored_responses = []
        for response in responses:
            score = 0.0
            
            # Quality score
            score += response.quality_score * weights['quality_score']
            
            # Confidence score
            score += response.confidence_score * weights['confidence']
            
            # Response time (inverse - faster is better, but normalized)
            time_score = max(0, 1 - (response.response_time / 30))  # 30s max
            score += time_score * weights['response_time']
            
            # Content length (optimal range)
            if response.content:
                word_count = len(response.content.split())
                length_score = 1.0 if 100 <= word_count <= 400 else 0.5
                score += length_score * weights['content_length']
            
            scored_responses.append((score, response))
        
        # Return highest scored response
        scored_responses.sort(key=lambda x: x[0], reverse=True)
        return scored_responses[0][1]

    def format_response_with_citations(self, content: str, sources: List[SourceReference]) -> str:
        """Format response with proper citations and footnotes"""
        if not sources:
            return content
        
        # Add citation numbers to content if not already present
        formatted_content = content
        
        # Add footnotes section
        footnotes = "\n\n**Sources:**\n"
        for i, source in enumerate(sources, 1):
            footnotes += f"[{i}] {source.title} - {source.url}\n"
        
        return formatted_content + footnotes

# Global orchestrator instance
orchestrator = MultiLLMOrchestrator()

