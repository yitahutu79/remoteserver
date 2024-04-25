import argparse
import json, os
import pandas as pd
from tqdm import tqdm


import numpy as np
import torch   
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from peft import  PeftModel


# os.environ["CUDA_LAUNCH_BLOCKING"] = "0"
# os.environ["CUDA_VISIBLE_DEVICES"] = "2"
# print(torch.cuda.device_count())
# torch.cuda.set_device(2)

def mk_prompt(history:list,ins:str,query:str,model_name:str,tokenizer=None)->str:
    # print(history)
    if model_name.startswith('baichuan'):
        prompt = '<reserved_106>' + ins
        for msg in history[0]:
            # print(msg)
            if msg.startswith("user: "):
                prompt += '<reserved_106>' + msg[6:]
            elif msg.startswith("assistant: "):
                prompt += '<reserved_107>' + msg[11:]
        prompt += '<reserved_106>' + query + '<reserved_107>'
    
    # old template
    # if model_name.startswith('baichuan'):
    #     for msg in history[0]:
    #         # print(msg)
    #         if msg.startswith("user: "):
    #             prompt += '<reserved_106>' + msg[6:]
    #         elif msg.startswith("assistant: "):
    #             prompt += '<reserved_107>' + msg[11:]
    #     prompt += '<reserved_106>' + ins
    #     prompt += query + '<reserved_107>'
        
        return prompt
    elif model_name.startswith('qwen') or model_name.startswith('llama'):
        messages = [{"role": "system", "content": ins[:-10]}]
        if history:
            for msg in history[0]:
                if msg.startswith("user: "):
                    messages.append({"role": "user", "content": msg[6:]})
                elif msg.startswith("assistant: "):
                    messages.append({"role": "assistant", "content": msg[11:]})
        messages.append({"role": "user", "content": query})
        # print('*'*100)
        # print(messages)
        # print('*'*100)
        # Pad the input tokens
        ids = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        return ids
    
    return None

