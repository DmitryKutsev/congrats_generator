# congrats_generator
Generator of the congratulations via web interface with web-scraper.

The generator originally works with pretrained model 
[sberbank-ai/rugpt3small_based_on_gpt2](https://huggingface.co/sberbank-ai/rugpt3small_based_on_gpt2) 
downloaded from [huggingface.co](https://huggingface.co/).

The model fine tuning process is described in google colab notebook _congrats_generator/my_gpt3.ipynb_.


Web crawler is located in _congrats_generator/crawler_ directory. 

# Stages to build and start up the generator:

* Clone this repository into your local machine.
  * [Learn more about git clone](https://git-scm.com/docs/git-clone)

* Make directory for the model and specify model and tokenizer path in 
_congrats_generator/crawler/config.json_. 
Put the model according to the path.

* Build the app container. Start app process is realized with docker and docker compose
services which allow the app to be more scalable further.
You can use _docker-compose build_ command to build 
your app, and _docker-compose up_ to start the app.

   * [Docker run reference](https://docs.docker.com/engine/reference/run/)

   * [Docker-compose](https://docs.docker.com/compose/reference/)

   * [Docker-compose build](https://docs.docker.com/compose/reference/build/)

   * [Docker-compose up](https://docs.docker.com/compose/reference/up/)

