import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Функция для получения HTML кода страницы
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

# Функция для парсинга главной страницы и извлечения данных о товарах
def parse_main_page(url):
    html = get_html(url)
    if not html:
        print("Не удалось загрузить страницу")
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Выводим заголовок страницы и первые 500 символов HTML для проверки
    print("HTML заголовок:", soup.title.string)
    print("HTML начало:", html[:500])
    
    products_data = []

    # Найти все блоки товаров на главной странице
    product_blocks = soup.find_all('div', class_='ty-tygh bp-tygh-container is-ready')
    
    if not product_blocks:
        print("Не найдены блоки товаров.")
        return []

    print(f"Найдено {len(product_blocks)} блоков товаров.")
    
    for block in product_blocks:
        title = block.find('a', class_='ty-product-list__title')
        title = title.text.strip() if title else 'Неизвестно'

        brand = block.find('a', class_='ty-product-list__brand')
        brand = brand.text.strip() if brand else 'Неизвестно'
        
        articule = block.find('div', class_='ty-product-list__sku')
        articule = articule.text.strip() if articule else 'Неизвестно'

        price_before_discount = block.find('span', class_='ty-list-price ty-nowrap')
        price_before_discount = price_before_discount.text.strip() if price_before_discount else 'Неизвестно'
        
        price_after_discount = block.find('span', class_='ty-price-num ty-price-num--new')
        price_after_discount = price_after_discount.text.strip() if price_after_discount else 'Неизвестно'
        
        availability = block.find('div', class_='ty-qty-in-stock ty-control-group__item')   #ty-product-list__availability
        availability = availability.text.strip() if availability else 'Неизвестно'
        
        delivery_info = block.find('div', class_='ty-wysiwyg-content ab-mb-style-presets')
        delivery_info = delivery_info.text.strip() if delivery_info else 'Неизвестно'
        
        description = block.find('div', class_='ty-product-list__description')
        description_text = description.text.strip() if description else 'Неизвестно'
        
        tech_chars = block.find('div', class_='ty-product-list__features')
        tech_chars_text = tech_chars.text.strip() if tech_chars else 'Неизвестно'
        
        products_data.append({
            'title': title,
            'brand': brand,
            'articule': articule,
            'price_before_discount': price_before_discount,
            'price_after_discount': price_after_discount,
            'availability': availability,
            'delivery_info': delivery_info,
            'description': description_text,
            'technical_characteristics': tech_chars_text
        })

    return products_data

# Функция для сохранения данных в Excel
def save_to_excel(data, filename='products.xlsx'):
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Название'
    sheet['B1'] = 'Бренд'
    sheet['C1'] = 'Артикул'
    sheet['D1'] = 'Цена до скидки'
    sheet['E1'] = 'Цена по скидке'
    sheet['F1'] = 'Наличие'
    sheet['G1'] = 'Информация о доставке'
    sheet['H1'] = 'Описание'
    sheet['I1'] = 'Технические характеристики'
    
    for i, item in enumerate(data, 2):
        sheet[f'A{i}'] = item['title']
        sheet[f'B{i}'] = item['brand']
        sheet[f'C{i}'] = item['articule']
        sheet[f'D{i}'] = item['price_before_discount']
        sheet[f'E{i}'] = item['price_after_discount']
        sheet[f'F{i}'] = item['availability']
        sheet[f'G{i}'] = item['delivery_info']
        sheet[f'H{i}'] = item['description']
        sheet[f'I{i}'] = item['technical_characteristics']
    
    workbook.save(filename)
    print(f"Данные сохранены в {filename}")

def main():
    base_url = 'https://bangbang.kz/'
    products_data = parse_main_page(base_url)
    
    if products_data:
        save_to_excel(products_data)
    else:
        print("Нет данных для сохранения")

if __name__ == '__main__':
    main()


