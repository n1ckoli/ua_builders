import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pyshorteners import Shortener
import xlsxwriter

BASE_URL = "https://meget.kiev.ua/stroitelnie-kompanii/2/?catalog_operation=builder"
HEADERS = {"User-Agent": UserAgent().random}
OUT_XLSX_FILENAME = 'parsed_data.xlsx'

async def main():
    parsed_data = []
    
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            r = await response.text()
            soup = BS(r, "html.parser")
            items = soup.find_all("a", {"class": "bc-link"})
            for item in items:
                name = item.find("span", {"class": "bc-name"}).text.strip()
                phone = item.find("span", {"class": "bc-phone"}).text.strip()
                parsed_data.append({'name': name, 'phone': phone})
    
    return parsed_data

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
