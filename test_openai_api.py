import importlib.util
import sys
import types
import unittest
from pathlib import Path


class _Tokenizer:
    def encode(self, text):
        return text.split()


def load_api():
    torch = types.ModuleType("torch")
    torch.float16 = "float16"
    sys.modules["torch"] = torch

    transformers = types.ModuleType("transformers")
    transformers.AutoTokenizer = types.SimpleNamespace(from_pretrained=lambda *args, **kwargs: _Tokenizer())
    transformers.AutoModelForCausalLM = types.SimpleNamespace(
        from_pretrained=lambda *args, **kwargs: types.SimpleNamespace(generation_config=None, chat=lambda *a, **k: "")
    )
    sys.modules["transformers"] = transformers

    generation = types.ModuleType("transformers.generation")
    utils = types.ModuleType("transformers.generation.utils")
    utils.GenerationConfig = types.SimpleNamespace(from_pretrained=lambda *args, **kwargs: None)
    sys.modules["transformers.generation"] = generation
    sys.modules["transformers.generation.utils"] = utils

    flask = types.ModuleType("flask")

    class _App:
        def route(self, *args, **kwargs):
            return lambda fn: fn

    flask.Flask = lambda *args, **kwargs: _App()
    flask.request = None
    flask.jsonify = lambda payload: payload
    sys.modules["flask"] = flask

    path = Path(__file__).resolve().parent / "OpenAI_api.py"
    spec = importlib.util.spec_from_file_location("openai_api", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CompletionTokenTest(unittest.TestCase):
    def test_completion_tokens_count_tokens(self):
        api = load_api()
        prompt_tokens, completion_tokens, total_tokens = api.count_usage(
            [{"content": "hi there"}],
            "hello world",
        )
        self.assertEqual(prompt_tokens, 2)
        self.assertEqual(completion_tokens, 2)
        self.assertEqual(total_tokens, 4)


if __name__ == "__main__":
    unittest.main()
