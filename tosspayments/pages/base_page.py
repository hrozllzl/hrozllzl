from __future__ import annotations

from typing import Any, Dict, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base page object with convenience helpers for mobile web automation."""

    def __init__(self, driver: WebDriver, data: Optional[Dict[str, Any]] = None, timeout: int = 15) -> None:
        self.driver = driver
        self.data = data or {}
        self.timeout = timeout

    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout)

    def find_element_by_id(self, element_id: str):
        return self._wait().until(EC.presence_of_element_located((By.ID, element_id)))

    def click_element_by_id(self, element_id: str) -> None:
        element = self._wait().until(EC.element_to_be_clickable((By.ID, element_id)))
        self._safe_click(element)

    def click_by_css(self, css_selector: str) -> None:
        element = self._wait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        self._safe_click(element)

    def click_by_xpath(self, xpath: str) -> None:
        element = self._wait().until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self._safe_click(element)

    def click_by_text(self, button_text: str) -> None:
        xpath = f"//button[contains(normalize-space(.), '{button_text}')]"
        self.click_by_xpath(xpath)

    def _safe_click(self, element) -> None:
        # Scroll into view and click to increase reliability on mobile web
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        except Exception:
            pass
        element.click()

    def wait_for_text(self, text: str, timeout: Optional[int] = None) -> bool:
        try:
            self._wait(timeout).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(normalize-space(.), '{text}')]")))
            return True
        except TimeoutException:
            return False