import asyncio
from playwright.async_api import async_playwright
import sqlite3
def determine_likelihood(terms):
    FSYears = []
    SPYears = []
    for term in terms:
        semester = term[:2]
        year = int(term[2:])
        if semester == 'FS':
            FSYears.append(year)
        elif semester == 'SP':
            SPYears.append(year)

    # calculate % just based on number of apperances
    if FSYears:
        FSChance = round((len(FSYears) / (max(FSYears) - min(FSYears) + 1)) * 100)
    else:
        FSChance = 0
    if SPYears:
        SPChance = round((len(SPYears) / (max(SPYears) - min(SPYears) + 1)) * 100)
    else:
        SPChance = 0

    if FSChance >= 90:
        OfferedInFall = 1
    elif FSChance > 0:
        OfferedInFall = -1
    else:
        OfferedInFall = 0

    if SPChance >= 90:
        OfferedInSpring = 1
    elif SPChance > 0:
        OfferedInSpring = -1
    else:
        OfferedInSpring = 0

    return OfferedInFall, OfferedInSpring

def insert_terms(subject, id, terms):
    # Connect the cursor
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()
    # Insert terms into table
    fall, spring = determine_likelihood(terms)
    print(subject, id)
    print(fall, spring)
    cursor.execute('''
        UPDATE class
        SET fall = ?, spring = ?
        WHERE id = ?
    ''', (fall, spring, subject + id))
    conn.commit()
    conn.close()

async def scrape(subject, id, page):
    terms_seen = set()
    await page.wait_for_selector('table tbody tr', timeout=10000)  # Wait until table rows are visible
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
    insert_terms(subject, id, sorted_terms)

async def navigate(subject, id, i):
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the URL
        await page.goto('https://musis1.missouri.edu/gradedist/mu_grade_dist_intro.cfm')

        # Interact with a dropdown and select an option
        try:
            print(i)
            await page.select_option('select#subject', value=f'{subject}')  # Select Subject
            await page.select_option('select#catalog_nbr', value=f'{id}')  # Select Number
        except Exception as e:
            print("Skipping Iteration")
            return
        # Interact with submit button
        await page.click('input#submit')

        # Scrape data
        await scrape(subject, id, page)

        # Wait for some action or verification
        await page.wait_for_timeout(2000)  # Wait for 2 seconds

        # Close browser
        await browser.close()

conn = sqlite3.connect('college.db')
cursor = conn.cursor()
cursor.execute(''' SELECT dept, id FROM class WHERE dept = 'INFOTC' ''')
courses = cursor.fetchall()
courses = [(dept, (id[len(dept):])) for dept, id in courses]
conn.commit()
conn.close()

for i in range(len(courses)):
    asyncio.run(navigate(courses[i][0], courses[i][1], i))
