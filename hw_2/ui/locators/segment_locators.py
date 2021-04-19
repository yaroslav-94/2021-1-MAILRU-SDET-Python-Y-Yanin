from selenium.webdriver.common.by import By
from ui.locators.login_locators import LoginPageLocators


class SegmentLocators(LoginPageLocators):

    SEGMENT_MAIN_LOCATOR = (By.XPATH, "//a[text()='Аудитории']")
    SEGMENT_SETTING_LOCATOR = (By.XPATH, "//input[contains(@class, 'adding-segments')]")
    SEGMENT_ADD_NEW_LOCATOR = (By.XPATH, "//div[text()='Добавить сегмент']")

    SEGMENT_CREATE_LOCATOR = (By.XPATH, "//div[text()='Создать сегмент']")
    SEGMENT_CREATE_EMPTY_LOCATOR = (By.XPATH, "//a[text()='Создайте']")
    SEGMENT_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'segment-name')]//input")

    SEGMENT_CHOOSE_IN_LIST_PATH = "//a[text()='{}']/../../..//input[@type='checkbox']"
    SEGMENT_ACTIONS_LOCATOR = (By.XPATH, "//span[text()='Действия']")
    SEGMENT_DELETE_LOCATOR = (By.XPATH, "//li[@title='Удалить']")
