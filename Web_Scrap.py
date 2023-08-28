import asyncio
from os import path
import urllib.parse
from pyppeteer import launch


class InternshalaScraper:
    def __init__(self, root_url='https://internshala.com/internships/'):
        self.root_url = root_url

    async def launch_browser(self):
        if not hasattr(self, 'browser'):
            self.browser = await launch()
            # self.browser = await launch(headless=False)

    def make_url(self, keywords):
        return path.join(self.root_url, f"keywords-{urllib.parse.quote(keywords)}/")

    async def query(self, keywords, num):
        if not hasattr(self, 'browser'):
            await self.launch_browser()

        url = self.make_url(keywords)

        main_page = await self.browser.newPage()
        await main_page.goto(url)

        await (await self.browser.pages())[0].close()  # Close blank page

        links = await main_page.evaluate('''
            () => {
                let elements = document.querySelectorAll('.heading_4_5.profile');
                let links = []
                for(let i=0;i<''' + str(num) + ''';i++){
                    links.push(elements[i].firstElementChild.href);
                }
                return links
            }
        ''')
        # print(links)

        for link in links:
            page = await self.browser.newPage()
            await page.goto(link)

        await (await self.browser.pages())[0].close()  # Close main page

        pages = await self.browser.pages()
        all_skills = []
        for page in pages:
            skills = await self.get_skills(page)
            for skill in skills:
                all_skills.append(skill)

        return all_skills

    async def get_skills(self, page):
        return await page.evaluate('''
            () => {
                const headings = document.querySelectorAll('.section_heading')

                let children;
                for(let i = 0; i < headings.length; i++) {
                    if(headings[i].innerText == 'Skill(s) required') {
                        children = headings[i].nextElementSibling.children;
                    };
                }
                if(!children) return []
                let skills = []
                for(let i = 0; i < children.length; i++) {
                    skills.push(children[i].innerText)
                }

                return skills;
            }
        ''')

    async def cleanup(self):
        await self.browser.close()


async def scrape(query, num):
    iss = InternshalaScraper()
    skills = await iss.query(query, 5)
    # await asyncio.sleep(60)
    await iss.cleanup()
    return skills


def direct_scrape(query, num):
    return asyncio.get_event_loop().run_until_complete(scrape(query=query, num=num))

def Abhi(str1,a):
    data = direct_scrape(str1, a)
    return str(data);