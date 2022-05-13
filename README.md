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

## Introdução Teórica

[Slides]

## Bot Simples

Para interagir com os modelos de Machine Learning vamos utilizar um bot no telegram. Para criar o bot você deve ter o telegram instalado e criar um bot a partir do usuário `BotFather`: https://t.me/BotFather. Siga o passo a passo e salve o token disponibilizado após a criação no arquivo `config.ini`. 

O bot está implementado na pasta `/bot/`. Na raiz do projeto, utilize o comando `python -m bot.run` para executar o bot. Acesse o bot criado no telegram para interagir com ele.

## Modelo de Análise de Sentimento

Para o modelo de análise de sentimento, vamos treinar um modelo de análise de sentimento em inglês baseado em textos que foram pré-classificados. Para isso, vamos utilizar uma biblioteca em Python, a `scikit-learn`: https://scikit-learn.org/. Os detalhes do modelo e o passo a passo para o treinamento está no arquivo `notebooks/AnaliseDeSentimento.ipynb`.

## Modelo para Descrição de Imagens 

## Utilizando a GPT-3 com a API do OpenAI.

## Incrementando e testando o bot.

## Encerramento.