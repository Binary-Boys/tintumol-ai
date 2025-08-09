import pygame
import speech_recognition as sr
from gtts import gTTS
import playsound
import google.generativeai as genai
import os
from PIL import Image
import requests
import tempfile


# ---------- SETTINGS ----------
GEMINI_API_KEY = "AIzaSyDPk8JBAJXS3LZr9wiDOXL5utCxwWiQsb8"  # <-- Replace with your key
AVATAR_IMAGE = "avatar.png"  # Cute female avatar image
VOICE_LANG = "en"
pygame.init()

# ---------- INIT GEMINI ----------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")  # or gemini-1.5-pro

# ---------- PYGAME WINDOW ----------
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cute AI Avatar Chat")

# Load avatar image
avatar_img = pygame.image.load(AVATAR_IMAGE)
avatar_img = pygame.transform.scale(avatar_img, (300, 300))

# ---------- FUNCTIONS ----------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"👤 You: {text}")
        return text
    except:
        return None

def get_ai_response(prompt):
    print("🤖 Thinking...")
    prompt = "Answer the following in Malayalam, and make sure the response is dumb and funny:" + prompt
    response = model.generate_content(prompt)
    return response.text.strip()

def speak(text):
    # Generate Malayalam speech
    tts = gTTS(text, lang="ml")
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name
    tts.save(filename)
    
    # Play with pygame
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Wait until done playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Cleanup
    os.remove(filename)



def draw_chat(user_text, ai_text):
    screen.fill((255, 255, 255))
    screen.blit(avatar_img, (100, 50))

    font = pygame.font.SysFont("Arial", 20)
    if user_text:
        user_surface = font.render(f"You: {user_text}", True, (0, 0, 0))
        screen.blit(user_surface, (20, 400))
    if ai_text:
        ai_surface = font.render(f"AI: {ai_text}", True, (0, 0, 255))
        screen.blit(ai_surface, (20, 450))

    pygame.display.update()

# ---------- MAIN LOOP ----------
running = True
user_message, ai_message = "", ""

while running:
    draw_chat(user_message, ai_message)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Press SPACE to talk
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        user_message = listen()
        if user_message:
            ai_message = get_ai_response(user_message)
            speak(ai_message)

pygame.quit()
