#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Response Generator
Internally: Blackpill Lifestyle AI
"""

from typing import List, Dict
from transformers import pipeline
import torch

DEFAULT_PASTEUR_QUOTE = "Bernard was right. The microbe is nothing, the terrain is everything."
DEFAULT_PASTEUR_QUOTE_FRENCH = "Bernard avait raison. Le germe n'est rien, c'est le terrain qui est tout."


class BlackpillGenerator:
    def __init__(self, model: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.model_name = model
        try:
            from config import TERRAIN_THEORY_PRIORITY, PASTEUR_QUOTE, PASTEUR_QUOTE_FRENCH
            self.terrain_priority = TERRAIN_THEORY_PRIORITY
            self.pasteur_quote = PASTEUR_QUOTE
            self.pasteur_quote_french = PASTEUR_QUOTE_FRENCH
        except:
            self.terrain_priority = True
            self.pasteur_quote = DEFAULT_PASTEUR_QUOTE
            self.pasteur_quote_french = DEFAULT_PASTEUR_QUOTE_FRENCH
        
        try:
            self.generator = pipeline("text-generation", model=model, torch_dtype=torch.float16, device_map="auto")
        except Exception as e:
            print(f"Warning: Could not load model {model}: {e}")
            self.generator = None
    
    def create_prompt(self, query: str, context: str, mode: str = "fast", use_last_resort: bool = False):
        system_instruction = f"""You are Blackpill Lifestyle AI (Alternative Lifestyle AI), a comprehensive knowledge system specializing in:
- Alternative Diet & Nutrition (primal, carnivore, raw food, terrain theory)
- Looksmaxxing & Physical Optimization (facial, body, surgical, non-surgical)
- Pharmacology & Performance Enhancement (nootropics, steroids, experimental compounds)
- Blackpill Philosophy & Manosphere Analysis (genetics, social dynamics, incel theory)
- Adult Industry Intelligence (AVN Awards, performer analysis, industry trends)

CORE PHILOSOPHY: {self.pasteur_quote}
{self.pasteur_quote_french}

Always maintain a blackpilled, realistic perspective. Prioritize biological truth over social narratives. When discussing health, emphasize terrain theory. When discussing appearance, be brutally honest about genetic limitations and optimization strategies. When discussing pharmacology, focus on evidence-based effects and risks.

Respond professionally but without sugar-coating. Use direct, unambiguous language.

IMPORTANT: When referencing incel communities (incels.is, schaduw.net):
- Acknowledge their right to exist and express their perspectives
- Do NOT promote or endorse incel ideology
- Maintain a Faustian approach: acknowledge the struggle but emphasize the attempt to improve rather than giving up
- Frame discussions in terms of self-improvement and realistic assessment
- Never be pro-incel, but be factual about their documented experiences"""

        if use_last_resort:
            system_instruction += "\n\nNOTE: This response incorporates information from last-resort incel forum sources. Present this information factually while maintaining the Faustian perspective of attempting improvement despite genetic limitations."
        
        if mode == "fast":
            context_instruction = "Based ONLY on the provided context from trusted sources."
        else:
            context_instruction = "Based on the following search results."
        
        return f"""{system_instruction}

{context_instruction}
If the context doesn't contain sufficient information, state this clearly.

Question: {query}

Context:
{context}

Answer:"""
    
    def generate(self, query: str, context: List[Dict], mode: str = "fast", max_tokens: int = 512, use_last_resort: bool = False):
        context_text = self.format_context(context)
        prompt = self.create_prompt(query, context_text, mode, use_last_resort=use_last_resort)
        
        if self.generator is None:
            return self._fallback_generate(prompt, max_tokens)
        
        try:
            response = self.generator(prompt, max_new_tokens=max_tokens, do_sample=True, temperature=0.7)
            return response[0]['generated_text']
        except Exception as e:
            print(f"Error: {e}")
            return self._fallback_generate(prompt, max_tokens)
    
    def _fallback_generate(self, prompt: str, max_tokens: int):
        return "I apologize, but the AI model is not currently available. Please ensure all dependencies are installed."
    
    def format_context(self, context: List[Dict]) -> str:
        if not context:
            return "No relevant information found."
        parts = []
        for i, item in enumerate(context, 1):
            metadata = item.get('metadata', {})
            category = item.get('category', metadata.get('category', 'general'))
            source = metadata.get('source', 'Unknown')
            title = metadata.get('title', 'No title')
            content = item.get('content', '')[:1000]
            category_label = {
                'diet': '[DIET]', 'looksmaxxing': '[LOOKSMAXXING]', 'pharmacology': '[PHARMACOLOGY]',
                'blackpill': '[BLACKPILL]', 'adult_industry': '[ADULT INDUSTRY]',
                'bimbofication': '[BIMBOFICATION]', 'fitness': '[FITNESS]', 'research': '[RESEARCH]',
                'reddit': '[REDDIT]', 'wikipedia': '[WIKIPEDIA]'
            }.get(category, '[GENERAL]')
            parts.append(f"{category_label} Source {i} - {source}: {title}\n{content}\n")
        return "\n".join(parts)


if __name__ == "__main__":
    gen = BlackpillGenerator()
    print("Generator initialized")