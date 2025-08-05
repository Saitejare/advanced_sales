import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import os

URL = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
OUTPUT_DIR = "output"
TEXT_FILE = os.path.join(OUTPUT_DIR, "chapter.txt")
SCREENSHOT_FILE = os.path.join(OUTPUT_DIR, "chapter.png")

async def fetch_chapter(url=URL, output_dir=OUTPUT_DIR, retries=3):
    os.makedirs(output_dir, exist_ok=True)
    attempt = 0
    while attempt < retries:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                print(f"Navigating to {url} (attempt {attempt+1})...")
                await page.goto(url, timeout=30000)
                await page.wait_for_selector("body", timeout=10000)
                content = await page.locator("body").inner_text()
                # Clean text (basic)
                cleaned = content.strip()
                with open(TEXT_FILE, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                await page.screenshot(path=SCREENSHOT_FILE, full_page=True)
                print(f"Text saved to {TEXT_FILE}\nScreenshot saved to {SCREENSHOT_FILE}")
                await browser.close()
                return True
        except PlaywrightTimeoutError as e:
            print(f"Timeout error: {e}. Retrying...")
        except Exception as e:
            print(f"Error: {e}. Retrying...")
        attempt += 1
        await asyncio.sleep(2)
    print("Failed to fetch chapter after retries.")
    return False

if __name__ == "__main__":
    asyncio.run(fetch_chapter())
