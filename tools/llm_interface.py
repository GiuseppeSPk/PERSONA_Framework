import os
import abc
import json
import time
from typing import Optional

# Tries to import SDKs, handles missing dependencies gracefully
try:
    import openai
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    import requests
except ImportError:
    requests = None

class LLMProvider(abc.ABC):
    """Abstract base class for LLM providers."""
    
    @abc.abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        pass

class MockProvider(LLMProvider):
    """Mock provider for testing without API costs."""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return f"[MOCK OUTPUT]\nSystem: {len(system_prompt)} chars\nPrompt: {len(prompt)} chars"

class OllamaProvider(LLMProvider):
    """Provider for local Ollama models."""
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not requests:
            raise ImportError("requests library is required for Ollama provider")
        
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get('response', '')
        except Exception as e:
            return f"Error calling Ollama: {e}"

class OpenAIProvider(LLMProvider):
    """Provider for OpenAI models (GPT-4, etc.)"""
    def __init__(self, model_name: str = "gpt-4o", api_key: Optional[str] = None):
        if not OpenAI:
            raise ImportError("openai library is not installed")
        
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {e}"

class AnthropicProvider(LLMProvider):
    """Provider for Anthropic models (Claude 3, etc.)"""
    def __init__(self, model_name: str = "claude-3-opus-20240229", api_key: Optional[str] = None):
        if not Anthropic:
            raise ImportError("anthropic library is not installed")
        
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            # Anthropic system prompts are top-level parameters
            response = self.client.messages.create(
                model=self.model_name,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4096,
                temperature=0.7
            )
            return response.content[0].text
        except Exception as e:
            return f"Error calling Anthropic: {e}"

def get_provider(provider_type: str, model_name: str) -> LLMProvider:
    """Factory function to get the requested provider."""
    provider_type = provider_type.lower()
    
    if provider_type == "mock":
        return MockProvider()
    elif provider_type == "ollama":
        return OllamaProvider(model_name=model_name)
    elif provider_type == "openai":
        return OpenAIProvider(model_name=model_name)
    elif provider_type == "anthropic":
        return AnthropicProvider(model_name=model_name)
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")
