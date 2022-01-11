
import json
import time
import luigi
from sklearn.model_selection import train_test_split
from transformers import GPT2Tokenizer
import argparse
from congrats_generator.utils import (make_pandas_df, make_masked_col,
                                      build_dataset, load_dataset, my_train)


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

        train_test_ratio = config['TRAIN_TEST_RATIO']
        random_state = config['RANDOM_STATE']
        df_train, df_test = train_test_split(my_df, train_size=train_test_ratio, random_state=random_state)
        build_dataset(df_train, config['TEST_DATA_PATH'])
        build_dataset(df_test, config['TRAIN_DATA_PATH'])


class LoadAndTrain(luigi.Task):
    """
    Load data set into objects for training. Train and save model.
    """

    start = luigi.Parameter(time.time())

    def __init__(self, *args, data_config_path='data_config.json',
                 train_config_path='training_config.json', **kwargs):
        self.train_config = json.load(open(train_config_path))
        self.data_config = json.load(open(data_config_path))
        super().__init__(*args, **kwargs)

    def output(self):
        pass

    def run(self):
        train_path = self.data_config['TRAIN_DATA_PATH']
        test_path = self.data_config['TEST_DATA_PATH']
        pretrained_model = self.train_config['PRETRAINED_MODEL']
        output_dir_path = self.train_config['SAVE_DIR_PATH']
        tokenizer = GPT2Tokenizer.from_pretrained(pretrained_model)

        train_dataset, test_dataset, data_collator = load_dataset(train_path, test_path, tokenizer)
        trainer = my_train(train_dataset, test_dataset, data_collator, output_dir_path)
        trainer.save_model()


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
                    PrepareTexts(my_mask=True),
                    # LoadAndTrain()
                ],
                detailed_summary=True,
                local_scheduler=True,
    )