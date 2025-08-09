import os
from typing import Dict, Any


CONFIG: Dict[str, Any] = {
    "APPIUM_SERVER_URL": os.getenv("APPIUM_SERVER_URL", "http://localhost:4723"),
    "PLATFORM_NAME": os.getenv("PLATFORM_NAME", "Android"),
    "AUTOMATION_NAME": os.getenv("AUTOMATION_NAME", "UiAutomator2"),
    "DEVICE_NAME": os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
    "BROWSER_NAME": os.getenv("BROWSER_NAME", "Chrome"),
    "TARGET_URL": os.getenv(
        "TARGET_URL",
        "https://buy.tosspayments.com/products/nyBhBXtobs?shopId=testjinimarket2",
    ),
    "NEW_COMMAND_TIMEOUT": int(os.getenv("NEW_COMMAND_TIMEOUT", "120")),
    # Appium vendor-prefixed capabilities
    "CHROMEDRIVER_AUTODOWNLOAD": os.getenv("CHROMEDRIVER_AUTODOWNLOAD", "true").lower()
    in {"1", "true", "yes"},
}


def build_android_chrome_options():
    """Return UiAutomator2Options configured for Android Chrome web testing."""
    try:
        from appium.options.android import UiAutomator2Options
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Appium 'UiAutomator2Options' is not available. Install appium-python-client."
        ) from exc

    options = UiAutomator2Options()
    # W3C capabilities
    options.set_capability("platformName", CONFIG["PLATFORM_NAME"])
    options.set_capability("browserName", CONFIG["BROWSER_NAME"])
    # Appium vendor-prefixed capabilities
    options.set_capability("appium:automationName", CONFIG["AUTOMATION_NAME"])
    options.set_capability("appium:deviceName", CONFIG["DEVICE_NAME"])
    options.set_capability("appium:newCommandTimeout", CONFIG["NEW_COMMAND_TIMEOUT"])

    # Useful quality-of-life capability to avoid manual chromedriver management
    options.set_capability(
        "appium:chromedriverAutodownload", CONFIG["CHROMEDRIVER_AUTODOWNLOAD"]
    )

    # Avoid resetting Chrome state across runs (optional, can be toggled via env later)
    if os.getenv("APPIUM_NO_RESET", "true").lower() in {"1", "true", "yes"}:
        options.set_capability("appium:noReset", True)

    return options