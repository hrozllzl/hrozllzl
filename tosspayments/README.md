# TossPayments Mobile Web Automation (Android Chrome)

This project demonstrates Android mobile web automation for a TossPayments product page using Appium + Selenium + Python + Pytest.

## Prerequisites
- Python 3.13
- Android emulator or device connected via ADB
- Appium Server running at `http://localhost:4723`
- Chrome installed on the device/emulator

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration
Environment variables (optional):
- `APPIUM_SERVER_URL` (default: `http://localhost:4723`)
- `ANDROID_DEVICE_NAME` (default: `Android Emulator`)
- `PLATFORM_NAME` (default: `Android`)
- `AUTOMATION_NAME` (default: `UiAutomator2`)
- `BROWSER_NAME` (default: `Chrome`)
- `TARGET_URL` (default: the TossPayments product URL)
- `CHROMEDRIVER_AUTODOWNLOAD` (default: `true`)

## Run tests
From the `tosspayments` directory:
```bash
pytest -v tests/test_payment.py
```

The test will be skipped automatically if the Appium server is not reachable.

## Project Structure
- `config/` test configuration and capability builder
- `data/` test data in JSON
- `pages/` page objects and base page helpers
- `tests/` Pytest suite