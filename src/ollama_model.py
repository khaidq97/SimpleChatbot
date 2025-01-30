from typing import Generator
import re
import ollama
from ollama import chat
from .model_list import get_model_name

def extract_think_content(text):
    think_pattern = re.search(r'<think>(.*?)</think>', text, re.DOTALL)
    think_content = think_pattern.group(1).strip() if think_pattern else ""
    remaining_content = re.sub(r'<think>.*?</think>', "", text, flags=re.DOTALL).strip()
    return think_content, remaining_content

class OllamaModel:
    downloaded_models = [model.model for model in ollama.list().models]
    
    def load_model(self, model_name: str):
        _model_name = get_model_name(model_name)
        if not _model_name:
            raise ValueError(f"Model {model_name} not found!")
        
        if _model_name not in self.downloaded_models:
            # Pull the model from the server
            ollama.pull(_model_name)
        return 
    
    def chat(self, model_name: str, message: str, history: list) -> Generator:
        _messages = []
        for _message in history:
            _messages += [
                {"role": _message['role'], "content": _message['content']}
            ]
        
        # Add the user message
        _messages += [{"role": "user", "content": message}]
        stream = chat(
            model=get_model_name(model_name),
            messages=_messages,
            stream=True
        )
        is_thinking = False
        for chunk in stream:
            chunk_content = chunk['message']['content']
            if chunk_content == "<think>":
                is_thinking = True
                continue
            
            if is_thinking:
                if chunk_content == "</think>":
                    is_thinking = False
                else:
                    yield chunk_content, True
                    continue
                
            yield chunk_content, False