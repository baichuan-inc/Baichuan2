<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->

<div align="center">
<h1>
  Baichuan2
</h1>
</div>

<p align="center">
🤗 <a href="https://huggingface.co/baichuan-inc/" target="_blank">Hugging Face</a> • 🤖 <a href="https://modelscope.cn/organization/baichuan-inc" target="_blank">ModelScope</a> • 💬 <a href="https://github.com/baichuan-inc/Baichuan2/blob/main/media/wechat.jpeg?raw=true" target="_blank">WeChat</a>
</p>

<div align="center">

[![license](https://img.shields.io/github/license/modelscope/modelscope.svg)](https://github.com/baichuan-inc/Baichuan2/blob/main/LICENSE)
<h4 align="center">
    <p>
        <b>中文</b> |
        <a href="https://github.com/baichuan-inc/Baichuan2/blob/main/README_EN.md">English</a>
    <p>
</h4>
</div>

# 目录

- [介绍](#介绍)
- [Benchmark结果](#Benchmark-结果)
- [模型细节](#模型细节)
- [推理和部署](#推理和部署)
- [应用案例](#应用案例)
- [对模型进行微调](#对模型进行微调)
- [历史 checkpoint](#历史-checkpoint)
- [社区支持](#社区支持)
- [声明](#声明)
- [协议](#协议)

# 介绍

Baichuan2 是由百川智能继 Baichuan-7B 和 Baichuan-13B 之后做出的更新版本，采用 2.6 万亿  Tokens 的高质量语料训练，在权威的中文和英文 benchmark 上均取得同尺寸最好的效果。本次发布包含有 7B、13B 的 Base 和 Chat 版本，并提供了 Chat 版本的 4bits 量化，所有版本不仅对学术研究完全开放，开发者也仅需邮件申请并获得官方商用许可后，即可以免费商用。具体发布版本和下载见下表：
|         | 基座模型  | 对齐模型 | 对齐模型 4bits 量化 |
|:-------:|:-------:|:-------:|:-----------------:|
| 7B      | [Baichuan2-7B-Base](https://huggingface.co/baichuan-inc/Baichuan2-7B-Base) |[Baichuan2-7B-Chat](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat) |[Baichuan2-7B-Chat-4bits](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat-4bits) |
| 13B     | [Baichuan2-13B-Base](https://huggingface.co/baichuan-inc/Baichuan2-13B-Base) |[Baichuan2-13B-Chat](https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat) |[Baichuan2-13B-Chat-4bits](https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat-4bits) |


# Benchmark 结果
updating @ chengwei



# 推理和部署

推理所需的模型权重、源码、配置已发布在 Hugging Face，下载链接见本文档最开始的表格。下面以 Baichuan2-13B-Chat 为例示范多种推理方式。程序会自动从 Hugging Face 下载所需资源。

推理前请安装依赖：
```shell
pip install -r requirements.txt
```

## Python代码方式

```python
>>> import torch
>>> from transformers import AutoModelForCausalLM, AutoTokenizer
>>> from transformers.generation.utils import GenerationConfig
>>> tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan2-13B-Chat", use_fast=False, trust_remote_code=True)
>>> model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-13B-Chat", device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)
>>> model.generation_config = GenerationConfig.from_pretrained("baichuan-inc/Baichuan2-13B-Chat")
>>> messages = []
>>> messages.append({"role": "user", "content": "世界上第二高的山峰是哪座"})
>>> response = model.chat(tokenizer, messages)
>>> print(response)
TODO 改一个新的case
```

> 在上述代码中，模型加载指定 `device_map='auto'`，会使用所有可用显卡。如需指定使用的设备，可以使用类似 `export CUDA_VISIBLE_DEVICES=0,1`（使用了0、1号显卡）的方式控制。


## 命令行工具方式

```shell
python cli_demo.py
```
最后输出示例如下：

<p align="center">
    <img src="media/cn-cli.png" width="70%"/>
</p>

## 网页 demo 方式

依靠streamlit运行以下命令，会在本地启动一个 web 服务，把控制台给出的地址放入浏览器即可访问。

```shell
streamlit run web_demo.py
```

效果如下：

<p align="center">
    <img src="media/cn-web.gif" width="70%"/>
</p>

## Baichuan-13B-Chat 示例输出

<details><summary><b>内容创作</b></summary>

```
用户：

```

</details>

<details><summary><b>广告文案</b></summary>
  
```
用户：
```

</details>

<details><summary><b>精准问答</b></summary>

```
用户：
世界上第二高的山是什么山
```

</details>

<details><summary><b>语言理解</b></summary>

```
用户：
```
</details>


## 推理性能
Baichuan-13B 使用了 ALiBi 线性偏置技术，相对于 Rotary Embedding 计算量更小，对推理性能有显著提升；与标准的 LLaMA-13B 相比，平均推理速度 (tokens/s) 实测提升 31.6%：

| Model       | tokens/s |
|-------------|:--------:|
| LLaMA-13B   | ？？     |
| Baichuan-13B| ？？    |

> 测试环境和参数：GPU A100-SXM4-80G, PyTorch 2.0.0+cu117, transformers 4.29.1, batch size = 1, 生成长度 = 2048, 精度 fp16, 基于 Baichuan-13B-Base


## 量化部署

为了让不同的用户以及不同的平台都能运行Baichuan2模型，我们针对Baichuan2模型做了相应地量化工作(包括Baichuan2-7B-Chat和Baichuan2-13B-Chat)，方便用户快速高效地在自己的平台部署Baichuan2模型。

### 量化方法

Baichuan2的量化方法采用社区主流的量化方法：[BitsAndBytes方法](https://github.com/TimDettmers/bitsandbytes)。该方法可以保证量化后的效果基本不掉点，目前已经集成到transformers库里，并在社区得到了广泛应用。BitsAndBytes支持4bits和8bits两种量化，其中4bits支持FP4和NF4两种格式，Baichuan2选用NF4作为4bit量化的数据类型。  
  
基于该量化方法，Baichuan2支持在线量化和离线量化两种模式。

### 在线量化

对于在线量化，我们支持8bits和4bits量化，使用方式和[Baichuan-13B](https://huggingface.co/baichuan-inc/Baichuan-13B-Chat)方式类似，只需要先加载模型到CPU的内存里，再调用一个quantize接口量化，最后调用cuda()函数，将量化后的权重拷贝到GPU显存中。实现整个模型加载的代码非常简单，我们以Baichuan2-7B-Chat为例：  
8bits在线量化:
```python
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", torch_dtype=torch.float16, trust_remote_code=True)
model = model.quantize(8).cuda() 
```
4bits在线量化:
```python
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", torch_dtype=torch.float16, trust_remote_code=True)
model = model.quantize(4).cuda() 
```
需要注意的是，在用from_pretrained接口的时候，用户一般会加上device_map = "auto"，在使用在线量化时，需要去掉这个参数，否则会报错。

### 离线量化
为了方便用户的使用，我们提供了离线量化好的4bits的版本[Baichuan2-7B-Chat-4bits](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat-4bits/tree/main)，供用户下载。
用户加载Baichuan2-7B-Chat-4bits模型很简单，只需要执行:
```python
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat-4bits", device_map="auto", trust_remote_code=True)
```
对于8bits离线量化，我们没有提供相应的版本，因为HuggingFace transformers库提供了相应的API接口，可以很方便的实现8bits量化模型的保存和加载。用户可以自行按照如下方式实现8bits的模型保存和加载：
```python
#模型保存，其中model_id为原始模型目录，quant8_saved_dir为8bits量化后的模型保存目录
model = AutoModelForCausalLM.from_pretrained(model_id, load_in_8bit=True, device_map="auto", trust_remote_code=True)
model.save_pretrained(quant8_saved_dir)

#模型加载
model = AutoModelForCausalLM.from_pretrained(quant8_saved_dir, device_map="auto", trust_remote_code=True)
```
### 量化效果
量化前后显存占用对比：
| Precision   | Baichuan2-7B GPU Mem (GB) |Baichuan2-13B GPU Mem (GB) |
|-------------|:------------:|:------------:|
| bf16 / fp16 | 14.0         | 25.9       |
| 8bits        | 8.0         | 14.2        |
| 4bits        | 5.1          | 8.6        |

量化后在各个 benchmark 上的结果和原始版本对比如下：

| Model 5-shot           | C-Eval | MMLU | CMMLU |
|------------------------|:------:|:----:|:-----:|
| Baichuan2-13B-Chat      | 56.74  | 57.32| 59.68  |
| Baichuan2-13B-Chat-4bits | 56.05   | 56.24 | 58.82  |
| Baichuan2-7B-Chat       | 54.35   | 52.93 | 54.99  |
| Baichuan2-7B-Chat-4bits | 53.04   | 51.72 | 52.84  |

可以看到，4bits相对bfloat16掉点在1~2个点左右。

## CPU部署
Baichuan2模型支持CPU推理，但需要强调的是，CPU的推理速度相对较慢。需按如下方式修改模型加载的方式：
```python
#以Baichuan2-7B-Chat为例
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", torch_dtype=torch.float32, trust_remote_code=True)
```
## Baichuan2 相对 Baichuan 推理迁移
由于很多用户在 Baichuan(Baichuan-7B, Baichuan-13B)上做了很多优化的工作，例如编译优化、量化等，为了将这些工作零成本地应用于 Baichuan2，用户可以对 Baichuan2 模型做一个离线转换，转换后就可以当做 Baichuan 模型来使用。具体来说，用户只需要利用以下脚本离线对 Baichuan2 模型的最后一层lm_head做归一化，并替换掉”lm_head.weight“即可。替换完后，就可以像对 Baichuan 模型一样对转换后的模型做编译优化等工作了。
```python
import torch
import os
ori_model_dir = 'your baichuan2 model directory'
# 为了不覆盖原始模型，最好将转换后的模型save到另一个目录再替换
new_model_dir = 'your normalized lm_head weight baichuan2 model directory'
model = torch.load(os.path.join(ori_model_dir, 'pytorch_model.bin'))
lm_head_w = model['lm_head.weight']
lm_head_w = torch.nn.functional.normalize(lm_head_w)
model['lm_head.weight'] = lm_head_w
torch.save(model, os.path.join(new_model_dir, 'pytorch_model.bin'))
```

# 应用案例

# 对模型进行微调

## 依赖安装
```shell
git clone https://github.com/baichuan-inc/Baichuan2.git
cd Baichuan2/fine-tune
pip install -r requirements.txt
```
- 如需使用 LoRA 等轻量级微调方法需额外安装 [peft](https://github.com/huggingface/peft)
- 如需使用 xFormers 进行训练加速需额外安装 [xFormers](https://github.com/facebookresearch/xformers)

## 单机训练

下面我们给一个微调 Baichuan2-7B-Base 的单机训练例子。

训练数据：`data/belle_chat_ramdon_10k.json`，该样例数据是从 [multiturn_chat_0.8M](https://huggingface.co/datasets/BelleGroup/multiturn_chat_0.8M) 采样出 1 万条，并且做了格式转换。主要是展示多轮数据怎么训练，不保证效果。


```shell
hostfile=""
deepspeed --hostfile=$hostfile fine-tune.py  \
    --report_to "none" \
    --data_path "data/belle_chat_ramdon_10k.json" \
    --model_name_or_path "baichuan-inc/Baichuan2-7B-Base" \
    --output_dir "output" \
    --model_max_length 512 \
    --num_train_epochs 4 \
    --per_device_train_batch_size 16 \
    --gradient_accumulation_steps 1 \
    --save_strategy epoch \
    --learning_rate 2e-5 \
    --lr_scheduler_type constant \
    --adam_beta1 0.9 \
    --adam_beta2 0.98 \
    --adam_epsilon 1e-8 \
    --max_grad_norm 1.0 \
    --weight_decay 1e-4 \
    --warmup_ratio 0.0 \
    --logging_steps 1 \
    --gradient_checkpointing True \
    --deepspeed ds_config.json \
    --bf16 True \
    --tf32 True
```

## 多机训练

多机训练只需要给一下 hostfile ，内容如下：
```
ip1 slots=8
ip2 slots=8
ip3 slots=8
ip4 slots=8
```
同时在训练脚本里面指定 hosftfile 的路径：
```shell
hostfile="/path/to/hostfile"
deepspeed --hostfile=$hostfile fine-tune.py  \
    --report_to "none" \
    --data_path "data/belle_chat_ramdon_10k.json" \
    --model_name_or_path "baichuan-inc/Baichuan2-7B-Base" \
    --output_dir "output" \
    --model_max_length 512 \
    --num_train_epochs 4 \
    --per_device_train_batch_size 16 \
    --gradient_accumulation_steps 1 \
    --save_strategy epoch \
    --learning_rate 2e-5 \
    --lr_scheduler_type constant \
    --adam_beta1 0.9 \
    --adam_beta2 0.98 \
    --adam_epsilon 1e-8 \
    --max_grad_norm 1.0 \
    --weight_decay 1e-4 \
    --warmup_ratio 0.0 \
    --logging_steps 1 \
    --gradient_checkpointing True \
    --deepspeed ds_config.json \
    --bf16 True \
    --tf32 True
```

## 轻量化微调

代码已经支持轻量化微调如 LoRA，如需使用仅需在上面的脚本中加入以下参数
```shell
--use_lora True
```
LoRA 具体的配置可见 fine-tune.py 脚本。
使用 LoRA 微调后可以使用下面的命令加载模型
```python
from peft import AutoPeftModelForCausalLM
model = AutoPeftModelForCausalLM.from_pretrained("output", trust_remote_code=True)
```

# 历史 checkpoint
我们提供了 Baichuan2-7B-Base 模型的 10 个历史 checkpoint（[下载地址](http://hugging-face.co/baichuan-inc/Baichuan-7B-Base)），供研究使用。

# 社区支持

## 华为昇腾
**昇腾NPU微调**：Baichuan2 支持基于昇腾 NPU 的 PyTorch + DeepSpeed 模型微调，微调所需的 modeling、README、示例脚本已发布：[7B](https://gitee.com/ascend/ModelZoo-PyTorch/tree/master/PyTorch/built-in/foundation/Baichuan2/7B)。13B 支持正在开发中。

**昇腾NPU部署**：Baichuan2 支持昇腾 NPU 推理，推理所需的 modeling、README、示例脚本已发布：[7B](https://gitee.com/ascend/ModelZoo-PyTorch/tree/master/ACL_PyTorch/built-in/foundation_models/baichuan2/7b)、[13B](https://gitee.com/ascend/ModelZoo-PyTorch/tree/master/ACL_PyTorch/built-in/foundation_models/baichuan2/13b)。

**MindFormers套件**：[MindFormers](https://gitee.com/mindspore/mindformers) 是构建一个基于昇思框架(MindSpore)大模型训练、微调、评估、推理、部署的全流程开发套件，当前集成了[Baichuan2](https://gitee.com/mindspore/mindformers/tree/dev/research/baichuan2)，支持用户进行模型部署、微调训练和创新研发。

**大模型体验平台**：[昇思大模型平台](https://xihe.mindspore.cn) 基于昇思 MindSpore AI 框架、MindFormers 大模型开发套件与昇腾硬件算力，将 [Baichuan2-7B](https://xihe.mindspore.cn/modelzoo/baichuan) 大模型能力开放给公众，欢迎大家使用。


# 声明

我们在此声明，我们的开发团队并未基于 Baichuan2 模型开发任何应用，无论是在 iOS、Android、网页或任何其他平台。我们强烈呼吁所有使用者，不要利用 Baichuan2 模型进行任何危害国家社会安全或违法的活动。另外，我们也要求使用者不要将 Baichuan2 模型用于未经适当安全审查和备案的互联网服务。我们希望所有的使用者都能遵守这个原则，确保科技的发展能在规范和合法的环境下进行。

我们已经尽我们所能，来确保模型训练过程中使用的数据的合规性。然而，尽管我们已经做出了巨大的努力，但由于模型和数据的复杂性，仍有可能存在一些无法预见的问题。因此，如果由于使用 Baichuan2 开源模型而导致的任何问题，包括但不限于数据安全问题、公共舆论风险，或模型被误导、滥用、传播或不当利用所带来的任何风险和问题，我们将不承担任何责任。

# 协议
对本仓库源码的使用遵循开源许可协议 [Apache 2.0](https://github.com/baichuan-inc/Baichuan-13B/blob/main/LICENSE)。对 Baichuan2 模型的社区使用见[《Baichuan2 模型社区许可协议》](https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat/resolve/main/Baichuan2%20%E6%A8%A1%E5%9E%8B%E7%A4%BE%E5%8C%BA%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE.pdf)。Baichuan2 支持商用。如果将 Baichuan2 模型或其衍生品用作商业用途，请您按照如下方式联系许可方，以进行登记并向许可方申请书面授权：联系邮箱 <opensource@baichuan-inc.com>。
