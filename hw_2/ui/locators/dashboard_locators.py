from selenium.webdriver.common.by import By


class DashboardPageLocators:

    DASHBOARD_COMPANY_LOCATOR = (By.XPATH, "//a[text()='Кампании']")
    DASHBOARD_AUDITORY_LOCATOR = (By.XPATH, "//a[text()='Аудитории']")
    DASHBOARD_BALANCE_LOCATOR = (By.XPATH, "//a[text()='Баланс']")
    DASHBOARD_STATS_LOCATOR = (By.XPATH, "//a[text()='Статистика']")

    DASHBOARD_PRO_LOCATOR = (By.XPATH, "//a[text()='PRO']")
    DASHBOARD_PROFILE_LOCATOR = (By.XPATH, "//a[text()='Профиль']")
    DASHBOARD_HELP_LOCATOR = (By.XPATH, "//a[text()='Помощь']")

    DASHBOARD_USER_INFO_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightWrap')]")
    DASHBOARD_LOGOUT_LOCATOR = (By.XPATH, "//a[text()='Выйти']")
