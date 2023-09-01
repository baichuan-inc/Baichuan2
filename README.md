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
- [Benchmark结果](#Benchmark结果)
- [模型细节](#模型细节)
- [推理和部署](#推理和部署)
- [应用案例](#应用案例)
- [对模型进行微调](#对模型进行微调)
- [社区支持](#社区支持)
- [声明](#声明)
- [协议](#协议)

# 介绍

## 模型下载
| 模型尺寸 | 基座模型  | 对齐模型 | 对齐模型 int4 量化 |
|:-------:|:-------:|:-------:|:-----------------:|
| 7B      | [Baichuan2-7B-Base](https://huggingface.co/baichuan-inc/Baichuan2-7B-Base) |[Baichuan2-7B-Chat](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat) |[Baichuan2-7B-Chat-int4](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat-int4) |
| 13B     | [Baichuan2-13B-Base](https://huggingface.co/baichuan-inc/Baichuan2-13B-Base) |[Baichuan2-13B-Chat](https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat) |[Baichuan2-13B-Chat-int4](https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat-int4) |

# Benchmark结果

# 推理和部署

## 量化

# 应用案例

# 对模型进行微调

## 依赖安装
```shell
git clone https://github.com/baichuan-inc/Baichuan2.git
cd Baichuan2/fine-tune
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
deepspeed --hostfile=$hostfile fine-tune.py  \
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
deepspeed --hostfile=$hostfile fine-tune.py  \
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
lora具体的配置可见fine-tune.py脚本。
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
