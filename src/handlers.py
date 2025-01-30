import asyncio
import time
from typing import AsyncGenerator
from gradio import ChatMessage
from .model_manager import model_manager
from .settings import STREAMING_SLEEP_TIME


async def model_change_handler(model_name: str) -> AsyncGenerator[str, None]:
    if not model_name or model_name == model_manager.model_name:
        return
    
    yield "⏳ Loading model..."
    status = await model_manager.load_model(model_name)
    yield status
    

async def chat_handler(message: str, history: list, model_name: any):
    if not model_name:
        yield [
            ChatMessage(
                content="⚠️ Please select a model first!",
                role="assistant",
                metadata={"status": "done", "is_error": True}
            )
        ]
        return
    
    if model_manager.is_loading:
        yield [
            ChatMessage(
                content="⚠️ Please wait until model finishes loading!",
                role="assistant",
                metadata={"status": "done", "is_error": True}
            )
        ]
        return
    
    if not model_manager.model_name:
        yield [
            ChatMessage(
                content="⚠️ Please select a model first!",
                role="assistant",
                metadata={"status": "done", "is_error": True}
            )
        ]
        return
    
    # Chat mode 
    stream = model_manager.chat(message, history)
    # thinking response
    thinking_message = ChatMessage(
            content="",
            role="assistant",
            metadata={
                'title': f'Thinking ...',
                'id': 0,
                'status': 'pending'
            }
        )
    
    yield [thinking_message]
    
    answer_response = ChatMessage(
        content="",
        role="assistant",
        metadata={"status": "done", "id": 1}
    )
    
    t1 = time.perf_counter()
    for chunk, is_thinking in stream:
        if is_thinking:
            thinking_message.content += chunk
            yield [thinking_message]
            await asyncio.sleep(STREAMING_SLEEP_TIME)
        else:
            thinking_message.metadata.update({
                "status": "done",
                "duration": time.perf_counter() - t1
            })
            answer_response.content += chunk
            yield [thinking_message,answer_response]
            await asyncio.sleep(STREAMING_SLEEP_TIME)  
    return
    
    