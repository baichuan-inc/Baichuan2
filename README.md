<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->

<div align="center">
<h1>
  Baichuan2
</h1>
</div>

<p align="center">
🤗 <a href="https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat" target="_blank">Hugging Face</a> • 🤖 <a href="https://modelscope.cn/organization/baichuan-inc" target="_blank">ModelScope</a> • 💬 <a href="https://github.com/baichuan-inc/Baichuan2/blob/main/media/wechat.jpeg?raw=true" target="_blank">WeChat</a>
</p>

<div align="center">

[![license](https://img.shields.io/github/license/modelscope/modelscope.svg)](https://github.com/baichuan-inc/Baichuan-7B/blob/main/LICENSE)
<h4 align="center">
    <p>
        <b>中文</b> |
        <a href="https://github.com/baichuan-inc/Baichuan2/blob/main/README_EN.md">English</a>
    <p>
</h4>
</div>

# 目录

- [介绍](#介绍)
- [Benchmark结果](#Benchmark结果)
- [模型细节](#模型细节)
- [推理和部署](#推理和部署)
- [应用案例](#应用案例)
- [对模型进行微调](#对模型进行微调)
- [社区支持](#社区支持)
- [声明](#声明)
- [协议](#协议)

# 介绍

# Benchmark结果

# 推理和部署

推理前请安装依赖：
```shell
pip install -r requirements.txt
```
## 量化部署

为了让不同的用户以及不同的平台都能运行Baichuan2模型，我们针对Baichuan2模型做了相应地量化工作(包括Baichuan2-7B-Chat和Baichuan2-13B-Chat)，方便用户快速高效地在自己的平台部署Baichuan2模型。

### 量化方法

Baichuan2的量化方法采用社区主流的量化方法：[BitsAndBytes方法](https://github.com/TimDettmers/bitsandbytes)。该方法可以保证量化后的效果基本不掉点，目前已经集成到transformers库里，并在社区得到了广泛应用。BitsAndBytes支持int4和int8两种量化，其中int4支持FP4和NF4两种格式，Baichuan2选用NF4作为4bit量化的数据类型。  
  
基于该量化方法，Baichuan2支持在线量化和离线量化两种模式。

### 在线量化

对于在线量化，我们支持int8和int4量化，使用方式和[Baichuan-13B](https://huggingface.co/baichuan-inc/Baichuan-13B-Chat)方式类似，只需要先加载模型到CPU的内存里，再调用一个quantize接口量化，最后调用cuda()函数，将量化后的权重拷贝到GPU显存中。实现整个模型加载的代码非常简单，我们以Baichuan2-7B-Chat为例：  
int8在线量化:
```python
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", torch_dtype=torch.float16, trust_remote_code=True)
model = model.quantize(8).cuda() 
```
int4在线量化:
```python
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", torch_dtype=torch.float16, trust_remote_code=True)
model = model.quantize(4).cuda() 
```
需要注意的是，在用from_pretrained接口的时候，用户一般会加上device_map = "auto"，在使用在线量化时，需要去掉这个参数，否则会报错。

### 离线量化
为了方便用户的使用，我们提供了离线量化好的int4的版本[Baichuan2-7B-Chat-int4](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat-int4/tree/main)，供用户下载。
用户加载Baichuan2-7B-Chat-int4模型很简单，只需要执行:
```python
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat-int4", device_map="auto", trust_remote_code=True)
```
对于int8离线量化，我们没有提供相应的版本，因为HuggingFace transformers库提供了相应的API接口，可以很方便的实现int8量化模型的保存和加载。用户可以自行按照如下方式实现int8的模型保存和加载：
```python
#模型保存，其中model_id为原始模型目录，quant8_saved_dir为int8量化后的模型保存目录
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
| int8        | 8.0         | 14.2        |
| int4        | 5.1          | 8.6        |

量化后在各个 benchmark 上的结果和原始版本对比如下：

| Model 5-shot           | C-Eval | MMLU | CMMLU |
|------------------------|:------:|:----:|:-----:|
| Baichuan2-13B-Chat      | 55.31  | 56.69| 59.28  |
| Baichuan2-13B-Chat-int4 | 54.90   | 55.73 | 58.09  |
| Baichuan2-7B-Chat       | 54.35   | 52.93 | 54.99  |
| Baichuan2-7B-Chat-int4 | 53.04   | 51.72 | 52.84  |

可以看到，int4相对bfloat16掉点在1~2个点左右。

## CPU部署
Baichuan2模型支持CPU推理，但需要强调的是，CPU的推理速度相对较慢。需按如下方式修改模型加载的方式：
```python
#以Baichuan2-7B-Chat为例
model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Chat", torch_dtype=torch.float32, trust_remote_code=True)
```
## Baichuan2相对Baichuan1推理迁移
由于很多用户在Baichuan1上做了很多优化的工作，例如编译优化、量化等，为了将这些工作零成本地应用于Baichuan2，用户可以对Baichuan2模型做1个离线转换，转换后就可以当做Baichuan1模型来使用。具体来说，用户只需要利用以下脚本离线对Baichuan2模型的最后一层lm_head做归一化，并替换掉”lm_head.weight“即可。替换完后，就可以像对Baichuan1模型一样对转换后的模型做编译优化等工作了。
```python
import torch
import os
ori_model_dir = 'your baichuan2 model directory'
#为了不覆盖原始模型，最好将转换后的模型save到另一个目录再替换
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
cd Baichuan2/finetune
pip install -r requirements.txt
```
- 如需使用lora等轻量级微调方法需额外安装peft
- 如需使用Xformers进行训练加速需额外安装xformers

## 单机训练

下面我们给一个微调Baichuan2-7B-Base的单机训练例子。

训练数据：data/belle_chat_ramdon_10k.json，该样例数据是从[multiturn_chat_0.8M](https://huggingface.co/datasets/BelleGroup/multiturn_chat_0.8M)采样出1万条，并且做了格式转换。主要是展示多轮数据怎么训练，不保证效果。


```shell
hostfile=""  # 单机
# hostfile="/path/to/hostfile"  # 多机
deepspeed --hostfile=$hostfile sft.py  \
    --report_to "none" \
    --data_path "data/belle_chat_ramdon_10k.json" \
    --model_name_or_path "Baichuan/Baichuan2-7B-Base" \
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

多机训练只需要给一下hostfile，内容如下：
```
ip1 slots=8
ip2 slots=8
ip3 slots=8
ip4 slots=8
```
同时在训练脚本里面指定hosftfile的路径：
```shell
hostfile="/path/to/hostfile"  # 多机
deepspeed --hostfile=$hostfile sft.py  \
    --report_to "none" \
    --data_path "data/belle_chat_ramdon_10k.json" \
    --model_name_or_path "Baichuan/Baichuan2-7B-Base" \
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

代码已经支持轻量化微调如Lora，如需使用仅需在上面的脚本中加入以下参数
```shell
--use_lora True
```
lora具体的配置可见finetune.py脚本。
使用lora微调后可以使用下面的命令加载模型
```python
from peft import AutoPeftModelForCausalLM

model = AutoPeftModelForCausalLM.from_pretrained("output", trust_remote_code=True)
```
# 社区支持

# 声明

我们在此声明，我们的开发团队并未基于 Baichuan2 模型开发任何应用，无论是在 iOS、Android、网页或任何其他平台。我们强烈呼吁所有使用者，不要利用 Baichuan2 模型进行任何危害国家社会安全或违法的活动。另外，我们也要求使用者不要将 Baichuan2 模型用于未经适当安全审查和备案的互联网服务。我们希望所有的使用者都能遵守这个原则，确保科技的发展能在规范和合法的环境下进行。

我们已经尽我们所能，来确保模型训练过程中使用的数据的合规性。然而，尽管我们已经做出了巨大的努力，但由于模型和数据的复杂性，仍有可能存在一些无法预见的问题。因此，如果由于使用 Baichuan2 开源模型而导致的任何问题，包括但不限于数据安全问题、公共舆论风险，或模型被误导、滥用、传播或不当利用所带来的任何风险和问题，我们将不承担任何责任。

# 协议
对本仓库源码的使用遵循开源许可协议 [Apache 2.0](https://github.com/baichuan-inc/Baichuan-13B/blob/main/LICENSE)。对 Baichuan2 模型的社区使用见[《Baichuan2 模型社区许可协议》](https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat/resolve/main/Baichuan2%20%E6%A8%A1%E5%9E%8B%E7%A4%BE%E5%8C%BA%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE.pdf)。Baichuan2 支持商用。如果将 Baichuan2 模型或其衍生品用作商业用途，请您按照如下方式联系许可方，以进行登记并向许可方申请书面授权：联系邮箱 <opensource@baichuan-inc.com>。
