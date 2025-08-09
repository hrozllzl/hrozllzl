from __future__ import annotations

from typing import Any, Dict

from .base_page import BasePage


class ClickProductPay(BasePage):
    """Page object to perform the product payment click flow."""

    def click_payment_button(self) -> bool:
        selectors: Dict[str, Any] = self.data.get("payment_button", {}) if self.data else {}
        tried = []

        element_id = selectors.get("id") or ""
        css_selector = selectors.get("css") or ""
        xpath = selectors.get("xpath") or ""

        try:
            if element_id:
                tried.append(f"id={element_id}")
                self.click_element_by_id(element_id)
                return True
        except Exception:
            pass

        try:
            if css_selector:
                tried.append(f"css={css_selector}")
                self.click_by_css(css_selector)
                return True
        except Exception:
            pass

        try:
            if xpath:
                tried.append(f"xpath={xpath}")
                self.click_by_xpath(xpath)
                return True
        except Exception:
            pass

        # Fallback: common Korean label for payment button
        try:
            tried.append("text=결제하기")
            self.click_by_text("결제하기")
            return True
        except Exception:
            pass

        raise RuntimeError(f"Failed to click payment button using selectors: {', '.join(tried) or 'none'}")

    def wait_after_click(self) -> bool:
        post = (self.data or {}).get("post_click", {})
        expect_text = post.get("expect_text_contains") or ""
        wait_seconds = int(post.get("wait_seconds", 8))
        if not expect_text:
            return True
        return self.wait_for_text(expect_text, timeout=wait_seconds)