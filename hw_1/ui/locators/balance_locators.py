from selenium.webdriver.common.by import By


BALANCE_LOCATOR = (By.XPATH, "//a[text()='Баланс']")
BALANCE_ADD_MONEY_LOCATOR = (By.XPATH, "//span[text()='Пополнение счёта']")
BALANCE_AUTO_ADD_MONEY_LOCATOR = (By.XPATH, "//span[text()='Автопополнение']")
BALANCE_OPERATION_LOCATOR = (By.XPATH, "//span[text()='Поступления и списания']")
