import os
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv


def get_auth_tokens(
    username: str | None = None,
    password: str | None = None
) -> tuple[str, str]:
    """Get Codementor authentication tokens using login credentials.
    
    Args:
        username: Codementor username, defaults to CODEMENTOR_USERNAME env var
        password: Codementor password, defaults to CODEMENTOR_PASSWORD env var
        
    Returns:
        Tuple of (access_token, refresh_token)
        
    Raises:
        ValueError: If username and/or password are not provided
    """
    load_dotenv(override=True)
    username = username or os.getenv('CODEMENTOR_USERNAME')
    password = password or os.getenv('CODEMENTOR_PASSWORD')

    missing = []
    if not username:
        missing.append('username')
    if not password:
        missing.append('password')
        
    if missing:
        missing_str = ' and '.join(missing)
        raise ValueError(
            f"Missing required {missing_str}. Either add CODEMENTOR_{missing_str.upper()} "
            f"to .env or pass {missing_str} parameter."
        )

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
