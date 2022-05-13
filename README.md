# Oficina de Inteligência Artificial

## Roteiro

1. Apresentação
2. Introdução teórica
3. Bot simples 
4. Modelo para Análise de Sentimento
5. Modelo para Descrição de Imagens 
6. Utilizando GPT-3 com a API da OpenAI
7. Incrementando e testando o bot
8. Encerramento


## Apresentação 

Meu nome é Adolfo Guimarães. 

- 🌍 Brasileiro/Nordestino/Sergipano
- 📚 Professor e Pesquisador na área de Ciência da Computação
- 💻 #python
- ❤ Inteligência artificial
- 👊 Acredito que a tecnologia (e a Inteligência Artificial) pode e deve ser utilizada em prol da sociedade. 

## Introdução Teórica

<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vQfg_MGKF5uTWFl45vkVGdswiUggcawSvUJFgYom5WlDGa8q1vC9EABB7TrFJ0Svy7k3Qu-Sd6uJeZE/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>

## Bot Simples

Para interagir com os modelos de Machine Learning vamos utilizar um bot no telegram. Para criar o bot você deve ter o telegram instalado e criar um bot a partir do usuário `BotFather`: https://t.me/BotFather. Siga o passo a passo e salve o token disponibilizado após a criação no arquivo `config.ini`. 

O bot está implementado na pasta `/bot/`. Na raiz do projeto, utilize o comando `python -m bot.run` para executar o bot. Acesse o bot criado no telegram para interagir com ele.

## Modelo de Análise de Sentimento

Para o modelo de análise de sentimento, vamos treinar um modelo de análise de sentimento em inglês baseado em textos que foram pré-classificados. Para isso, vamos utilizar uma biblioteca em Python, a `scikit-learn`: https://scikit-learn.org/. Os detalhes do modelo e o passo a passo para o treinamento está no arquivo `notebooks/AnaliseDeSentimento.ipynb`.

## Modelo para Descrição de Imagens 

Para o modelo de descrição de imagens vamos utilizar a nuvem da Azure. Ela possui um serviço de reconhecimento de imagem e podemo acessa-lo a partir de uma conta gratuita de estudante. No minicurso será mostrado como criar e acessar os recurso utilizando o e-mail insitucional. 

## Utilizando a GPT-3 com a API do OpenAI.

Nosso último modelo de Machine Learning vai ser o de conversação utilizando a API da OpenAI. Essa API dá acesso 

## Incrementando e testando o bot.

## Encerramento.