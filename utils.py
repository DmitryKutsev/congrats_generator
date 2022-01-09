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
from transformers import TextDataset, DataCollatorForLanguageModeling
from sklearn.model_selection import train_test_split

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

    for sent in my_df['Content']:
      doc = Doc(sent)
      doc.segment(segmenter)
      doc.tag_ner(ner_tagger)

      for span in doc.spans:
          if span.type == PER or span.type == ORG:
              sent = sent.replace(span.text, 'MASK')

      masked_content.append(sent)

    my_df['Content'] = masked_content
    return my_df


def clean_and_split_data(my_df):
    train_test_ratio = 0.9
    df_train, df_test = train_test_split(my_df, train_size=train_test_ratio, random_state=1)


def load_dataset(train_path, test_path, tokenizer):
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