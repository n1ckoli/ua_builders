import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pyshorteners import Shortener
import xlsxwriter

# список главных url по которым идет парсинг
BASE_URLS = [
    "https://meget.kiev.ua/stroitelnie-kompanii-zastroyshiki/", # 1
    "https://meget.kiev.ua/stroitelnie-kompanii/2/?catalog_operation=builder", # 2
    "https://meget.kiev.ua/stroitelnie-kompanii/3/?catalog_operation=builder", # 3
    "https://meget.kiev.ua/stroitelnie-kompanii/4/?catalog_operation=builder", # 4
    "https://meget.kiev.ua/stroitelnie-kompanii/5/?catalog_operation=builder", # 5
    "https://meget.kiev.ua/stroitelnie-kompanii/6/?catalog_operation=builder", # 6
    "https://meget.kiev.ua/stroitelnie-kompanii/7/?catalog_operation=builder", # 7
    "https://meget.kiev.ua/stroitelnie-kompanii/8/?catalog_operation=builder", # 8
    "https://meget.kiev.ua/stroitelnie-kompanii/9/?catalog_operation=builder", # 9
    "https://meget.kiev.ua/stroitelnie-kompanii/10/?catalog_operation=builder", # 10
    "https://meget.kiev.ua/stroitelnie-kompanii/11/?catalog_operation=builder", # 11
    "https://meget.kiev.ua/stroitelnie-kompanii/12/?catalog_operation=builder", # 12
    "https://meget.kiev.ua/stroitelnie-kompanii/13/?catalog_operation=builder", # 13
    "https://meget.kiev.ua/stroitelnie-kompanii/14/?catalog_operation=builder", # 14
    "https://meget.kiev.ua/stroitelnie-kompanii/15/?catalog_operation=builder", # 15
    "https://meget.kiev.ua/stroitelnie-kompanii/16/?catalog_operation=builder", # 16
    "https://meget.kiev.ua/stroitelnie-kompanii/17/?catalog_operation=builder", # 17
    "https://meget.kiev.ua/stroitelnie-kompanii/18/?catalog_operation=builder", # 18
]
HEADERS = {"User-Agent": UserAgent().random}
OUT_XLSX_FILENAME = 'parsed_data.xlsx'

async def parse_page(session, url):
    parsed_data = []
    async with session.get(url, headers=HEADERS) as response:
        r = await response.text()
        soup = BS(r, "html.parser")
        items = soup.find_all("a", {"class": "bc-link"})
        for item in items:
            name = item.find("span", {"class": "bc-name"}).text.strip()
            phone = item.find("span", {"class": "bc-phone"}).text.strip()
            parsed_data.append({'name': name, 'phone': phone})
    return parsed_data

async def main():
    async with aiohttp.ClientSession() as session:
        all_parsed_data = []
        for url in BASE_URLS:
            parsed_data = await parse_page(session, url)
            all_parsed_data.extend(parsed_data)
    
    return all_parsed_data

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main())
    
    # Write data to Excel
    workbook = xlsxwriter.Workbook(OUT_XLSX_FILENAME)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    
    headers = ['Name', 'Phone']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold)
    
    for row, item in enumerate(data, start=1):
        worksheet.write(row, 0, item['name'])
        worksheet.write(row, 1, item['phone'])
    
    workbook.close()
    print(f'Data written to {OUT_XLSX_FILENAME}')
