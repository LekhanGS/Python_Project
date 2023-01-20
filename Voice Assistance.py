import speech_recognition as sr
import playsound
from gtts import gTTS
import os
from selenium import webdriver

num = 1
def assistant_speaks(output):
	global num

	num += 1
	print("Person : ", output)

	toSpeak = gTTS(text = output, lang ='en', slow = False)

	file = str(num)+".mp3"
	toSpeak.save(file)
	
	playsound.playsound(file, True)
	os.remove(file)



def get_audio():

	rObject = sr.Recognizer()
	audio = ''

	with sr.Microphone() as source:
		print("Speak...")
		
		# recording the audio using speech recognition
		audio = rObject.listen(source, phrase_time_limit = 5)
	print("Stop.") # limit 5 secs

	try:

		text = rObject.recognize_google(audio, language ='en-US')
		print("You : ", text)
		return text

	except:

		assistant_speaks("Could not understand your audio, PLease try again !")
		return 0

        
def process_text(input):
	try:
		if 'search' in input or 'play' in input:
			search_web(input)
			return

		elif "who are you" in input or "define yourself" in input:
			speak = '''Hello, I am Monk. Your personal Assistant.
			How can i help you Master? '''
			assistant_speaks(speak)
			return

		elif "who made you" in input or "created you" in input:
			speak = "I have been created by Lekhan."
			assistant_speaks(speak)
			return

		elif 'open' in input:
			open_application(input.lower())
			return

		else:

			assistant_speaks("I can search the web for you, Do you want to continue?")
			ans = get_audio()
			if 'yes' in str(ans) or 'yeah' in str(ans):
				search_web(input)
			else:
				return
	except :

		assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
		ans = get_audio()
		if 'yes' in str(ans) or 'yeah' in str(ans):
			search_web(input)


def search_web(input):

	driver = webdriver.Chrome()
	driver.implicitly_wait(1)
	driver.maximize_window()

	if 'youtube' in input.lower():

		assistant_speaks("Opening in youtube")
		indx = input.lower().split().index('youtube')
		query = input.split()[indx + 1:]
		driver.get("http://www.youtube.com/results?search_query =" + '+'.join(query))
		return

	elif 'wikipedia' in input.lower():

		assistant_speaks("Opening Wikipedia")
		indx = input.lower().split().index('wikipedia')
		query = input.split()[indx + 1:]
		driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
		return

	else:

		if 'google' in input:

			indx = input.lower().split().index('google')
			query = input.split()[indx + 1:]
			driver.get("https://www.google.com/search?q =" + '+'.join(query))

		elif 'search' in input:

			indx = input.lower().split().index('google')
			query = input.split()[indx + 1:]
			driver.get("https://www.google.com/search?q =" + '+'.join(query))

		else:

			driver.get("https://www.google.com/search?q =" + '+'.join(input.split()))

		return

def open_application(input):

	if "chrome" in input:
		assistant_speaks("Google Chrome")
		os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
		return

	elif "nfs" in input or "need for speed" in input:
		assistant_speaks("Opening Need For Speed")
		os.startfile(r'F:\Need for Speed Heat\NeedForSpeedHeat.exe')
		return

	elif "virtualmachine" in input:
		assistant_speaks("Opening Virtual Machine")
		os.startfile('C:\Program Files (x86)\VMware\VMware Workstation\vmware.exe')
		return

	elif "spotify" in input:
		assistant_speaks("Opening Spotify")
		os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')
		return

	else:
		assistant_speaks("Application not available")
		return
        
# Driver Code
if __name__ == "__main__":
	assistant_speaks("What's your name, Human?")
	#name ='Human'
	name = get_audio()
	assistant_speaks("Hello, " + str(name))
	
	while(1):

		assistant_speaks("What can i do for you?")
		text = get_audio().lower()

		if text == 0:
			continue

		if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
			assistant_speaks("Ok bye, "+ name+'.')
			break

		process_text(text)
