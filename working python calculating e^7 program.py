import math
import pyttsx3

engine = pyttsx3.init()

limit = math.exp(7)
result = f"The limit is: {limit}"

print(result)
engine.say(result)
engine.runAndWait()
