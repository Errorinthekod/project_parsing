from bs4 import BeautifulSoup as BS
import requests
# from multiprocessing import Pool



def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    return None


def get_glide_link(html):
    links =[]
    soup = BS(html,'html.parser')
    posts = soup.find('div', class_='ty-tygh   bp-tygh-container')
    post = posts.find('div', class_='content_abt__ut2_grid_tab_2258_138')
    for p in post:
        item_info = p.find('div', class_='ut2-gl__body')
        title = item_info.find('div', class_='ut2-gl__name') #name
        link = title.find('a').get('href')
        full_link = link
        links.append(full_link)
    return links






def get_data(html):
    soup = BS(html, 'html.parser')
    product_blocks = soup.find('div', class_='ty-product-list__item')
    for block in product_blocks:
        titlee = block.find('a', class_='ty-product-list__title')
        titlee = titlee.text.strip() if titlee else 'Неизвестно'

        # brand = block.find('a', class_='ty-product-list__brand')
        # brand = brand.text.strip() if brand else 'Неизвестно'
        
        # articule = block.find('div', class_='ty-product-list__sku')
        # articule = articule.text.strip() if articule else 'Неизвестно'

        # price_before_discount = block.find('span', class_='ty-list-price ty-nowrap')
        # price_before_discount = price_before_discount.text.strip() if price_before_discount else 'Неизвестно'
        
        # price_after_discount = block.find('span', class_='ty-price-num ty-price-num--new')
        # price_after_discount = price_after_discount.text.strip() if price_after_discount else 'Неизвестно'
        
        # availability = block.find('div', class_='ty-qty-in-stock ty-control-group__item')   #ty-product-list__availability
        # availability = availability.text.strip() if availability else 'Неизвестно'
        
        # delivery_info = block.find('div', class_='ty-wysiwyg-content ab-mb-style-presets')
        # delivery_info = delivery_info.text.strip() if delivery_info else 'Неизвестно'
        
        # description = block.find('div', class_='ty-product-list__description')
        # description_text = description.text.strip() if description else 'Неизвестно'
        
        # tech_chars = block.find('div', class_='ty-product-list__features')
        # tech_chars_text = tech_chars.text.strip() if tech_chars else 'Неизвестно'


    
    
    
        articule = block.find('div', class_='ut2-pb__sku')
        articule = articule.text.strip() if articule else 'Неизвестно'

        price_1 = block.find('div', class_='ty-list-price ty-nowrap')
        price_1 = price_1.text.strip() if price_1 else 'Неизвестно'

        price_2 =  block.find('div', class_='ut2-pb__price-actual')
        price_2 = price_2.text.strip() if  price_2 else 'Неизвестно'

        available = block.find('div', class_='cm-reload-bigpicture_565 stock-wrap')
        available = available.text.strip() if  available else 'Неизвестно'

        brand_name = block.find('div', class_='c')
        brand_name = brand_name.text.strip() if  brand_name else 'Неизвестно'

        deliv_text = block.find('div', class_='ty-wysiwyg-content ab-mb-style-presets')
        deliv_text = deliv_text.text.strip() if deliv_text else 'Неизвестно'
    
        description_text = block.find_all('p', class_='MsoNormal')
        deliv_text = deliv_text.text.strip() if deliv_text else 'Неизвестно'
        print (description_text)
        
        tech_char = block.find('div', class_='ty-product-feature')
        deliv_text = deliv_text.text.strip() if deliv_text else 'Неизвестно'
        print (tech_char)

        accessories = block.find_all('div', class_='ty-product-list clearfix')
        deliv_text = deliv_text.text.strip() if deliv_text else 'Неизвестно'
        print (accessories)


        data = {
            'title': titlee,
            'price_1': price_1,
            'price_2': price_2,
            'articule': articule,
            'available': available,
            'brand': brand_name,
            'delivery': deliv_text,
            'description': description_text,
            'tech-characteristics': tech_char,
            'accessories': accessories,
        }
        return data
    


def last_page(html):
    soup = BS(html, 'html.parser')
    page = soup.find('ul', class_='pagination')
    pages = page.find_all('a',class_='page-link')
    last_page = pages[-1].get('data-page')

    return int(last_page)

from openpyxl import Workbook

def save_to_exel(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Название'
    sheet['B1'] = 'Цена до скидки'
    sheet['C1'] = 'Цена после скидки'
    sheet['D1'] = 'Артикул (код)'
    sheet['E1'] = 'Наличие'
    sheet['F1'] = 'Бренд'
    sheet['G1'] = 'Информация о доставке'
    sheet['H1'] = 'Описание'
    sheet['I1'] = 'Технические характеристики'
    sheet['J1'] = 'Аксессуары'
    
    for i,item in enumerate(data,2):
        sheet[f'A{i}'] = item['ut2_pb__title']
        sheet[f'B{i}'] = item['price_1']
        sheet[f'C{i}'] = item['price_2']
        sheet[f'D{i}'] = item['articule']
        sheet[f'E{i}'] = item['available']
        sheet[f'F{i}'] = item['brand_name']
        sheet[f'G{i}'] = item['deliv_text']
        sheet[f'H{i}'] = item['description_text']
        sheet[f'I{i}'] = item['tech_char']
        sheet[f'J{i}'] = item['accessories']
    
    workbook.save('shor_data.xlsx')

   

def parsing(page_num):
    URL = 'https://bangbang.kz/'
    page_url = URL + f'page={page_num}'
    page_html = get_html(page_url)
    links = get_glide_link(page_html)
    all_data = []  # Список для хранения всех данных
    for link in links:
        posts_links = get_html(url=link)
        if posts_links:  # Проверяем, успешно ли получен HTML
            data = get_data(html=posts_links)
            all_data.append(data)  # Добавляем данные в список

    save_to_exel(all_data)  # Сохраняем все данные в Excel

def main():
    URL = 'https://bangbang.kz/'
    html = get_html(url=URL)
    links = get_glide_link(html=html)
    get_data(html)
    
  
        
if __name__ == '__main__':
    main()



# print('Hello!')