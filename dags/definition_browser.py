from selenium import webdriver


# Definiamo il driver per accedere al browser Chrome.
def fun_definition_browser():
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://172.16.0.73:4444/wd/hub',
        options=options
    )
    return driver