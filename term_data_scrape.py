import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape(page):
    terms_seen = set()
    rows = await page.query_selector_all('table tbody tr')
    await page.wait_for_load_state('networkidle', timeout=10000)  # Wait for the network to be idle (10 seconds)

    for row in rows:
        term = await row.query_selector('td:nth-child(1)')
        if term:
            term_text = await term.inner_text()
            if term_text.startswith(('SP', 'FS')):
                if term_text not in terms_seen:
                    terms_seen.add(term_text)
    
    sorted_terms = sorted(terms_seen, key=lambda term: int(term[2:]), reverse=True)
    print(sorted_terms)

async def run(subject, id):
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigate to the URL
        await page.goto('https://musis1.missouri.edu/gradedist/mu_grade_dist_intro.cfm')

        # Interact with a dropdown and select an option
        await page.select_option('select#subject', value=f'{subject}')  # Select Subject
        await page.select_option('select#catalog_nbr', value=f'{id}')  # Select Number

        # Interact with submit button
        await page.click('input#submit')

        # Scrape data
        await scrape(page)

        # Wait for some action or verification
        await page.wait_for_timeout(2000)  # Wait for 2 seconds

        # Close browser
        await browser.close()

asyncio.run(run('CMP_SC', '1050'))

