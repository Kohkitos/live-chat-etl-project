from selenium.webdriver.chrome.options import Options
from pysentimiento import create_analyzer

# selenium's options
OPCIONES=Options()

OPCIONES.add_experimental_option('excludeSwitches', ['enable-automation'])
OPCIONES.add_experimental_option('useAutomationExtension', False)
OPCIONES.headless=False
OPCIONES.add_argument('--start-maximized')
OPCIONES.add_argument('--incognito')

# nlp pipelines
ANALYZER = create_analyzer(task="sentiment", lang="es")
HATE_SPEECH = create_analyzer(task="context_hate_speech", lang="es")
