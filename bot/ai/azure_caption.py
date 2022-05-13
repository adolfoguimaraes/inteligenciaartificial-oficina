from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

from bot.config import Config

# pip install azure-cognitiveservices-vision-computervision

class AzureCaption():

    def __init__(self):
        c = Config()
        self.region = "eastus"
        self.key = str(c.get_value('AZUREIMAGE','KEY'))
        self.endpoint = str(c.get_value('AZUREIMAGE', 'ENDPOINT'))
        

        self.credentials = CognitiveServicesCredentials(self.key)
        self.client = ComputerVisionClient(endpoint=self.endpoint,credentials=self.credentials)

    def caption_image(self, image):
        result = self.client.describe_image_in_stream(image)
        return result.captions[0].text

    

if __name__ == "__main__":

    azure_ = AzureCaption()

    with open("models/input/images/img1.jpg",'rb') as img:
        text_ = azure_.caption_image(img)
        print(text_)

