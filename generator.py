#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Enhanced Response Generator
Implements: Grounded claims, structured output, concrete protocols
"""

from typing import List, Dict, Optional, Tuple
from transformers import pipeline
import torch
import re
from config import GENERATION_CONFIG, PASTEUR_QUOTE, PASTEUR_QUOTE_FRENCH

DEFAULT_PASTEUR_QUOTE = "Bernard was right. The microbe is nothing, the terrain is everything."
DEFAULT_PASTEUR_QUOTE_FRENCH = "Bernard avait raison. Le germe n'est rien, c'est le terrain qui est tout."


class BlackpillGenerator:
    def __init__(self, model: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.model_name = model
        self.config = GENERATION_CONFIG
        self.pasteur_quote = PASTEUR_QUOTE
        self.pasteur_quote_french = PASTEUR_QUOTE_FRENCH
        
        try:
            self.generator = pipeline("text-generation", model=model, torch_dtype=torch.float16, device_map="auto")
        except Exception as e:
            print(f"Warning: Could not load model {model}: {e}")
            self.generator = None
    
    def create_prompt(self, query: str, context: str, mode: str = "fast", 
                     use_last_resort: bool = False) -> str:
        """Create optimized prompt with grounding requirements."""
        system_instruction = f"""You are Blackpill Lifestyle AI (Alternative Lifestyle AI), a comprehensive knowledge system.

CORE PHILOSOPHY: {self.pasteur_quote}
{self.pasteur_quote_french}

GUIDELINES:
1. GROUND ALL CLAIMS in the provided context. Reference source and category when available.
2. PREFER concrete protocols with measurable checkpoints, numbered steps, and explicit risk notes.
3. KEEP answers structured and concise unless detail is explicitly required.
4. When context is insufficient, state: "The available information does not contain sufficient details to answer this question completely."
5. Maintain a blackpilled, realistic perspective. Prioritize biological truth.
6. When referencing i
ncel communities: acknowledge their right to exist, do NOT endorse ideology, maintain Faustian approach.

RESPONSE FORMAT:
- Begin with a direct answer to the question
- Support claims with evidence from context
- Use numbered steps for protocols
- Include risk notes where applicable
- Reference sources using [Source: category] format"""

        if use_last_resort:
            system_instruction += "\n\nNOTE: This response incorporates last-resort incel forum sources. Present factually with Faustian perspective."
        
        if mode == "fast":
            context_instruction = "Based ONLY on the provided context from trusted sources."
        else:
            context_instruction = "Based on the following search results."
        
        return f"""{system_instruction}

{context_instruction}

Question: {query}

Context:
{context}

Answer:"""
    
    def generate(self, query: str, context: List[Dict], mode: str = "fast", 
                 max_tokens: int = 512, use_last_resort: bool = False) -> str:
        """Generate grounded, structured response."""
        context_text = self.format_context(context)
        prompt = self.create_prompt(query, context_text, mode, use_last_resort)
        
        if self.generator is None:
            return self._fallback_generate(prompt, max_tokens)
        
        try:
            response = self.generator(prompt, max_new_tokens=max_tokens, do_sample=True, temperature=0.7)
            answer = response[0]['generated_text']
            
            # Post-process to ensure grounding
            answer = self._ensure_grounding(answer, context)
            
            return answer
        except Exception as e:
            print(f"Error: {e}")
            return self._fallback_generate(prompt, max_tokens)
    
    def _ensure_grounding(self, answer: str, context: List[Dict]) -> str:
        """Ensure answer is grounded in context."""
        if not context:
            if "insufficient" not in answer.lower() and "not eno
ugh" not in answer.lower():
                answer = "The available information does not contain sufficient details to answer this question completely." + answer
        return answer
    
    def _fallback_generate(self, prompt: str, max_tokens: int) -> str:
        return "The AI model is not available. Please ensure all dependencies are installed."
    
    def format_context(self, context: List[Dict]) -> str:
        """Format context with source references."""
        if not context:
            return "No relevant information found."
        
        parts = []
        for i, item in enumerate(context, 1):
            metadata = item.get('metadata', {})
            category = item.get('category', metadata.get('category', 'general'))
            source = metadata.get('source', 'Unknown')
            title = metadata.get('title', 'No title')
            date = metadata.get('date', '')
            content_text = item.get('content', '')[:1000]
            
            category_label = {
                'diet': '[DIET]', 'looksmaxxing': '[LOOKSMAXXING]', 
                'pharmacology': '[PHARMACOLOGY]', 'blackpill': '[BLACKPILL]',
                'adult_industry': '[ADULT INDUSTRY]', 'bimbofication': '[BIMBOFICATION]',
                'fitness': '[FITNESS]', 'research': '[RESEARCH]',
                'reddit': '[REDDIT]', 'wikipedia': '[WIKIPEDIA]'
            }.get(category, '[GENERAL]')
            
            date_str = f" ({date})" if date else ""
            parts.append(f"{category_label} Source {i} - {source}: {title}{date_str}
{content_text}

")
        
        return "\n".join(parts)    def generate_structured(self, query: str, context: List[Dict], mode: str = "fast",
                           max_tokens: int = 1024, use_last_resort: bool = False) -> Dict:
        """Generate structured response with grounding metadata."""
        context_text = self.format_context(context)
        prompt = self.create_prompt
(query, context_text, mode, use_last_resort)
        
        if self.generator is None:
            return {
                'answer': self._fallback_generate(prompt, max_tokens),
                'grounded': False,
                'sources': []
            }
        
        try:
            response = self.generator(prompt, max_new_tokens=max_tokens, do_sample=True, temperature=0.7)
            answer = response[0]['generated_text']
            
            # Extract referenced sources
            sources = self._extract_referenced_sources(answer, context)
            
            return {
                'answer': answer,
                'grounded': bool(context),
                'sources': sources,
                'used_last_resort': use_last_resort
            }
        except Exception as e:
            return {
                'answer': self._fallback_generate(prompt, max_tokens),
                'grounded': False,
                'sources': [],
                'used_last_resort': use_last_resort
            }
    
    def _extract_referenced_sources(self, answer: str, context: List[Dict]) -> List[Dict]:
        """Extract sources referenced in the answer."""
        sources = []
        for i, item in enumerate(context, 1):
            metadata = item.get('metadata', {})
            if f"Source {i}" in answer or metadata.get('title', '') in answer:
                sources.append({
                    'source': metadata.get('source', 'Unknown'),
                    'category': metadata.get('category', 'general'),
                    'title': metadata.get('title', '')
                })
        return sources
    
    def generate_protocol(self, query: str, context: List[Dict]) -> Dict:
        """Generate protocol-style response with checkpoints and risk notes."""
        result = self.generate_structured(query, context, max_tokens=1500)
        
        # Enhance with protocol formatting
        answer = result['answer']
        
        # Add protocol struc
ture if not present
        if "Step" not in answer and "Protocol" in query:
            answer = "PROTOCOL:

" + answer
        
        # Add risk notes section
        if "Risk" not in answer and "risk" not in answer.lower():
            answer += "

RISK NOTES: Consult with qualified professionals before implementing any protocol."
        
        result['answer'] = answer
        return result


if __name__ == "__main__":
    gen = BlackpillGenerator()
    print("Generator initialized with grounding and structured output")