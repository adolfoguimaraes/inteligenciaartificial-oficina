import os
from numpy import dtype 
import openai

from bot.config import Config

class OpenAiConversation():

    def __init__(self):
        c = Config()

        openai.api_key = c.get_value("OPENAI", "SECRETKEY")

        if c.get_value("OPENAI", "ACTIVE") == "0":
            self.status = False
        else: 
            self.status = True 
        

        self.conversationTopics = {
            'starwars': {
                'file_id': 'file-ruakplgi1ad3SkF2osaaD6Sg',
                'example_context': "Star Wars is a famous movie's serie. There are a lot of fans around the world",
                'examples': [["What is Star Wars?","A famous movie's serie."]]
            }
        }

    def getStatus(self):
        return self.status

    def makeQuestion(self, input_file, question, example_context, examples):

        try:
            return_ = openai.Answer.create(
                search_model="davinci",
                model="davinci",
                question=question,
                file=input_file,
                examples_context=example_context,
                examples=examples,
                max_tokens=50,
                stop=["\n", "<|endoftext|>"]
            )
        except Exception as e:
            print("Não foi possível responder a sua pergunta.")
            print(e)
            return_ = []

    
        return return_['answers'][0]

    def getTopics(self): 
        return list(self.conversationTopics.keys())

    def sendQuestion(self, topic, question):

        if (self.status):

            file_ = self.conversationTopics[topic]['file_id']
            example_context = self.conversationTopics[topic]['example_context']
            examples = self.conversationTopics[topic]['examples']

            return self.makeQuestion(file_, question, example_context, examples)
        else:

            return "This service is inactive."


    

        




if __name__ == "__main__":

    openai_ = OpenAiConversation()
    print(openai_.sendQuestion("starwars", "What you know about Anakin Sakywalker?"))
    

