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
        OffereInSpring = 1
    elif SPChance > 0:
        OffereInSpring = -1
    else:
        OffereInSpring = 0

    return OfferedInFall, OffereInSpring
        

def insert_terms(subject, terms):
    # Connect the cursor
    # conn = sqlite3.connect('college.db')
    # cursor = conn.cursor()

    # Insert terms into table
    fall, spring = determine_likelihood(terms)
    print(subject)
    print(fall, spring)
    # cursor.execute('''
    #     INSERT OR IGNORE INTO availability (class_id, semester_id)
    #     VALUES (?, ?)
    # ''', (subject, next_sem_chance))
    # print(subject, next_sem_chance)
    # conn.commit()
    # conn.close()

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
    insert_terms(subject + id, sorted_terms)

async def navigate(subject, id, semaphore, i):
    async with semaphore:
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                print(i)
                await page.goto('https://musis1.missouri.edu/gradedist/mu_grade_dist_intro.cfm', timeout=20000)  # 20 seconds timeout
                await page.select_option('select#subject', value=f'{subject}')
                await page.select_option('select#catalog_nbr', value=f'{id}')
                await page.click('input#submit')

                await scrape(subject, id, page)
                await page.wait_for_timeout(2000)  # Wait for 2 seconds

            except Exception as e:
                print(f"Skipping {i}")

            finally:
                await browser.close()

async def main(courses):
    semaphore = asyncio.Semaphore(10)
    tasks = []

    for i in range(0,19):
        try:
            tasks.append(asyncio.create_task(navigate(courses[i][0], courses[i][1], semaphore, i)))
        except Exception as e:
            print(f'Error at iteration {i}, skipping')
            continue
    await asyncio.gather(*tasks)

# get course data
conn = sqlite3.connect('college.db')
cursor = conn.cursor()
cursor.execute(''' SELECT dept, id FROM class WHERE dept = 'CMP_SC' ''')
courses = cursor.fetchall()
conn.commit()
conn.close()
asyncio.run(main(courses))