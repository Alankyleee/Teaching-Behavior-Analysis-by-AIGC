# -*- coding:utf-8 -*-

import requests
import time
import pandas as pd
import openai

from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key="XXXXXXXXXXXXXXXXXXXX",
    base_url="XXXXXXXXXXXXXXXXXXXX"
)



# 获取从服务器返回的结果
def get_answer(prompt, model="xxx"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    answer = response.choices[0].message.content
    return answer


# 读取Excel文件并准备prompt
def prepare_prompts(file_name):
    df = pd.read_excel(file_name)
    prompt_base = (""""
以下是课堂教学行为编码表的分类：
格式为：行为表述+行为表现形式
行为主体为教师的包括
1 讲授。就内容或步骤提供事实或见解,表达教师自己的观点,提出教师自己的解释,或引述某位权威者(而非学生)的看法等。
2 提问。以教师的意见或想法为基础,询问学生问题,并期待学生的回答;通常要求学生记住一些事实,或引导学生想象、分析。
3 指示。指示或命令学生做某事,期望学生服从、接受教师的意志或企图改变学生的行为(如批评等);引导学生开展学习活动等。
4 反馈与评价。教师以结论性的回答结束谈话;对于学生的回答,教师请学 生做进一步的思考或讨论,发展或补充学生所提出的意见或 想法;对学习内容、学生的观点或学生学习的效果进行评价。
13 板书。通过在黑板、白板等工具上抄写、演算等方式展示教学内容。
14 演示或展示。教师用实物、模型进行演示,或使用多媒体进行展示。
15 观察或巡视。教师通过巡视或观察了解学生的学习情况。
16 个别指导或参与活动。教师与学生通过提问与应答、要求与反应、评价与反馈实现 互动,在学生开展练习与实践、实验活动等的过程中,教师 针对学生遇到的问题或困难实时给予指导等。
现在你作为一个课堂行为分类机器人，对于输入按照分类，严格地只输出行为编码，不输出其他内容。
以下是你要判断的句子改句子是课堂对话的内容：
    """
                   )
    result = [prompt_base + speech for speech in df['speech']]
    return result


# 主函数
def main():
    # 准备prompt列表
    prompts = prepare_prompts('problem3.xlsx')

    jieguo = []
    i = 0

    # 遍历prompt列表，获取答案，并保存到Excel
    for prompt in prompts:
        print(prompt)
        time.sleep(10)  # 避免API速率限制
        answer = get_answer(prompt)
        jieguo.append(answer)
        print(answer)
        print(i)
        i += 1

    # 保存结果到Excel
    df_jieguo = pd.DataFrame({'jieguo': jieguo})
    df_jieguo.to_excel('gpt_result3.xlsx', index=False)


# 运行主函数
if __name__ == "__main__":
    main()
