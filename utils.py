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