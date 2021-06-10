from selenium.webdriver.common.by import By


class MainPageLocators:
    MAIN_HOME_LOC = (By.XPATH, "//a[text()='HOME']")
    MAIN_LOGOUT_LOC = (By.XPATH, "//a[text()='Logout']")

    MAIN_PYTHON_MENU_LOC = (By.XPATH, "//a[text()='Python']")
    MAIN_PYTHON_HISTORY_LOC = (By.XPATH, "//a[text()='Python history']")
    MAIN_PYTHON_FLASK_LOC = (By.XPATH, "//a[text()='About Flask']")

    MAIN_LINUX_MENU_LOC = (By.XPATH, "//a[text()='Linux']")
    MAIN_LINUX_CENTOS_LOC = (By.XPATH, "//a[text()='Download Centos7']")

    MAIN_NETWORK_MENU_LOC = (By.XPATH, "//a[text()='Network']")
    MAIN_NETWORK_NEWS_LOC = (By.XPATH, "//a[text()='News']")
    MAIN_NETWORK_DOWNLOAD_LOC = (By.XPATH, "//a[text()='Download']")
    MAIN_NETWORK_TCPDUMP_LOC = (By.XPATH, "//a[text()='Examples ']")

    MAIN_WHAT_API_LOC = (By.XPATH, "//div[text()='What is an API?']")
    MAIN_WHAT_API_URL_LOC = (By.XPATH, "//div[text()='What is an API?']/../figure")

    MAIN_FUTURE_LOC = (By.XPATH, "//div[text()='Future of internet']")
    MAIN_FUTURE_URL_LOC = (By.XPATH, "//div[text()='Future of internet']/../figure")

    MAIN_SMTP_LOC = (By.XPATH, "//div[text()='Lets talk about SMTP?']")
    MAIN_SMTP_URL_LOC = (By.XPATH, "//div[text()='Lets talk about SMTP?']/../figure")
