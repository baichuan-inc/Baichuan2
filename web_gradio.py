from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from peft import PeftModel
import torch
import gradio as gr

model_path = "./baichuan-inc/Baichuan2-13B-Chat-4bits"
lora_path = './baichuan-inc/baichuan2-13b-iepile-lora'


def init_model():
    """
    初始化 LLM
    """
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )
    model.generation_config = GenerationConfig.from_pretrained(
        model_path,
    )
    model = PeftModel.from_pretrained(
        model,
        lora_path,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        use_fast=False,
        trust_remote_code=True
    )
    return model, tokenizer


def chat_with_model(message, history, max_length, top_p, temperature):
    """
    处理用户输入并与模型进行交互，生成回复，并更新聊天界面
    """
    # 自定义 Config
    model.generation_config.max_new_tokens = max_length
    model.generation_config.top_p = top_p
    model.generation_config.temperature = temperature

    #  LLM 消息历史
    model_history = []
    for conver in history:
        model_history.append({"role": "user", "content": conver[0]})
        model_history.append({"role": "assistant", "content": conver[1]})
    model_history.append({"role": "user", "content": message})

    # 通过 LLM 流式处理
    for response in model.chat(tokenizer, model_history, stream=True):
        # 通过生成器返回，允许界面动态更新
        yield response


# 标题
js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';

    var text = 'Baichuan 2';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 50);
            }, i * 250);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""

# 设置 Gradio 界面
with gr.Blocks(js=js, theme="soft") as demo:
    # 初始化 LLM
    model, tokenizer = init_model()

    with gr.Row():
        with gr.Column(scale=2):
            max_length = gr.Slider(0, 4096, value=2048, step=1.0, label="Maximum length", interactive=True)
            top_p = gr.Slider(0, 1, value=0.7, step=0.01, label="Top P", interactive=True)
            temperature = gr.Slider(0, 1, value=0.95, step=0.01, label="Temperature", interactive=True)
        with gr.Column(scale=8):
            chat = gr.ChatInterface(
                textbox=gr.Textbox(placeholder="Ask me a question", scale=8, render=False),
                fn=chat_with_model,
                additional_inputs=[max_length, top_p, temperature],
                # 创建聊天机器人组件
                chatbot=gr.Chatbot(
                    label="Agent",
                    avatar_images=[
                        None,
                        "https://em-content.zobj.net/source/twitter/53/robot-face_1f916.png",
                    ],
                    show_copy_button=True,
                    render=False,
                ),
                examples=[["Hello"], ["What is a prime number?"], ["Please implement the code for quick sort."]],
                retry_btn="Retry",
                undo_btn="Delete",
                clear_btn="Clear",
            ).queue()

demo.launch(share=True, inbrowser=False)