def infer(model_path:str,eval_data:list,lora_model:str=None):
    """
    
    model_name 记得规范开头  是baichuan_xx  qwen_xx  yi_xx 之类的
    """
    
    load_type = torch.float16
    

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True,
        padding_side='left'
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=load_type,
        low_cpu_mem_usage=True,
        device_map='auto',
        trust_remote_code=True
        )
    
    if lora_model:
         model = PeftModel.from_pretrained(
            base_model, 
            lora_model,
            torch_dtype=load_type,
            device_map='auto'
        )
    else:
        model = base_model
    model.eval()
    model.generation_config = GenerationConfig.from_pretrained(model_path)
    # with torch.no_grad():
        
    #     print('=' * 85)
    #     print("Start inference with instruction mode.")

    #     print('=' * 85)
    
    json_data = eval_data #json.load(open(eval_data_path, 'r', encoding='utf8'))
    
    batch_size = 10

    json_data = [
        json_data[i: i+batch_size] for i in range(0, len(json_data), batch_size)
    ]
    result = []
    # 每一个batch的数据
    for batch in tqdm(json_data):
        input_batch = []
        labs = []
        qs = []
        # 每一条数据
        for item in batch:
            query, ins, label, history = item['input'], item['instruction'], item['output'], item['history']

            
            ids = mk_prompt(history,ins,query,model.config.model_type,tokenizer)
            
            # print(ids)
            # print(query)
            
            input_batch.append(ids)
            labs.append(label)
            qs.append(query)

            inputs = tokenizer(input_batch, padding=True, return_tensors="pt").to(model.device)

        generated_ids = model.generate(
            input_ids=inputs.input_ids,
            max_new_tokens=128,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

        generation_output = generated_ids.cpu() # 17G
        
        if model.config.model_type.startswith('baichuan'):
            split_word = '<reserved_107>'
        else: # 目前支持的yi和 qwen 其实都是assistant
            split_word = 'assistant'
            
        output = [
            tokenizer.decode(
                i, 
                skip_special_tokens=True
            ).split(split_word)[-1].strip() for i in generation_output
        ]
        
        
        
            
        for q,i, l in zip(qs,output, labs):
            # print('query:',q)
            # if len(i) > 30 and len(i) / len(l) > 1.2:
            #     print('**long** ai:',i)
            # else:
            #     print('ai:',i)
            # print('label:',l)
            print('query:',q,'ai:',i,'lable:',l)
            break
                
            # result.append(output.split('<\s>')[0])
            
        result += output
    print('done')
    
    
    return result

if __name__ == '__main__':

    print('ok')
    # model_path = '/data/models/baichuan-inc/Baichuan2-13B-Chat'
    model_path = '/data/models/qwen/Qwen1.5-14B-Chat'
    # model_path = '/data/xhm/LLaMA-Factory/saves/Qwen1.5-14B-Chat/full'

    # model_path = '/data/cxl/saves/Yi-34B-Chat/yil0' #  good
    model_path = '/data/cxl/saves/Yi-34B-Chat/yil03-1' #  good
 
    model_path = '/data/cxl/saves/Yi-34B-Chat/yi-ppo-1ktry' #   有灾难遗忘的情形
    model_path = '/data/cxl/saves/Qwen1.5-14B-Chat/qwl02-dora' #   ok
    model_path = '/data/cxl/saves/Qwen1.5-14B-Chat/qwl02-1'  # 1300 dpspd
    # model_path = '/data/cxl/saves/Qwen1.5-14B-Chat/qwl02' #   1300
    model_path = '/data/cxl/saves/Qwen1.5-1.8B-Chat/qwl02-1.8B' #   1300
    
    
    
    
    
    # print(model_path)
    
    # 服务器路径有这个文件就可以读，没有直接用下面定义的
    data = json.load(open('/data/lj/eval/mk_eval_data/data/eval_tbu_for_qwen14.json','r',encoding='utf8'))
    # data = [
    #         {
    #             'instruction': '你是一名电商人工客服，请用礼貌、专业的态度回答用户的问题，请务必使用中文回答。必要时请参考对话记录。\n以下是供你参考的已知信息：\n1. 问题："都没货了么", 答案："亲 不能拍就是没有了哦"\n2. 问题："你好，我买的产品怎么还没到货，", 答案："我催促下亲"\n3. 问题："已下单，急用", 答案："下单48小时内发货亲"\n4. 问题："这物流从2号到现在怎么一直没更新", 答案："亲亲，通常包裹量比较大的时候，可能会影响快递公司及时更新物流信息的速度，这边催下快递。"\n5. 问题："在吗我的多少怎么没到我的东西怎么没到", 答案："亲 这边联系快递核实"\n6. 问题："为什么我所在的地区无法下单？", 答案："无法下单就是目前您所在地区停发了亲"\n上述的已知信息可能与用户的问题无关，你需要根据用户的具体需求选择性的参考。\n另外你要避免向客户做出承诺，如优惠、物流时间等\n\n你要回复的问题是：',
    #             'output': '亲,能下单才是有货的哈',
    #             'history': [['user: 咋没货']],
    #             'input': '咋没货'
    #         },
    #         {
    #             'instruction': '你是一名电商人工客服，请用礼貌、专业的态度回答用户的问题，请务必使用中文回答。必要时请参考对话记录。\n以下是供你参考的已知信息：\n1. 问题："都没货了么", 答案："亲 不能拍就是没有了哦"\n2. 问题："你好，我买的产品怎么还没到货，", 答案："我催促下亲"\n3. 问题："已下单，急用", 答案："下单48小时内发货亲"\n4. 问题："这物流从2号到现在怎么一直没更新", 答案："亲亲，通常包裹量比较大的时候，可能会影响快递公司及时更新物流信息的速度，这边催下快递。"\n5. 问题："在吗我的多少怎么没到我的东西怎么没到", 答案："亲 这边联系快递核实"\n6. 问题："为什么我所在的地区无法下单？", 答案："无法下单就是目前您所在地区停发了亲"\n上述的已知信息可能与用户的问题无关，你需要根据用户的具体需求选择性的参考。\n另外你要避免向客户做出承诺，如优惠、物流时间等\n\n你要回复的问题是：',
    #             'output': '亲,能下单才是有货的哈',
    #             'history': [['user: 咋没货']],
    #             'input': '你好'
    #         },
    #         {
    #             'instruction': '你是一名电商人工客服，请用礼貌、专业的态度回答用户的问题，请务必使用中文回答。必要时请参考对话记录。\n以下是供你参考的已知信息：\n1. 问题："保质期多久啊？", 答案："亲，冰箱保鲜一年"\n2. 问题："<运营问题>保质期多久？", 答案："1年"\n3. 问题："有效期多久", 答案："亲，这个商品收到后需要冷藏保存，保质期为1年。"\n4. 问题："这个保质期为什么是3年", 答案："亲，这个商品的保质期通常为3年哦。但是我们建议常温一年使用完 \n"\n5. 问题："我看说明上写着保质期三年呢", 答案："亲正常就是一年左右哈"\n6. 问题："怎么清洗会不会有味道保质期多久", 答案："亲，用料酒泡30分钟-1小时，用手搓洗肠衣几遍即可。"\n上述的已知信息可能与用户的问题无关，你需要根据用户的具体需求选择性的参考。\n另外你要避免向客户做出承诺，如优惠、物流时间等\n\n你要回复的问题是：',
    #             'output': '亲,这个商品收到后需要冷藏保存,保质期为1年。',
    #             'history': [['assistant: 很高兴为您服务,请问有什么可以帮您？',
    #             'user: 肠衣袋里使用盐淹着呢么？',
    #             'assistant: 亲,肠衣是盐腌制的哦~']],
    #             'input': '保质期多久'
    #         }
    #         ]
    # print(data[0])
    model_path = '/data/models/qwen/Qwen1.5-1.8B-Chat'
    lora_path = None # '/data/cxl/saves/Qwen1.5-1.8B-Chat/lora/qw18l02-2-r32'
    model_path ='/data/models/01ai/Yi-34B-Chat'
    # lora_path ='/data/cxl/saves/Yi-34B-Chat/lora/yi/yil02-loramoe'  # moe -2   记得切换layer底层环境！
    model_path ='/data/cxl/saves/Yi-34B-Chat/yil02-loramoe-test'
    result = infer(model_path=model_path,eval_data = data,lora_model=lora_path)
    
    """
    yimoe 分析
    
    合并好的  只测了 loramoe  看起来正常
    
    lora的
        yil02-loramoe-1：   有bad现象   ps:没改底层，改底层之后尝试 bad但模型的确有moe层～
        yil02-loramoe ：    有bad现象   ps:没改底层，改底层之后尝试 bad但模型的确有moe层～
    合并上面的
      都没有那个现象了   
      yil02-loramoe-1：   无bad现象   ps:没改底层，改底层之后尝试：  ok  但是model没有loramoe   
      yil02-loramoe ：    无bad现象  ps:没改底层，改底层之后尝试：  ok  但是model没有loramoe   
    """
    
    # print(result)


"""
'<reserved_106>我已经拼单成功16小时,能尽快帮我发货吗？
<reserved_107>亲 我们将会在年后2月15日(正月初六)上班按照订单先后顺序发出。
<reserved_106>有视频吗<reserved_107>可以参考看下
<reserved_106>你是一名电商人工客服，请用礼貌、专业的态度回答用户的问题，请务必使用中文回答。必要时请参考对话记录。
\n以下是供你参考的已知信息：
\n1. 问题："购买后的产品需要全部一次使用完吗？",答案："您可以先泡一些的  不够在泡  用不完还可以储存 用水泡过的肠衣没用完可以用盐腌制起来 然后沥干水分 后食品袋包好放冰箱冷藏保鲜就可以了亲 没泡过的直接冷藏保鲜就可以"\n2. 问题："<食用方式>肠胃不好可以食用吗？",答案："可以"\n3. 问题："<运营问题>保质期多久？",答案："1年"\n4. 问题："<食用方式>食用完会不会容易胀气或腹泻？",答案："不会"\n
上述的已知信息可能与用户的问题无关，你需要根据用户的具体需求选择性的参考。\n
另外你要避免向客户做出承诺，如优惠、物流时间等\n
\n你要回复的问题是：肠衣要用什么水,泡多久<reserved_107>'
"""