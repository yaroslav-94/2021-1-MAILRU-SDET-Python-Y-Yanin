from selenium.webdriver.common.by import By
from ui.locators.login_locators import LoginPageLocators


class CompanyLocators(LoginPageLocators):

    COMPANY_MAIN_LOCATOR = (By.XPATH, "//a[text()='Кампании']")
    COMPANY_CREATE_NEW_LOCATOR = (By.XPATH, "//a[text()='Создайте рекламную кампанию']")
    COMPANY_CREATE_IN_LIST_LOCATOR = (By.XPATH, "//div[text()='Создать кампанию']")
    COMPANY_AIM_CREATING_LOCATOR = (By.XPATH, "//div[text()='Охват']")

    COMPANY_AIM_URL_LOCATOR = (By.XPATH, "//input[contains(@class, 'mainUrl')]")
    COMPANY_NAME_NEW_LOCATOR = (By.XPATH, "//div[contains(@class, 'campaign-name')]//input")
    COMPANY_FORMAT_AD_LOCATOR = (By.XPATH, "//div[@id='patterns_4']")
    COMPANY_UPLOAD_FILE_LOCATOR = (By.XPATH, "//input[@data-test='image_240x400']")

    COMPANY_SAVE_IMAGE_LOCATOR = (By.XPATH, "//input[@type='submit']")
    COMPANY_CHOOSE_IN_LIST_PATH = "//a[text()='{}']/..//input[@type='checkbox']"
    COMPANY_STATUS_LIST_LOCATOR = (By.XPATH, "//div[contains(@class, 'statusFilter')]//div[@data-test='select']")

    COMPANY_CHOOSE_STATUS_LIST_PATH = "//li[@title='{}']"
    COMPANY_ACTIONS_LOCATOR = (By.XPATH, "//span[text()='Действия']")
    COMPANY_DELETE_LOCATOR = (By.XPATH, "//li[@title='Удалить']")
