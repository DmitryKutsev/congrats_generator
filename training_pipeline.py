
import shutil

import pickle
import json
from string import punctuation
import time
import os
import luigi
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import gzip
import argparse

from congrats_generator.utils import make_pandas_df, make_masked_col, build_dataset


class PrepareTexts(luigi.Task):
    """
    Prepare parced texts for converting into training data set objects.
    Make train.txt and test.txt files.
    """

    start = luigi.Parameter(time.time())
    my_mask = luigi.Parameter(False)

    def __init__(self, *args, my_mask=False, config_path='data_config.json', **kwargs):
        self.config = json.load(open(config_path))
        self.mask = my_mask
        super().__init__(*args, **kwargs)


    def run(self):
        config = self.config

        with open(config['CRAWL_TEXT_PATH']) as handler:
            full_text = handler.read()

        my_df = make_pandas_df(full_text)
        if self.mask:
            my_df = make_masked_col(my_df)
        my_df['Sum'] = [my_df['Title'].tolist()[i] + my_df['Content'].tolist()[i]
                        for i in range(len(my_df))]

        train_test_ratio = config['TRAIN_TEST_RATIO']
        df_train, df_test = train_test_split(my_df, train_size=train_test_ratio, random_state=1)
        build_dataset(df_train, config['TEST_DATA_PATH'])
        build_dataset(df_test, config['TRAIN_DATA_PATH'])


class LoadAndTrain(luigi.Task):
    """
    Load data set into objects for training. Train and save model.
    """
    def output(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':

    my_parser = argparse.ArgumentParser(description='Command line argumenst of the Luigi pipeline')

    my_parser.add_argument('-mask',
                           metavar='mask',
                           type=bool,
                           required=False,
                           help='If we want to replace Named Entities with MASK string, '
                                'set this parameter to mask=True. It has mask=False value by default')


    args = my_parser.parse_args()
    mask = args.mask

    luigi.build([
                    PrepareTexts(luigi.Task, my_mask=mask)
                ],
                detailed_summary=True,
                local_scheduler=True,
    )