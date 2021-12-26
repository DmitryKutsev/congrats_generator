
import shutil
import luigi
import pickle
import json
from string import punctuation
import time, os
import pandas as pd
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
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
import gzip
import argparse

from congrats_generator.utils import make_pandas_df, make_masked_col


class PrepareTexts(luigi.Task):

    config = luigi.Parameter(json.load(open('training_config.json.json')))
    mask = luigi.Parameter(default=False)
    start = luigi.Parameter(time.time())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def output(self):
        config = self.config
        target_1 = config['TRAIN_DATA_PATH']
        target_2 = config['TEST_DATA_PATH']
        return True if luigi.LocalTarget(target_1) and luigi.LocalTarget(target_2) else False

    def run(self):
        config = self.config

        with open(config['CRAWL_TEXT_PATH']) as handler:
            full_text = handler.read()

        my_df = make_pandas_df(full_text)
        if self.mask:
            my_df = make_masked_col(my_df)
        my_df['Sum'] = [my_df['Title'].tolist()[i] + my_df['Content'].tolist()[i]
                        for i in range(len(my_df))]




if __name__ == '__main__':

    my_parser = argparse.ArgumentParser(description='Command line argumenst of the Luigi pipeline')

    my_parser.add_argument('-mask',
                           metavar='mask',
                           type=bool,
                           required=False,
                           help='If we want to replace Named Entities with MASK string, '
                                'set this parameter to mask=True. It has mask=False value by default')


    args = my_parser.parse_args()
    mask = args.mask if args.mask else False

    luigi.build([
                    PrepareTexts(luigi.Task, mask=mask)
                ],
                detailed_summary=True,
                scheduler_port=8082,
                scheduler_host='localhost')