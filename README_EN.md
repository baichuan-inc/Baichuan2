<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->

<div align="center">
<h1>
  Baichuan2
</h1>
</div>

<p align="center">
🤗 <a href="https://huggingface.co/baichuan-inc/" target="_blank">Hugging Face</a> • 🤖 <a href="https://modelscope.cn/organization/baichuan-inc" target="_blank">ModelScope</a> • 💬 <a href="https://github.com/baichuan-inc/Baichuan-7B/blob/main/media/wechat.jpeg?raw=true" target="_blank">WeChat</a>
</p>

<div align="center">

[![license](https://img.shields.io/github/license/modelscope/modelscope.svg)](https://github.com/baichuan-inc/Baichuan2/blob/main/LICENSE)
<h4 align="center">
    <p>
        <b>English</b> |
        <a href="https://github.com/baichuan-inc/Baichuan2/blob/main/README.md">中文</a>
    <p>
</h4>
</div>

# Table of Contents

- [Introduction](#Introduction)
- [Benchmark Results](#Benchmark-Results)
- [Inference and Deployment](#Inference-and-Deployment)
- [Fine-tuning the Model](#Fine-tuning-the-Model)
- [Intermediate Checkpoints](#Intermediate-Checkpoints)
- [Community and Ecosystem](#Community-and-Ecosystem)
- [Disclaimer](#Disclaimer)
- [License](#License)

# Introduction

Baichuan2 is an updated version released by Baichuan Intelligence after Baichuan-7B and Baichuan-13B. It was trained on a high-quality corpus with 2.64 trillion tokens, achieving the best results in both Chinese and English benchmarks of the same scale. This release includes Base and Chat versions for 7B and 13B, and a 4bits quantized version for the Chat model. All versions are fully open to academic research. Developers only need to apply via email and obtain official commercial permission to use it for free commercially. The specific released versions and download links are shown in the table below:

|         | Base Model  | Aligned Model | Aligned Model 4bits Quantized |
|:-------:|:-----------:|:-------------:|:-----------------------------:|
| 7B      | 🤗 [Baichuan2-7B-Base](https://huggingface.co/baichuan-inc/Baichuan2-7B-Base) | 🤗 [Baichuan2-7B-Chat](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat) | 🤗 [Baichuan2-7B-Chat-4bits](https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat-4bits) |
| 13B     | 🤗 [Baichuan2-13B-Base](https://huggingface.co/baichuan-inc/Baichuan2-13B-Base) | 🤗 [Baichuan2-13B-Chat](https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat) | 🤗 [Baichuan2-13B-Chat-4bits](https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat-4bits) |

# Benchmark Results

We conducted extensive testing on authoritative Chinese-English datasets across six domains: general, legal, medical, mathematics, code, and multi-language translation.

## General Domain

In the general domain, we conducted 5-shot tests on the following datasets:
- [C-Eval](https://cevalbenchmark.com/index.html#home) is a comprehensive Chinese basic model evaluation dataset, covering 52 disciplines and four levels of difficulty. We used the dev set of this dataset as the source for few-shot learning and tested on the test set. Our evaluation approach followed that of [Baichuan-7B](https://github.com/baichuan-inc/Baichuan-7B/tree/main).
- [MMLU](https://arxiv.org/abs/2009.03300) is an English evaluation dataset comprising 57 tasks, encompassing elementary math, American history, computer science, law, etc. The difficulty ranges from high school level to expert level. It's a mainstream LLM evaluation dataset. We used its [open-source](https://github.com/hendrycks/test) evaluation approach.
- [CMMLU](https://github.com/haonan-li/CMMLU) is a comprehensive Chinese evaluation benchmark covering 67 topics, specifically designed to assess language models' knowledge and reasoning capabilities in a Chinese context. We adopted its [official](https://github.com/haonan-li/CMMLU) evaluation approach.
- [Gaokao](https://github.com/OpenLMLab/GAOKAO-Bench) is a dataset utilizing China's college entrance examination questions to evaluate large language models' abilities, focusing on linguistic proficiency and logical reasoning. We retained only its single-choice questions and conducted random partitioning. Our evaluation method is similar to that of C-Eval.
- [AGIEval](https://github.com/microsoft/AGIEval) aims to evaluate a model's general abilities in cognition and problem-solving related tasks. We retained only its four-option single-choice questions and did random partitioning. We used an evaluation scheme similar to C-Eval.
- [BBH](https://huggingface.co/datasets/lukaemon/bbh) is a challenging task subset of Big-Bench. Big-Bench currently includes 204 tasks. Task themes involve linguistics, child development, mathematics, common sense reasoning, biology, physics, societal biases, software development, etc. BBH consists of benchmark tasks extracted from the 204 Big-Bench tasks in which large models did not perform well.

### 7B 模型结果
|               | **C-Eval** | **MMLU** | **CMMLU** | **Gaokao** | **AGIEval** | **BBH** |
|:---------------------:|:----------:|:--------:|:---------:|:----------:|:-----------:|:-------:|
|               |  5-shot    |  5-shot  |  5-shot   | 5-shot     | 5-shot      | 3-shot  |
| **GPT-4**             | 68.40      | 83.93    | 70.33     | 66.15      | 63.27       | -       |
| **GPT-3.5-Turbo**     | 51.10      | 68.54    | 54.06     | 47.07      | 46.13       | -   |
| **LLaMA-7B**          | 27.10      | 35.10    | 26.75     | 27.81      | 28.17       | 32.38   |
| **LLaMA2-7B**         | 28.90      | 45.73    | 31.38     | 25.97      | 26.53       | 39.16   |
| **MPT-7B**            | 27.15      | 27.93    | 26.00     | 26.54      | 24.83       | -       |
| **Falcon-7B**         | 24.23      | 26.03    | 25.66     | 24.24      | 24.10       | -       |
| **ChatGLM2-6B**       | 50.20      | 45.90    | 49.00     | 49.44      | 45.28       | 31.65   |
| **Baichuan-7B**       | 42.80      | 42.30    | 44.02     | 36.34      | 34.44       | 32.48   |
| **Baichuan2-7B-Base**      | 54.00      | 54.16    | 57.07     | 47.47      | 42.73       | 41.56   |



### 13B 模型结果
|                     | **C-Eval** | **MMLU** | **CMMLU** | **Gaokao** | **AGIEval** | **BBH** |
|:---------------------------:|:----------:|:--------:|:---------:|:----------:|:-----------:|:-------:|
|                     |  5-shot    |  5-shot  |  5-shot   | 5-shot     | 5-shot      | 3-shot  |
| **GPT-4**                   | 68.40      | 83.93    | 70.33     | 66.15      | 63.27       | -       |
| **GPT-3.5-Turbo**           | 51.10      | 68.54    | 54.06     | 47.07      | 46.13       | -   |
| **LLaMA-13B**               | 28.50      | 46.30    | 31.15     | 28.23      | 28.22       | 37.89   |
| **LLaMA2-13B**              | 35.80      | 55.09    | 37.99     | 30.83      | 32.29       | 46.98   |
| **Vicuna-13B**              | 32.80      | 52.00    | 36.28     | 30.11      | 31.55       | 43.04   |
| **Chinese-Alpaca-Plus-13B** | 38.80      | 43.90    | 33.43     | 34.78      | 35.46       | 28.94   |
| **XVERSE-13B**              | 53.70      | 55.21    | 58.44     | 44.69      | 42.54       | 38.28   |
| **Baichuan-13B-Base**       | 52.40      | 51.60    | 55.30     | 49.69      | 43.20       | 43.01   |
| **Baichuan2-13B-Base**           | 58.10      | 59.17    | 61.97     | 54.33      | 48.17       | 48.78   |


## Law and Medicine
In the legal domain, we used the [JEC-QA](https://jecqa.thunlp.org/) dataset. The JEC-QA dataset originates from China's National Judicial Examination. We retained only the multiple-choice questions from it. Our evaluation method was similar to that of C-Eval.

In the medical domain, we used medical-related subjects from general domain datasets (C-Eval, MMLU, CMMLU), as well as [MedQA](https://arxiv.org/abs/2009.13081) and [MedMCQA](https://medmcqa.github.io/). We followed an evaluation scheme similar to C-Eval.
- The MedQA dataset comes from medical exams in the US, Mainland China, and Taiwan. We tested the USMLE and MCMLE subsets from the [MedQA dataset](https://huggingface.co/datasets/bigbio/med_qa), and used a version with five candidates.
- The MedMCQA dataset originates from entrance exams of medical colleges in India. We retained only the multiple-choice questions. Since the test set doesn't have answers, we used the dev set for testing.
- Medical-related subjects included in the general domain datasets are as follows:
    - C-Eval: clinical_medicine, basic_medicine
    - MMLU: clinical_knowledge, anatomy, college_medicine, college_biology, nutrition, virology, medical_genetics, professional_medicine
    - CMMLU: anatomy, clinical_knowledge, college_medicine, genetics, nutrition, traditional_chinese_medicine, virology 

We conducted 5-shot tests on the above datasets.


### 7B 模型结果

|             | **JEC-QA** | **CEval-MMLU-CMMLU** | **MedQA-USMLE** | **MedQA-MCMLE** | **MedMCQA** |
|:---------------------:|:----------:|:--------------------:|:---------------:|:---------------:|:-----------:|
|             | 5-shot     |  5-shot              |  5-shot         |  5-shot         | 5-shot      |
| **GPT-4**             | 59.32      | 77.16                | 80.28           | 74.58           | 72.51       |
| **GPT-3.5-Turbo**     | 42.31      | 61.17                | 53.81           | 52.92           | 56.25       |
| **LLaMA-7B**          | 27.45      | 33.34                | 24.12           | 21.72           | 27.45       |
| **LLaMA2-7B**         | 29.20      | 36.75                | 27.49           | 24.78           | 37.93       |
| **MPT-7B**            | 27.45      | 26.67                | 16.97           | 19.79           | 31.96       |
| **Falcon-7B**         | 23.66      | 25.33                | 21.29           | 18.07           | 33.88       |
| **ChatGLM2-6B**       | 40.76      | 44.54                | 26.24           | 45.53           | 30.22       |
| **Baichuan-7B**       | 34.64      | 42.37                | 27.42           | 39.46           | 31.39       |
| **Baichuan2-7B-Base** | 44.46      | 56.39                | 32.68           | 54.93           | 41.73       |


### 13B 模型结果
|                  | **JEC-QA** | **CEval-MMLU-CMMLU** | **MedQA-USMLE** | **MedQA-MCMLE** | **MedMCQA** |
|:---------------------------:|:----------:|:--------------------:|:---------------:|:---------------:|:-----------:|
|                   | 5-shot     |  5-shot              |  5-shot         |  5-shot         | 5-shot      |
| **GPT-4**                   | 59.32      | 77.16                | 80.28           | 74.58           | 72.51       |
| **GPT-3.5-Turbo**           | 42.31      | 61.17                | 53.81           | 52.92           | 56.25       |
| **LLaMA-13B**               | 27.54      | 35.14                | 28.83           | 23.38           | 39.52       |
| **LLaMA2-13B**              | 34.08      | 47.42                | 35.04           | 29.74           | 42.12       |
| **Vicuna-13B**              | 28.38      | 40.99                | 34.80           | 27.67           | 40.66       |
| **Chinese-Alpaca-Plus-13B** | 35.32      | 46.31                | 27.49           | 32.66           | 35.87       |
| **XVERSE-13B**              | 46.42      | 58.08                | 32.99           | 58.76           | 41.34       |
| **Baichuan-13B-Base**       | 41.34      | 51.77                | 29.07           | 43.67           | 39.60       |
| **Baichuan2-13B-Base**      | 47.40      | 59.33                | 40.38           | 61.62           | 42.86       |

## Mathematics and Code
In the mathematics domain, we used the [OpenCompass](https://opencompass.org.cn/) evaluation framework and conducted 4-shot tests on the [GSM8K](https://huggingface.co/datasets/gsm8k) and [MATH](https://huggingface.co/datasets/competition_math) datasets.

- GSM8K is a dataset released by OpenAI, consisting of 8.5K high-quality linguistically diverse elementary school math application questions. It requires selecting the most reasonable solution based on a given scenario and two possible solutions.
- The MATH dataset contains 12,500 math problems (of which 7,500 belong to the training set and 5,000 to the test set). These problems are collected from math competitions like AMC 10, AMC 12, AIME.

For the code domain, we used the [HumanEval](https://huggingface.co/datasets/openai_humaneval) and [MBPP](https://huggingface.co/datasets/mbpp) datasets. Using OpenCompass, we performed a 0-shot test on HumanEval and a 3-shot test on the MBPP dataset.
- Tasks in HumanEval include programming tasks encompassing language understanding, reasoning, algorithms, and basic math to evaluate the functional correctness of models and measure their problem-solving capability.
- MBPP consists of a dataset with 974 Python short functions, textual descriptions of programs, and test cases to check their functional correctness.

### 7B 模型结果
|               | **GSM8K** | **MATH** | **HumanEval** | **MBPP** |
|:---------------------:|:---------:|:--------:|:-------------:|:--------:|
|               |  4-shot   | 4-shot   |  0-shot       |  3-shot  |
| **GPT-4**             |   89.99   | 40.20    | 57.32         |  63.60   |
| **GPT-3.5 Turbo**     |   57.77   | 13.96    | 52.44         |  61.40   |
| **LLaMA-7B**          |   9.78    | 3.02     | 11.59         |  14.00   |
| **LLaMA2-7B**         |   16.22   | 3.24     | 12.80         |  14.80   |
| **MPT-7B**            |   8.64    | 2.90     | 14.02         |  23.40   |
| **Falcon-7B**         |   5.46    | 1.68     | -             |  10.20   |
| **ChatGLM2-6B**       |   28.89   | 6.40     | 9.15          |   9.00   |
| **Baichuan-7B**       |   9.17    | 2.54     | 9.20          |   6.60   |
| **Baichuan2-7B-Base**      |   24.49   | 5.58     | 18.29         |  24.20   |

### 13B 模型结果

|                     | **GSM8K** | **MATH** | **HumanEval** | **MBPP** |
|:---------------------------:|:---------:|:--------:|:-------------:|:--------:|
|                     |  4-shot   | 4-shot   |  0-shot       |  3-shot  |
| **GPT-4**                   |   89.99   | 40.20    | 57.32         |  63.60   |
| **GPT-3.5 Turbo**           |   57.77   | 13.96    | 52.44         |  61.40   |
| **LLaMA-13B**               |   20.55   | 3.68     | 15.24         |  21.40   |
| **LLaMA2-13B**              |   28.89   | 4.96     | 15.24         |  27.00   |
| **Vicuna-13B**              |   28.13   | 4.36     | 16.46         |  15.00   |
| **Chinese-Alpaca-Plus-13B** |   11.98   | 2.50     | 16.46         |  20.00   |
| **XVERSE-13B**              |   18.20   | 2.18     | 15.85         |  16.80   |
| **Baichuan-13B-Base**       |   26.76   | 4.84     | 11.59         |  22.80   |
| **Baichuan2-13B-Base**           |   52.77   | 10.08    | 17.07         |  30.20   |

## Multilingual
We used the [Flores-101](https://huggingface.co/datasets/facebook/flores) dataset to evaluate the multilingual capability of the model. Flores-101 covers 101 languages from around the world. Its data comes from various domains including news, travel guides, and books. We chose the official languages of the United Nations (Arabic, Chinese, English, French, Russian, and Spanish) as well as German and Japanese for testing. Using OpenCompass, we performed 8-shot tests on seven sub-tasks within Flores-101: Chinese-English, Chinese-French, Chinese-Spanish, Chinese-Arabic, Chinese-Russian, Chinese-Japanese, and Chinese-German.

### 7B 模型结果

|               | **中-英** | **中-法** | **中-西班牙** | **中-阿拉伯** | **中-俄** | **中-日** | **中-德** |
|:---------------------:|:-------:|:-------:|:---------:|:---------:|:-------:|:-------:|:-------:|
| **GPT-4**             | 29.94   | 29.56   | 20.01     | 10.76     | 18.62   | 13.26   | 20.83   |
| **GPT-3.5 Turbo**     | 27.67   | 26.15   | 19.58     | 10.73     | 17.45   | 1.82    | 19.70   |
| **LLaMA-7B**          | 17.27   | 12.02   | 9.54      | 0.00      | 4.47    | 1.41    | 8.73    |
| **LLaMA2-7B**         | 25.76   | 15.14   | 11.92     | 0.79      | 4.99    | 2.20    | 10.15   |
| **MPT-7B**            | 20.77   | 9.53    | 8.96      | 0.10      | 3.54    | 2.91    | 6.54    |
| **Falcon-7B**         | 22.13   | 15.67   | 9.28      | 0.11      | 1.35    | 0.41    | 6.41    |
| **ChatGLM2-6B**       | 22.28   | 9.42    | 7.77      | 0.64      | 1.78    | 0.26    | 4.61    |
| **Baichuan-7B**       | 25.07   | 16.51   | 12.72     | 0.41      | 6.66    | 2.24    | 9.86    |
| **Baichuan2-7B-Base**      | 27.27   | 20.87   | 16.17     | 1.39      | 11.21   | 3.11    | 12.76   |


### 13B 模型结果

|                             | **中-英** | **中-法** | **中-西班牙** | **中-阿拉伯** | **中-俄** | **中-日** | **中-德** |
|:---------------------------:|:-------:|:-------:|:---------:|:---------:|:-------:|:-------:|:-------:|
|          **GPT-4**          | 29.94   | 29.56   | 20.01     | 10.76     | 18.62   | 13.26   | 20.83   |
|      **GPT-3.5 Turbo**      | 27.67   | 26.15   | 19.58     | 10.73     | 17.45   | 1.82    | 19.70   |
|        **LLaMA-13B**        | 21.75   | 16.16   | 13.29     | 0.58      | 7.61    | 0.41    | 10.66   |
|       **LLaMA2-13B**        | 25.44   | 19.25   | 17.49     | 1.38      | 10.34   | 0.13    | 11.13   |
|       **Vicuna-13B**        | 22.63   | 18.04   | 14.67     | 0.70      | 9.27    | 3.59    | 10.25   |
| **Chinese-Alpaca-Plus-13B** | 22.53   | 13.82   | 11.29     | 0.28      | 1.52    | 0.31    | 8.13    |
|       **XVERSE-13B**        | 29.26   | 24.03   | 16.67     | 2.78      | 11.61   | 3.08    | 14.26   |
|    **Baichuan-13B-Base**    | 30.24   | 20.90   | 15.92     | 0.98      | 9.65    | 2.64    | 12.00   |
|      **Baichuan2-13B-Base**      | 30.61   | 22.11   | 17.27     | 2.39      | 14.17   | 11.58   | 14.53   |
