from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOG_WELCOME_LABEL_LOC = (By.XPATH, "//h3[text()='Welcome to the TEST SERVER']")
    LOG_INPUT_NAME_LOC = (By.XPATH, "//input[@id='username']")
    LOG_INPUT_PASS_LOC = (By.XPATH, "//input[@id='password']")
    LOG_ENTRY_LOC = (By.XPATH, "//input[@id='submit']")
    LOG_REGISTRATION_LOC = (By.XPATH, "//a[text()='Create an account']")
