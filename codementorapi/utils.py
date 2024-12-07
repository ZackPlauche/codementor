import time
from playwright.sync_api import sync_playwright


def get_auth_tokens(username: str, password: str) -> tuple[str, str]:
    with sync_playwright() as p:
        # Set to True in production
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to login page
        page.goto('https://arc.dev/login?service=codementor', timeout=60000)

        # Fill in credentials
        page.fill('input[type="email"]', username)
        page.fill('input[type="password"]', password)

        # Implicit wait for one second
        time.sleep(1)

        # Submit the form
        page.click('form > button[type="submit"]')

        # Wait for login to complete and tokens to be set
        page.wait_for_url(
            'https://www.codementor.io/m/dashboard', timeout=120000)

        # Extract cookies
        cookies = page.context.cookies()
        access_token = next(
            (c['value'] for c in cookies if c['name'] == 'ACCESS_TOKEN'), None)
        refresh_token = next(
            (c['value'] for c in cookies if c['name'] == 'REFRESH_TOKEN'), None)

        browser.close()
        return access_token, refresh_token
