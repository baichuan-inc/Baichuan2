from flask import Flask, request, jsonify
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig

app = Flask(__name__)

# Load the pre-trained model and tokenizer
model_name = "baichuan-inc/Baichuan2-13B-Chat"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
#这里的torch_dtype=torch.float16可改为torch_dtype=torch.bfloat16，仅支持30系及以上显卡
model.generation_config = GenerationConfig.from_pretrained(model_name)

@app.route('/v1/chat/completions', methods=['POST'])#URL: http://127.0.0.1:8000/v1/chat/completions
def chat_completion():
    try:
        # Parse incoming JSON data
        data = request.get_json()
        messages = data.get('messages', [])
        is_streaming = data.get('stream', False)

        # Check if streaming is enabled
        if is_streaming:#这里暂时只支持非流式输出
            return jsonify({"error": "Streaming is not supported."}), 400

        # Generate response using the model
        response_text = generate_response(messages)

        # Calculate token counts
        prompt_tokens = sum(len(tokenizer.encode(msg['content'])) for msg in messages)
        # 暂时不支持调节其他参数
        completion_tokens = len(response_text)
        total_tokens = prompt_tokens + completion_tokens

        # Build the response
        response_data = {
            "object": "chat.completion",
            "model": model_name,
            "choices": [{"message": {"role": "assistant", "content": response_text}, "index": 0, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            }
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_response(messages):
    # Generate response using the model
    response = model.chat(tokenizer, messages)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
