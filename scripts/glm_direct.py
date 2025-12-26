#!/usr/bin/env python3
"""
Direct GLM API integration - wrapper for glm_cli.py
Provides direct HTTP API access to Zhipu AI GLM models
"""

import os
import sys
import requests
from typing import Optional, Dict, Any

# Configuration
API_KEY = os.environ.get('GLM_API_KEY', '')
BASE_URL = 'https://api.z.ai/api/coding/paas/v4'
DEFAULT_MODEL = 'glm-4.5'


class GLMDirectAPI:
    """Direct GLM API caller for integration with coordinator"""

    def __init__(self, api_key: str = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or API_KEY
        self.model = model
        self.endpoint = f"{BASE_URL}/chat/completions"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def send_message(self, message: str, thinking_mode: bool = True,
                     max_tokens: int = 4096, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Send a message to GLM and get response

        Returns:
            Dict with keys: success (bool), output (str), error (str, if any)
        """
        if not self.api_key:
            return {
                'success': False,
                'error': 'GLM_API_KEY not set',
                'output': '',
                'command': 'glm_direct'
            }

        payload = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': message}
            ],
            'max_tokens': max_tokens,
            'temperature': temperature
        }

        if thinking_mode:
            payload['thinking'] = {'type': 'enabled'}

        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()

            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return {
                    'success': True,
                    'output': content,
                    'error': None,
                    'command': 'glm_direct'
                }
            else:
                return {
                    'success': False,
                    'error': 'Unexpected response format from GLM',
                    'output': str(result),
                    'command': 'glm_direct'
                }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'GLM API call timed out',
                'output': '',
                'command': 'glm_direct'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'GLM API request failed: {str(e)}',
                'output': '',
                'command': 'glm_direct'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'GLM API error: {str(e)}',
                'output': '',
                'command': 'glm_direct'
            }


def call_glm_direct(task_description: str, context_files: list = None,
                    model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """
    Main entry point for coordinator integration

    Args:
        task_description: The task/prompt to send to GLM
        context_files: Optional list of file paths to include as context
        model: Model to use (glm-4.5 or glm-4.5-air)

    Returns:
        Dict with success, output, error keys
    """
    if context_files is None:
        context_files = []

    # Build context from files
    context = ""
    if context_files:
        for file_path in context_files:
            try:
                from pathlib import Path
                full_path = Path(file_path)
                if full_path.exists():
                    with open(full_path, 'r', encoding='utf-8') as f:
                        context += f"\n\n=== {file_path} ===\n{f.read()}"
            except Exception as e:
                context += f"\n\n=== {file_path} (Error reading: {e}) ===\n"

    # Combine task and context
    full_prompt = f"{task_description}\n{context}" if context else task_description

    # Create API client and call
    client = GLMDirectAPI(model=model)
    return client.send_message(full_prompt)


def main():
    """CLI entry point for testing"""
    if len(sys.argv) < 2:
        print("Usage: python glm_direct.py 'prompt' [--model glm-4.5|glm-4.5-air]")
        sys.exit(1)

    prompt = sys.argv[1]
    model = DEFAULT_MODEL

    if len(sys.argv) > 2 and sys.argv[2] == '--model':
        model = sys.argv[3]

    result = call_glm_direct(prompt, model=model)

    if result['success']:
        print(result['output'])
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
