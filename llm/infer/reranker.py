import math
from typing import List
import numpy as np
from rouge_chinese import Rouge
import jieba
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import torch
from FlagEmbedding import BGEM3FlagModel, FlagReranker, FlagModel
import re
import string
from collections import Counter
import functools
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# NCCL_DEBUG="INFO"
class EmbeddingSimilarity():
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    def __init__(self, model_path='/data/models/Xorbits/bge-m3', device='cuda') -> None:
        self.bge_m3 = BGEM3FlagModel(
            model_path,  
            use_fp16=True,
            device=device
        )

        self.reranker = FlagReranker(
            '/data/models/Xorbits/bge-reranker-large', 
            use_fp16=True
        ) 

        self.large = FlagModel(
            '/data/models/AI-ModelScope/bge-large-zh-v1.5', 
            # query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
            use_fp16=True
        ) 


    def dense_score(self, pred: List[str], label: List[str]):
        pred_embeddings = self.bge_m3.encode(pred)["dense_vecs"]
        label_embeddings = self.bge_m3.encode(label)["dense_vecs"]

        return np.sum(pred_embeddings * label_embeddings, axis=-1)
    


    def rouge_bleu_score(self, pred: List[str], label: List[str], mean_result=True):
        """_summary_
            计算 chinese_rouge  当前是 1、2、L 分数平均的f
                bleu        当前是  1、2、3 4:3:3
                二者的差异：前者的ngram是从truth出（考量召回率）   后者从infer中出（考量准确率）
                的值
        Args:
            pred (List[str]): _description_
            label (List[str]): _description_
            mean_result (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        score_dict = {"rouge-mean": [], "bleu-3": []}

        for pred_sentence, label_sentence in zip(pred, label):
            hypothesis = list(jieba.cut(pred_sentence))
            reference = list(jieba.cut(label_sentence))

            # 计算ROUGE得分
            if not hypothesis or not reference:
                mean_rouge_score = 0.0
            else:
                rouge = Rouge()
                scores = rouge.get_scores(" ".join(hypothesis), " ".join(reference))
                result = scores[0]
                rouge_f_scores = [value["f"] for key, value in result.items() if key in ("rouge-1", "rouge-2", "rouge-l")]
                mean_rouge_score = sum(rouge_f_scores) / len(rouge_f_scores) if rouge_f_scores else 0

            score_dict["rouge-mean"].append(round(mean_rouge_score * 100, 4))

            # 计算BLEU-4得分  4330的百分比主要计算精确旅
            bleu_score_2 = sentence_bleu([reference], hypothesis, weights=(0.4, 0.3, 0.3, 0), smoothing_function=SmoothingFunction().method1)

            score_dict["bleu-3"].append(round(bleu_score_2 * 100, 4))


        return score_dict

    def rouge_bleu_score_0(self, pred: List[str], label: List[str], mean_result=True):
        score_dict = {"rouge-1": [], "rouge-2": [], "rouge-l": [], "bleu-4": []}
        # score_dict = {"bleu-4": []}
        # score_dict = {"bleu-4": []}


        for pred, label in zip(pred, label):
            hypothesis = list(jieba.cut(pred))
            reference = list(jieba.cut(label))

            if len(" ".join(hypothesis).split()) == 0 or len(" ".join(reference).split()) == 0:
                result = {"rouge-1": {"f": 0.0}, "rouge-2": {"f": 0.0}, "rouge-l": {"f": 0.0}}
            else:
                rouge = Rouge()
                scores = rouge.get_scores(" ".join(hypothesis), " ".join(reference))
                result = scores[0]

            for k, v in result.items():
                score_dict[k].append(round(v["f"] * 100, 4))
            
            bleu_score = sentence_bleu([list(label)], list(pred), smoothing_function=SmoothingFunction().method3)
            score_dict["bleu-3"].append(round(bleu_score * 100, 4))
        
        return score_dict


    def scores(self, pred: List[str], label: List[str], mean_result=True):
        assert len(pred) == len(label), "Lengths of preds and labels should be equal."

        sentence_pairs = [(i,j) for i, j in zip(pred, label)]

        res = {}

        # res["m3_colbert"] = self.bge_m3.compute_score(
        #     sentence_pairs, 
        #     weights_for_different_modes=[0.4, 0.1, 0.5]
        # )["colbert"]

        # s1 = self.large.encode(pred)
        # s2 = self.large.encode(label)
        # res["bge_v1.5"] = np.sum(s1 * s2, axis=-1).tolist()
        
        res['my_cmrc_eval'] = [x*100 for x in my_cmrc_eval(pred,label)]
    
        # res['EM'] = qa_exact_match(pred,label)
        # res['F1'] = qa_f1(pred,label)
        # res['Accuracy'] = accuracy_metric(pred,label)
        # res['Precision'] = precision_metric(pred,label)
        # res['Recall'] = recall_metric(pred,label)
        # res['F1_mul'] = F1_metric(pred,label)
        
        # sentence_pairs.to("cuda:2")
        
        
        res["reranker"] = self.reranker.compute_score(
            sentence_pairs,normalize=True
        )
        
        # min_value = -10
        # max_value = 10
        # res["reranker"] = [(x - min_value) / (max_value - min_value)*100 for x in res["reranker"]]
        res["reranker"] = [x*100 for x in res["reranker"]]
        

        res.update(self.rouge_bleu_score(pred, label))

        # if mean_result:
        #     res = {k: float(np.mean(v)) for k, v in res.items()}
        
        return res
    
    
    def reranker_score(self, pred: List[str], label: List[str],):
        assert len(pred) == len(label), "Lengths of preds and labels should be equal."

        sentence_pairs = [(i,j) for i, j in zip(pred, label)]

        return self.reranker.compute_score(
            sentence_pairs
        )
        

def special_for_dataset(predictions, examples):
    print("Metrics not found, maybe dataset special metric or metric name error")
    return True
       
def accuracy_metric(predictions, examples):
    """'predictions, examples are list(int)"""
    count = 0
    score_list = []
    num_predictions = max(len(predictions), 1)
    assert len(predictions) == len(examples)
    for prediction, example in zip(predictions, examples):
        count += prediction == example
        score_list.append(int(prediction == example))
    # return count * 100.0 / num_predictions, score_list
    return score_list

