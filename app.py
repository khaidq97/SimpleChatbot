import gradio as gr
from src.handlers import model_change_handler, chat_handler
from src.model_list import get_model_list
from src.settings import BOT_AVATAR, FAVICON, USER_AVATAR

head = """
<script>
    setTimeout(function() {
        document.title = "Simple Local Chatbot";
    }, 100);
</script>
"""

with gr.Blocks(head=head) as app:
    # gr.Markdown("# Please choose the model you want to use")
    with gr.Row():
        model_selector = gr.Dropdown(
            choices=get_model_list(),
            value=None,
            label="Select Model",
            interactive=True
        )
        status = gr.Textbox(label="Status", interactive=False)
    
    chatbot = gr.Chatbot(
        height=700,
        avatar_images=(
            USER_AVATAR,  # User Avatar
            BOT_AVATAR    # Bot Avatar
        ),
        render=True,
        type="messages"
    )
    
    model_selector.change(
        model_change_handler,
        inputs=model_selector,
        outputs=status
    )
    
    chat_interface = gr.ChatInterface(
        chat_handler,
        chatbot=chatbot,
        examples=[
            ["What can you do ?"],
            ["Explain quantum computing simply"],
            ["What is the meaning of life ?"],
            ["Tell me a joke"],
            ["Can you code the snake game"],
        ],
        # title="Chat Interface 🤔",
        additional_inputs=[model_selector]
    )
    
app.queue(
    default_concurrency_limit=5,  # The number of requests that can be processed concurrently
    max_size=100,         # The maximum number of requests that can be queued
    api_open=False        # Offer the option to open the API
).launch(
    inbrowser=True,
    share=False,
    favicon_path=FAVICON       
)