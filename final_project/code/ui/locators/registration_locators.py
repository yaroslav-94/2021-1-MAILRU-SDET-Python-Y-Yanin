from selenium.webdriver.common.by import By


class RegistrationPageLocators:
    REG_TITLE_LOC = (By.XPATH, "//h3[text()='Registration']")
    REG_USERNAME_LOC = (By.XPATH, "//input[@id='username']")
    REG_EMAIL_LOC = (By.XPATH, "//input[@id='email']")
    REG_PASSWORD_LOC = (By.XPATH, "//input[@id='password']")
    REG_REP_PASS_LOC = (By.XPATH, "//input[@id='confirm']")
    REG_ACCEPT_RULES_LOC = (By.XPATH, "//input[@id='term']")
    REG_REGISTER_LOC = (By.XPATH, "//input[@id='submit']")
    REG_LOGIN_LOC = (By.XPATH, "//a[text()='Log in']")

