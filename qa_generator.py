from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import json
import torch
device = torch.device("cuda")
tokenizer_race = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-race-QuestionAnswer")
model_race = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-race-QuestionAnswer").to(device)

tokenizer_squad = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")
model_squad = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer").to(device)

path = os.sep.join([os.getcwd(), "datasets"])


def model_tokenizing(context, tokenizer, model):
    inputs = tokenizer(context, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_length=1024)
    question_answer = tokenizer.decode(outputs[0], skip_special_tokens=False)
    question_answer = question_answer.replace(tokenizer.pad_token, "").replace(tokenizer.eos_token, "")
    print(question_answer.split(tokenizer.sep_token))
    try:
        print(context)
        question = question_answer.split(tokenizer.sep_token)[0]
        answer = question_answer.split(tokenizer.sep_token)[1]
    except IndexError:
        question = question_answer.split(tokenizer.sep_token)[0]
        answer = question
    return question, answer


def work_with_file(file: dict):
    qa_dict = {}
    for page in file:
        for key, value in file[page].items():
            question_race, answer_race = model_tokenizing(value['text'], tokenizer_race, model_race)
            question_squad, answer_squad = model_tokenizing(value['text'], tokenizer_squad, model_squad)
            qa_dict[key] = {"question_race": question_race, "answer_race": answer_race,
                             "question_squad": question_squad, "answer_squad": answer_squad,
                             "text": value['text']}
    return qa_dict


os.chdir(path)
files = [filename for filename in os.listdir(path) if ".json" in filename and "cleaned" in filename]
for filename in files:
    file = json.load(open(filename, "r"))
    res = work_with_file(file)
    with open("qa_pairs-" + filename, "a+") as f:
        json.dump(res, f, indent=1)
