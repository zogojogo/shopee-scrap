from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
import json
from faker import Faker

# set up the web driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# setup faker
fake = Faker('id_ID')

# navigate to shopee.co.id and search for the search term
base_url = 'https://shopee.co.id'
category_url = f'{base_url}/Cincin-cat.11042921.11042922'
driver.get(category_url)

# wait for the search results to load
count = 1
products = []
for i in range (0, 10):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.col-xs-2-4.shopee-search-item-result__item')))

    total_page_height = driver.execute_script("return document.body.scrollHeight")
    browser_window_height = driver.get_window_size(windowHandle='current')['height']
    current_position = driver.execute_script('return window.pageYOffset')
    while total_page_height - current_position > browser_window_height:
        time.sleep(0.1)
        driver.execute_script(f"window.scrollTo({current_position}, {browser_window_height + current_position});")
        current_position = driver.execute_script('return window.pageYOffset')

    product_elements = driver.find_elements(by=By.CSS_SELECTOR, value='.col-xs-2-4.shopee-search-item-result__item')

    for product in product_elements:
        name = WebDriverWait(product, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._1yN94N.WoKSjC._2KkMCe')))
        name_text = name.text
        image = WebDriverWait(product, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.B0Ze3i.wAkToc')))
        image_url = image.get_attribute('src')
        category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.shopee-category-list__sub-category.shopee-category-list__sub-category--active'))).get_attribute('href')
        category_id = category.split('.')[-1]
        description = fake.text(
            max_nb_chars=200,
            ext_word_list=None
        )

        product_data = {'id': count, 'title': name_text, 'image_urls': [image_url], 'category_ids' : [category_id], 'description': description}
        products.append(product_data)
        count += 1
    driver.get(f'{category_url}?page={i+1}')

# close the web driver
driver.quit()

# return the product data
json_object = json.dumps(products, indent = 4)
json_output = {
    "count": len(products),
    "products": products,
}

with open("data.json", "w") as outfile:
    json.dump(json_output, outfile, indent=4)