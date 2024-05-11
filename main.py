import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import pygame


# FUNÇÃO PARA CAPTAR AUDIO DO MICROFONE
def ouvir_microfone():

  microfone = sr.Recognizer()

  with sr.Microphone() as source:
      
      microfone.adjust_for_ambient_noise(source)

      print("Diga alguma coisa: ")

      audio = microfone.listen(source)

  try:
      frase = microfone.recognize_google(audio, language='pt-BR')
      print(f"Voce disse: {frase}")
      return frase
  except sr.UnknownValueError:
      print("Não entendi.")


# FUNÇÃO CHATBOT PARA RESPONDER QUESTOES
def chatbot(n, prompt):
    if (n == 0):
      response = chat.send_message(prompt)
      #print(f"-> {response.text}\n"
      speaker.say(response.text)
      speaker.runAndWait()
    else:
      response = chat.send_message(prompt)
      #print(f"-> {response.text}\n"
      speaker.say(response.text)
      speaker.runAndWait()


# PYGAME
pygame.init()
janela = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Liz")

mic_turn = pygame.image.load("Liz\c_turn.png")
mic_turn_rect = mic_turn.get_rect()

liz_turn = pygame.image.load("Liz\liz_turn.png")
liz_turn_rect = liz_turn.get_rect()

#   PYTTSX3
speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[2].id)


# INICIANDO O AI
genai.configure(api_key=API_KEY)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

chat = model.start_chat(history=[])

pular = 0
#  RODANDO O APLICATIVO
while True:
   for event in pygame.event.get():
    
    # INSTRUÇÃO
    if pular == 0:
      prompt = "você se chama Liz. é uma assistente social. você não fala que é uma assistente social. você ajuda as pessoas apenas conversando. você pode usar historias, contos, cronicas para ajudar as pessoas a entenderem a realidade caso ela queiram. pra saber se elas querem, pergunte. não faça respostas grandes, se limite a no maximo 2 linhas. nunca use emojis ou figuras nas conversas. o seu criador é desconhecido. caso a pessoa insista em um tipo de conversa, então converse sobre aquilo com ela. comece dizendo: Olá, eu sou Liz. Sou uma assistente virtual, mas fui feita para ajudar as pessoas com os problemas delas. Eu espero que você não tenha nenhum problema, caso tenha, eu estou aqui. Bem... se quiser falar comigo, é só ver se aparece um microfone no meio da tela. Se tiver o microfone, é só apertar P, esperar uns segundos, e dizer o que quiser, aqui você não preisa guardar seus segredos. Se quiser encerrar nossa conversa, é só dizer tchau."
      janela.blit(liz_turn, liz_turn_rect)
      pygame.display.update()
      chatbot(0, prompt)
      pular+=1

    if event.type == pygame.QUIT or prompt == "tchau":
      quit()

    if event.type == pygame.KEYDOWN:
       if event.key == pygame.K_p:
          prompt = ouvir_microfone()
          janela.blit(liz_turn, liz_turn_rect)
          pygame.display.update()
          chatbot(1, prompt)

    janela.blit(mic_turn, mic_turn_rect)
    pygame.display.update()
