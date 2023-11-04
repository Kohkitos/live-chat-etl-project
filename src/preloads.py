from selenium.webdriver.chrome.options import Options
from pysentimiento import create_analyzer

# selenium's options
opciones=Options()

opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.headless=False
opciones.add_argument('--start-maximized')
opciones.add_argument('--incognito')

# nlp pipelines
analyzer = create_analyzer(task="sentiment", lang="es")
hate_speech_analyzer = create_analyzer(task="context_hate_speech", lang="es")