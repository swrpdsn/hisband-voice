import os
from playwright.sync_api import sync_playwright, expect

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Get the absolute path to the index.html file
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    index_path = os.path.join(base_dir, "index.html")

    # Navigate to the local index.html file
    page.goto(f"file://{index_path}")

    # 1. Test Login Modal
    page.get_by_role("link", name="Log In").click()
    login_modal = page.locator("#loginModal")
    expect(login_modal).to_be_visible()

    # DEBUG: Print the HTML of the page to see what's visible
    print(page.content())

    # 2. Test switching to Signup mode
    page.get_by_role("button", name="Don’t have an account? Sign up").click()
    expect(login_modal.get_by_role("heading", name="Create Account")).to_be_visible()
    expect(login_modal.get_by_role("button", name="Sign Up")).to_be_visible()

    # 3. Test switching back to Login mode
    page.get_by_role("button", name="Already have an account? Log In").click()
    expect(login_modal.get_by_role("heading", name="Log In to Hisband Voice")).to_be_visible()

    # 4. Test Forgot Password Modal
    page.get_by_role("link", name="Forgot Password?").click()
    forgot_modal = page.locator("#forgotPasswordModal")
    expect(login_modal).to_be_hidden()
    expect(forgot_modal).to_be_visible()
    expect(forgot_modal.get_by_role("heading", name="Reset Password")).to_be_visible()

    # 5. Screenshot the final state
    page.screenshot(path="jules-scratch/verification/final_flow.png")

    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)