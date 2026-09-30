import asyncio
from playwright.async_api import async_playwright

async def collect_jobs(url: str, title_selector: str, company_selector: str, limit: int = 10):
    """Collect visible job cards from a permitted public page using explicit selectors."""
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True)
        page=await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        titles=await page.locator(title_selector).all_inner_texts()
        companies=await page.locator(company_selector).all_inner_texts()
        await browser.close()
    return [{"title":t.strip(),"company":companies[i].strip() if i<len(companies) else "Unknown"} for i,t in enumerate(titles[:limit])]

def collect_jobs_sync(*args, **kwargs):
    return asyncio.run(collect_jobs(*args, **kwargs))
