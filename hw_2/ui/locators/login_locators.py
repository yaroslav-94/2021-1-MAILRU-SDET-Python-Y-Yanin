from selenium.webdriver.common.by import By


class LoginPageLocators:

    BASE_ENTER_LOCATOR = (By.XPATH, "//div[text()='Войти']")
    BASE_LOGIN_LOCATOR = (By.XPATH, "//input[@name='email']")
    BASE_PASSWORD_LOCATOR = (By.XPATH, "//input[@name='password']")

    BASE_AUTH_LOCATOR = (By.XPATH, "//div[contains(@class, 'authForm-module-button')]")
    BASE_USER_INFO_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightWrap')]")
    BASE_LOGOUT_LOCATOR = (By.XPATH, "//a[text()='Выйти']")

    BASE_ERROR = (By.XPATH, "//div[text()='Error']")
    BASE_ERROR_MSG = (By.XPATH, "//div[text()='Invalid login or password']")
    BASE_ERROR_BADLOGIN_LOCATOR = (By.XPATH, "//div[text()='Введите email или телефон']")
