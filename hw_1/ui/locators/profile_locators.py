from selenium.webdriver.common.by import By


PROFILE_INFO_LOCATOR = (By.XPATH, "//a[text()='Профиль']")
PROFILE_FIO_LOCATOR = (By.XPATH, "//div[@data-name='fio']/div/input")
PROFILE_PHONE_LOCATOR = (By.XPATH, "//div[@data-name='phone']/div/input")
PROFILE_EMAIL_LOCATOR = (By.XPATH, "//div[@data-class-name='AdditionalEmailRow']/div/div/div/input")
PROFILE_SAVE_LOCATOR = (By.XPATH, "//button[@data-class-name='Submit']")
