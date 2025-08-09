from __future__ import annotations

import os
from pathlib import Path
from typing import Generator
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

import pytest
from appium import webdriver
from selenium.common.exceptions import WebDriverException

from config.config import CONFIG, build_android_chrome_options
from data.json_loader import load_json
from pages.click_product_pay import ClickProductPay


def _appium_status_url(server_url: str) -> str:
    return server_url.rstrip("/") + "/status"


def is_appium_available(server_url: str) -> bool:
    try:
        with urlopen(_appium_status_url(server_url), timeout=3) as resp:  # type: ignore[arg-type]
            return 200 <= getattr(resp, "status", 200) < 300
    except (URLError, HTTPError):
        return False


@pytest.fixture(scope="session")
def driver() -> Generator:
    server_url = CONFIG["APPIUM_SERVER_URL"]

    if not is_appium_available(server_url):
        pytest.skip(f"Appium server is not available at {server_url}. Skipping mobile web tests.")

    options = build_android_chrome_options()

    try:
        driver = webdriver.Remote(command_executor=server_url, options=options)
    except WebDriverException as exc:
        pytest.skip(f"Failed to create Appium driver: {exc}")
        return  # for type checkers

    yield driver

    try:
        driver.quit()
    except Exception:
        pass


def test_click_payment_flow(driver):
    target_url = CONFIG["TARGET_URL"]
    driver.get(target_url)

    # Load test data JSON
    project_root = Path(__file__).resolve().parents[1]
    json_path = project_root / "data" / "click_product_pay_data.json"
    data = load_json(json_path)

    page = ClickProductPay(driver, data)

    assert page.click_payment_button() is True
    assert page.wait_after_click() is True