def F1_metric(predictions, examples):
    assert len(predictions) == len(examples)
    from sklearn.metrics import f1_score

    # truth = []
    # for prediction, example in zip(predictions, examples):
    #     truth.append(example["label"])

    return f1_score(examples, predictions, average="macro") * 100.0


def precision_metric(predictions, examples):
    assert len(predictions) == len(examples)
    from sklearn.metrics import precision_score

    # truth = []
    # for prediction, example in zip(predictions, examples):
    #     truth.append(example["label"])
    return precision_score(examples, predictions, average="micro") * 100.0


def recall_metric(predictions, examples):
    assert len(predictions) == len(examples)
    from sklearn.metrics import recall_score

    # truth = []
    # for prediction, example in zip(predictions, examples):
    #     truth.append(example["label"])
    return recall_score(examples, predictions, average="micro") * 100.0
        
def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation + '，。')
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        text = ''.join(text)
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction, ground_truth):
    #prediction_tokens = normalize_answer(prediction).split()
    prediction_tokens = list(jieba.cut(normalize_answer(prediction)))
    prediction_tokens = [i for i in prediction_tokens if i]
    #ground_truth_tokens = normalize_answer(ground_truth).split()
    ground_truth_tokens = list(jieba.cut(normalize_answer(ground_truth)))
    ground_truth_tokens = [i for i in ground_truth_tokens if i]
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def my_cmrc_score(prediction, ground_truth):
    prediction = prediction[:max(100, int(len(ground_truth) * 1.25))]
    if ground_truth in prediction or prediction in ground_truth:
        return 1.0
    else:
        return f1_score(prediction, ground_truth)

def exact_match_score(prediction, ground_truth):
    return normalize_answer(prediction) == normalize_answer(ground_truth)


def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    if not ground_truths:
        return 0.0
    scores_for_ground_truths = []
    for ground_truth in ground_truths:

        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)


