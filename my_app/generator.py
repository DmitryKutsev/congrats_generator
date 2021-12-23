from transformers import pipeline
from transformers import GPT2Tokenizer



class Generator:
    """
    Class for congratulations generation. Handles model, which is hardcoded in class.
    """

    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
        self.speech_generator = pipeline('text-generation',
                               model='./models/gpt3_22.12-2',
                               tokenizer=self.tokenizer,
                               max_length=500)

    def generate_congrats(self, my_person: str) -> str:
        """
        Generates congratulations to input person.
        """
        return self.speech_generator(my_person)