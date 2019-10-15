from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
import time

BK_URL = "https://www.evaluabk.com"
MC_URL = "http://mcexperiencia.cl"
WD_URL = "https://www.mywendysfeedback.com/chl"
PH_URL = "https://s.pizzahutsurvey.com/chl"
DD_URL = "https://www.talktodunkin.com/chl"

def setup_chrome_driver(options=None):
    if not options:
        options = webdriver.ChromeOptions()
        chrome_prefs = {}
        options.experimental_options["prefs"] = chrome_prefs
        # chrome_prefs["profile.default_content_settings"] = {"images": 2}
        # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    return webdriver.Chrome(options=options)


class DriverController:
    def __init__(self, homepage):
        self.driver = setup_chrome_driver()
        self.root = homepage

    def wait_until_loaded(self, xpath, message="Correctly loaded"):
        seconds = 15
        try:
            WebDriverWait(self.driver, seconds).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            print(message)
        except TimeoutException:
            print("Time exceeded! (still waiting for page to load)")

    def switch_to_frame(self):
        self.wait_until_loaded("//iframe")
        frame = self.find_xpath("//iframe")
        self.driver.switch_to.frame(frame)

    def switch_to_main(self):
        self.driver.switch_to.default_content()

    def find_id(self, element_id):
        return self.driver.find_element_by_id(element_id)

    def find_css(self, element_css, multi=False):
        if multi:
            return self.driver.find_elements_by_css_selector(element_css)
        return self.driver.find_element_by_css_selector(element_css)

    def find_xpath(self, element_xpath, multi=False):
        if multi:
            return self.driver.find_elements_by_xpath(element_xpath)
        return self.driver.find_element_by_xpath(element_xpath)

    def find_class(self, element_class, multi=False):
        if multi:
            return self.driver.find_elements_by_class_name(element_class)
        return self.driver.find_element_by_class_name(element_class)

    def navigate(self, route="/"):
        url = self.root + route
        self.driver.get(url)


class Bot:
    def __init__(self, url, brand="", button_id="", code_id="", initial_id=""):
        self.url = url
        self.controller = DriverController(self.url)
        self.button_id = button_id
        self.code_id = code_id
        self.brand = brand
        self.initial_id = initial_id
        self.name = "{} Survey Answerer Bot".format(self.brand).strip()
        print("Initializing {}".format(self.name))

    def fill_initial_input(self):
        fake_value = randint(950000000000, 999999999999) # idk why it works
        initial_input = self.controller.find_id(self.initial_id)
        initial_input.send_keys(fake_value)

    def initial_input_present(self): 
        try:
          self.controller.find_id(self.initial_id)
          return True
        except:
          return False

    def answer_survey(self, fill_form=True):
        self.controller.navigate()
        button = self.get_form_button()
        while button:
            if(self.initial_id != ""):
              input_present = self.initial_input_present()
              if (input_present):
                self.fill_initial_input()
            time.sleep(0.1)
            button.click()
            if fill_form:
                self.fill_form_page()
            button = self.get_form_button()
        self.code = self.get_code()

    def get_form_button(self):
        try:
            return self.controller.find_id(self.button_id)
        except:
            return None

    def fill_form_page(self):
        # TODO: Should generate random values and insert them
        # in every form input
        # For McDonald's form, it needs to load precalculated answers per page
        pass

    def get_code(self):
        try:
            code_container = self.controller.find_class(self.code_id)
            code_text = code_container.text
            code = code_text.split(" ")[-1]
            return code
        except:
            return None

    def retrieve_code(self):
        print("{} code: {}".format(self.brand, self.code))


class BurgerKingBot(Bot):
    def __init__(self):
        super().__init__(BK_URL, "Burger King", "NextButton", "ValCode")


class WendysBot(Bot):
    def __init__(self):
        super().__init__(WD_URL, "Wendy's", "NextButton", "ValCode")

class PizzaHutBot(Bot):
    def __init__(self):
        super().__init__(PH_URL, "Pizza Hut", "NextButton", "ValCode", "InputCouponNum")


class DunkinDonutsBot(Bot):
    def __init__(self):
        super().__init__(DD_URL, "Dunkin Donuts", "NextButton", "ValCode")


class McDonaldsBot(Bot):
    def __init__(self):
        super().__init__(MC_URL, "McDonald's", "movenextbtn")

    def get_page_inputs(self):
        try:
            return self.controller.find_class("form-control", multi=True)
        except:
            return None

    def get_page_selects(self):
        try:
            return self.controller.find_css("select", multi=True)
        except:
            return None

    def get_form_button(self):
        try:
            return self.controller.find_id(self.button_id)
        except:
            return None

    def answer_survey(self, fill_form=True):
        self.controller.navigate()
        self.controller.switch_to_frame()
        button = self.get_form_button()
        button.click()
        # TODO: Fill the inputs according to their types
        # OBS: some values can't be random
        # inputs = self.get_page_inputs()
        # selects = self.get_page_selects()
        # button = self.get_form_button()


bot = BurgerKingBot()
bot.answer_survey(fill_form=False)
bot.retrieve_code()

# bot = PizzaHutBot()
# bot.answer_survey(fill_form=False)
# bot.retrieve_code()

# bot = DunkinDonutsBot()
# bot.answer_survey(fill_form=False)
# bot.retrieve_code()

# bot = WendysBot()
# bot.answer_survey(fill_form=False)
# bot.retrieve_code()

# bot = McDonaldsBot()
# bot.answer_survey()
# bot.find_page_inputs()
# bot.retrieve_code()
