from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import json

tokenizer_race = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-race-QuestionAnswer")
model_race = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-race-QuestionAnswer")

tokenizer_squad = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")
model_squad = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-squad-QuestionAnswer")

path = os.sep.join([os.getcwd(), "datasets"])


def model_tokenizing(context, tokenizer, model):
    inputs = tokenizer(context, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)
    question_answer = tokenizer.decode(outputs[0], skip_special_tokens=False)
    question_answer = question_answer.replace(tokenizer.pad_token, "").replace(tokenizer.eos_token, "")
    print(question_answer.split(tokenizer.sep_token))
    try:
        question = question_answer.split(tokenizer.sep_token)[0]
        answer = question_answer.split(tokenizer.sep_token)[1]
    except IndexError:
        question = question_answer.split(tokenizer.sep_token)[0]
        answer = question
    return question, answer


def work_with_file(file: dict):
    qa_dict = {}
    for page in file:
        for value, key in file[page].items():
            qa_dict["id"] = value
            for v in key.values():
                qa_dict["question_race"], qa_dict["answer_race"] = model_tokenizing(v, tokenizer_race, model_race)
                qa_dict["question_squad"], qa_dict["answer_squad"] = model_tokenizing(v, tokenizer_squad, model_squad)
    return qa_dict


os.chdir(path)
files = [filename for filename in os.listdir(path) if ".json" in filename and "cleaned" in filename]
for filename in files:
    file = json.load(open(filename, "r"))
    res = work_with_file(file)
    with open("qa_pairs-" + filename, "a+") as f:
        json.dump(res, f, indent=1)