def qa_evaluate(predictions, examples, metric):
    '''
    examples: list(list(right answers))
    '''
    assert len(examples) == len(predictions)
    #tokenizer = get_tokenizer()

    score = 0.0
    score_list = []
    for example, prediction in zip(examples, predictions):
        ground_truths = [example]
        if ground_truths:
            tmp_score = metric_max_over_ground_truths(metric, prediction, ground_truths)

            # score += tmp_score
        else:
            tmp_score = 0.0
        score_list.append(tmp_score)
    score = 100.0 * score / len(predictions)
    return score_list
    # return score


qa_exact_match = functools.partial(qa_evaluate, metric=exact_match_score)
qa_f1 = functools.partial(qa_evaluate, metric=f1_score)
my_cmrc_eval = functools.partial(qa_evaluate, metric=my_cmrc_score)



if __name__=='__main__':
    scorer = EmbeddingSimilarity('/data/models/Xorbits/bge-m3')
    sentences_1 = ["", "我喜欢你","我喜欢你", "我喜欢你"]
    sentences_2 = ["你是我的最爱", "我不喜欢你", "我喜欢你","小明喜欢小芳"]
    
    # sentences_1 = ['亲，一包肠衣可以灌5斤左右肉，10斤装的可以灌8-10斤肉，根据个人手法会有所不同哦。', '亲,您可以选择购买两件哦,一件是肠衣,一件是调料', '根据个人手法的亲', '亲，这一包猪肠衣大概能灌4-5斤肉左右，根据不同的香肠类型和个人的手法，会有差异的哦。', '亲这边帮您备注了哈', '亲亲，我们是有货的，下单后48小时内发出哈~', '亲，已经付款了，我们会尽快为您发货哦~', '看选项哦亲，选项上面有写的就送，没有写的就不送哦', '亲,可能是打包的时候挤压导致的，不影响食用的哦。', '亲,很抱歉给您带来不好的体验,还请亲理解一下,您看为了给您有个好的购物体验,给您补偿2元可以吗。']
    # sentences_2 = ['猪肠衣五斤一包4-5米左右,口径3.8-4.0左右,灌大约4斤肉 10斤一包8-10米左右,口径3.8-4.0左右,灌大约8-10斤肉。', '分开拍下 拍完给您尽量一起发货', '猪肠衣五斤一包4-5米左右,口径3.8-4.0左右,灌大约4斤肉 10斤一包8-10米左右,口径3.8-4.0左右,灌大约8-10斤肉。', '5斤', '已备注', '能下单就是有的哈', '好的亲', '看选项哦亲,选项上面有写的就送,没有写的就不送哦', '亲,可能是打包的时候挤压导致的,不影响食用的哦', '实在抱歉亲这边权限只能2元呢']
    # sentences_1 = ["What is BGE M3?", "Defination of BM25"]
    # sentences_2 = ["BGE M3 is an embedding model supporting dense retrieval, lexical matching and multi-vector interaction.", 
    #             "BM25 is a bag-of-words retrieval function that ranks a set of documents based on the query terms appearing in each document"]
    
    # sim = scorer.scores(sentences_1, sentences_2, False)
    sim = scorer.scores(sentences_1, sentences_2)
    print(sim)

    """
    {
        'colbert': [0.6863591074943542, 0.6898072361946106], 
        'bge_v1.5': [0.6157, 0.682 ], 
        'reranker': [4.46484375, -3.33984375],  >0
        'rouge-1': [44.4444, 85.7143], 
        'rouge-2': [0.0, 40.0], 
        'rouge-l': [22.2222, 85.7143], 
        'bleu-4': [11.5216, 49.7609]
    }
    """
    
    
    '''
    {
        'my_cmrc_eval': (39.682539682539684, [0, 0.8571428571428571, 0.3333333333333333]), 
        'EM': (0.0, [False, False, False]), 
        'F1': (39.682539682539684, [0, 0.8571428571428571, 0.3333333333333333]), 
        'Accuracy': (0.0, [0, 0, 0]), 
        'Precision': 0.0, 
        'Recall': 0.0, 
        'F1_mul': 0.0, 
        'reranker': [-2.34765625, -3.33984375, -2.11328125], 'bleu-4': [0, 49.7609, 19.3769]}
    '''