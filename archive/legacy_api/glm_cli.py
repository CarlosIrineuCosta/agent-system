#!/usr/bin/env python3
"""
GLM Coding Plan CLI Wrapper
A simple CLI tool to interact with GLM models using your coding plan subscription
"""

import os
import sys
import json
import requests
import argparse
from typing import Optional

# Configuration
API_KEY = os.environ.get('GLM_API_KEY', '')
BASE_URL = 'https://api.z.ai/api/coding/paas/v4'
DEFAULT_MODEL = 'glm-4.5'

class GLMCodingCLI:
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.api_key = api_key
        self.model = model
        self.endpoint = f"{BASE_URL}/chat/completions"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    
    def send_message(self, message: str, thinking_mode: bool = True) -> str:
        """Send a message to GLM and get response"""
        payload = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': message}
            ],
            'max_tokens': 4096,
            'temperature': 0.7
        }
        
        # Add thinking mode if enabled
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
            
            # Extract the response text
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                return "Error: Unexpected response format"
                
        except requests.exceptions.RequestException as e:
            return f"Error calling GLM API: {str(e)}"
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("GLM Coding Plan CLI - Interactive Mode")
        print(f"Model: {self.model}")
        print("Type 'exit' or 'quit' to end session")
        print("Type '/thinking on' or '/thinking off' to toggle thinking mode")
        print("-" * 50)
        
        thinking_mode = True
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                
                if user_input == '/thinking on':
                    thinking_mode = True
                    print("Thinking mode: ON")
                    continue
                
                if user_input == '/thinking off':
                    thinking_mode = False
                    print("Thinking mode: OFF")
                    continue
                
                if not user_input:
                    continue
                
                print("\nGLM: ", end='', flush=True)
                response = self.send_message(user_input, thinking_mode)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")

def main():
    parser = argparse.ArgumentParser(description='GLM Coding Plan CLI')
    parser.add_argument('prompt', nargs='?', help='Direct prompt (if not provided, enters interactive mode)')
    parser.add_argument('--model', default=DEFAULT_MODEL, choices=['glm-4.5', 'glm-4.5-air'], help='Model to use')
    parser.add_argument('--api-key', help='API key (or set GLM_API_KEY env var)')
    parser.add_argument('--no-thinking', action='store_true', help='Disable thinking mode')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or API_KEY
    if not api_key:
        print("Error: No API key provided. Set GLM_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    # Create CLI instance
    cli = GLMCodingCLI(api_key, args.model)
    
    # Run in appropriate mode
    if args.prompt:
        # Direct mode
        response = cli.send_message(args.prompt, not args.no_thinking)
        print(response)
    else:
        # Interactive mode
        cli.interactive_mode()

if __name__ == '__main__':
    main()
