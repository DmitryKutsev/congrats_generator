import re

import pandas as pd
from natasha import (
    MorphVocab,
    NewsNERTagger,
    NamesExtractor,
    MorphVocab,
    Segmenter,
    NewsEmbedding,
    PER,
    Doc,
    ORG
)
from transformers import (TextDataset, DataCollatorForLanguageModeling,
                          GPT2LMHeadModel, TrainingArguments, Trainer, PreTrainedTokenizerBase)


def make_pandas_df(full_text: str) -> pd.core.frame.DataFrame:
    """
    Help function for PrepareTexts step in training_pipeline.
    Makes and returns pandas data frame.
    """

    titles_list = []
    congrats_list = []

    for letter in full_text.split('END'):
        letter = letter.replace('\n', '').replace('TITLE', '')

        if len(letter.split('CONTENT')) > 1:
            titles_list.append(letter.split('CONTENT')[0])
            congrats_list.append(letter.split('CONTENT')[1])

        data = {'Title': titles_list,
                'Content': congrats_list}

    my_df = pd.DataFrame(data)
    my_df['Sum'] = [my_df['Title'].tolist()[i] + my_df['Content'].tolist()[i] for i in range(len(my_df))]
    return my_df


def make_masked_col(my_df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    Help function for PrepareTexts step in training_pipeline.
    Makes NER, change nemed entities on MASK string. Returns changed data frame.
    """
    emb = NewsEmbedding()
    morph_vocab = MorphVocab()
    names_extractor = NamesExtractor(morph_vocab)
    ner_tagger = NewsNERTagger(emb)
    segmenter = Segmenter()
    masked_content = []

    for sent in my_df['Sum']:
        doc = Doc(sent)
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)

        for span in doc.spans:
            if span.type == PER or span.type == ORG:
                sent = sent.replace(span.text, 'MASK')

        masked_content.append(sent)

    my_df['Sum'] = masked_content
    return my_df


def build_dataset(df: pd.core.frame.DataFrame, dest_path: str):
    """
    Help function for PrepareTexts step in training_pipeline.
    Cleans and splits data, builds data set.
    """
    f = open(dest_path, 'w')
    data = ''
    summaries = df['Sum'].tolist()

    for summary in summaries:
        summary = str(summary).strip()
        summary = re.sub(r"\s", " ", summary)
        summary = re.sub(r"\n", "", summary)
        summary = re.sub(r"Статус материала Опубликован в разделе: Телеграммы", "", summary)
        summary = re.sub(r"Ссылка на материал:", "", summary)
        summary = re.sub(r"Текстовая версия:", "", summary)
        summary = re.sub(r"Ссылка на материал:", "", summary)
        summary = re.sub(r"([a-zA-Z]+)", "", summary)
        summary = re.sub(r"([0-9/*#@+]+)", "", summary)
        data += summary

        f.write(data)


def load_dataset(train_path: str, test_path: str, tokenizer: PreTrainedTokenizerBase) -> tuple:
    """
    Help function for LoadAndTrain step in training_pipeline.
    Makes TextDataset objects for test and train.
    """

    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=128)

    test_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=test_path,
        block_size=128)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )

    return train_dataset, test_dataset, data_collator


def my_train(train_dataset: TextDataset, test_dataset: TextDataset,
             data_collator: DataCollatorForLanguageModeling, output_dir_path: str) -> Trainer:
    """
    Help function for LoadAndTrain step in training_pipeline.
    Trains model.
    """
    model = GPT2LMHeadModel.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")

    training_args = TrainingArguments(
        output_dir=output_dir_path,
        overwrite_output_dir=True,
        # num_train_epochs=3,
        # per_device_train_batch_size=32,
        # per_device_eval_batch_size=64,
        num_train_epochs=40,
        per_device_train_batch_size=64,
        per_device_eval_batch_size=32,
        eval_steps=400,
        save_steps=150,
        warmup_steps=500,
        prediction_loss_only=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )
    return trainer
