from typing import Any, Generator
from .ollama_model import OllamaModel

class ModelManager:
    model_name: Any | None = None
    is_loading: bool = False
    
    def __init__(self):
        self.ollama_model = OllamaModel()
    
    async def load_model(self, model_name: str) -> None:
        try:
            self.is_loading = True
            
            self.ollama_model.load_model(model_name)
            
            self.model_name = model_name
            self.is_loading = False
            return f"✅ {model_name} loaded successfully!"
        except Exception as e:
            self.is_loading = False
            self.model_name = None
            return f"❌ Error loading {model_name}: {e}"
        
    def chat(self, message: str, history: list) -> Generator:
        stream = self.ollama_model.chat(
            model_name=self.model_name,
            message=message,
            history=history
        )
        return stream
        
model_manager = ModelManager()