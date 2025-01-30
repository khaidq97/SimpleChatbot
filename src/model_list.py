    
MODEL_LIST = {
    "Ollama-Deepseek-R1-Distill-Qwen-1.5B": "deepseek-r1:1.5b",
    "Ollama-DeepSeek-R1-Distill-Qwen-7B": "deepseek-r1:7b",
    "Ollama-DeepSeek-R1-Distill-Llama-8B": "deepseek-r1:8b",
    "Ollama-DeepSeek-R1-Distill-Qwen-14B": "deepseek-r1:14b",
    
    "Ollama-Llama3.2-1B": "llama3.2:1b",
    "Ollama-Llama3.2-3B": "llama3.2:3b",
    
    "Ollama-Qwen2.5-0.5b": "qwen2.5:0.5b",
    "Ollama-Qwen2.5-1.5b": "qwen2.5:1.5b",
}

def get_model_list()->list[str]:
    return list(MODEL_LIST.keys())

def get_model_name(model_name: str)->str:
    return MODEL_LIST.get(model_name.strip(), "")