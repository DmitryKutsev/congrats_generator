from transformers import pipeline
from transformers import GPT2Tokenizer
import configparser



class Generator:
    """
    Class for congratulations generation. Handles model specified in config.
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.tokenizer_path = str(self.config['MODELS']['TokenizerPath'])
        self.model_path = str(self.config['MODELS']['ModelPath'])
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.tokenizer_path)
        self.speech_generator = pipeline('text-generation',
                               model=self.model_path,
                               tokenizer=self.tokenizer,
                               max_length=500)

    def generate_congrats(self, my_person: str) -> str:
        """
        Generates congratulations to input person.
        """
        return self.speech_generator(my_person)
