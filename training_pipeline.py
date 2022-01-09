
import shutil

import pickle
import json
from string import punctuation
import time
import os
import luigi
import pandas as pd
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import gzip
import argparse

from congrats_generator.utils import make_pandas_df, make_masked_col


class PrepareTexts(luigi.Task):
    """
    Prepare parced texts for converting into training data set objects.
    Make train.txt and test.txt files.
    """

    start = luigi.Parameter(time.time())
    my_mask = luigi.Parameter(False)

    def __init__(self, *args, my_mask=False, config_path='training_config.json', **kwargs):
        self.config = json.load(open('training_config.json'))
        self.mask = my_mask
        super().__init__(*args, **kwargs)


    def output(self):
        config = self.config
        target_1 = luigi.LocalTarget(config['TRAIN_DATA_PATH'])
        target_2 = luigi.LocalTarget(config['TEST_DATA_PATH'])

        return target_1 and target_2

    def run(self):
        config = self.config

        with open(config['CRAWL_TEXT_PATH']) as handler:
            full_text = handler.read()

        my_df = make_pandas_df(full_text)
        if self.mask:
            my_df = make_masked_col(my_df)
        my_df['Sum'] = [my_df['Title'].tolist()[i] + my_df['Content'].tolist()[i]
                        for i in range(len(my_df))]


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