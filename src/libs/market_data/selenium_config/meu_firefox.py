from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def configura_webdriver_firefox():
    # Configurar as opções do Firefox para o modo headless e definir a pasta de download
    firefox_options = Options()
    firefox_options.headless = True  # Modo headless

    # Configurar a pasta de download e permitir o download automático
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference(
        "browser.download.dir", "/tmp/downloads"
    )  # Substitua pelo caminho da sua pasta
    firefox_options.set_preference("browser.download.useDownloadDir", True)
    firefox_options.set_preference(
        "browser.download.viewableInternally.enabledTypes", ""
    )
    firefox_options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/zip"
    )  # Substitua pelo tipo MIME do seu arquivo

    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--disable-gpu")

    # Criar uma instância do WebDriver do Firefox
    driver = webdriver.Firefox(options=firefox_options)
    return driver
