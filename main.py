from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from adj_dunc import qua_str,fiyat_duzenle
from selenium.webdriver.support import expected_conditions as EC
import seaborn as sns

#DEFS
start_time = time.time()

PATH = 'C:\Program Files (x86)\chromedriver.exe'  # Path of chrome driver

driver = webdriver.Chrome(PATH)

driver.get('http://www.migros.com.tr')  # Url
time.sleep(1)

menu_main_div = driver.find_element_by_class_name(
    'header-menu-bar')  # Find the main categories

menu = menu_main_div.find_elements_by_class_name(
    'header-menu-bar-list-item')  # Find the main categories

links = []
texts = []

# Make two arrays for main category links and texts.
for i in menu[2:-1]:
    texts.append(i.text)
    links.append(i.find_element_by_css_selector('a').get_attribute('href'))

if links != None:
    print('Ready')

# Create a DataFrame for records.
df = pd.DataFrame([], columns=['Category', 'Sub Category', 'Product', 'Price'])

dum = 0
for k, j in zip(links, texts):
    print("**********", j, "**************")  # Main Category Name

    driver.get(k)  # Go to next main category

    # Adjusting the submenu texts and values
    sub_menu_text = [
        sbt.text for sbt in driver.find_elements_by_class_name('category-filter ')]
    sub_menu_links = [sbl.get_attribute(
        'href') for sbl in driver.find_elements_by_class_name('category-filter ')]
    sub_menu_texts = list(
        map(lambda x: ' '.join(x.split()[:-1]), sub_menu_text))
    # Quantity for each sub category
    qua = list(map(lambda x: x.split()[-1], sub_menu_text))

    for o, m, qq in zip(sub_menu_texts, sub_menu_links, qua):
        print("#####", o, "#####")  # Print subcategory
        driver.get(m)  # Go next subcategory

        # Define a variable to check there is a next page in product page.
        lmt = 0
        while lmt < 1:
            try:
                try:
                    alt_main = driver.find_element_by_class_name(
                        'sub-category-product-list')

                    sub_menu = alt_main.find_elements_by_class_name('list')

                    # Scrapping the products.
                    for i in sub_menu:
                        price_tag = i.find_element_by_class_name('price-tag')
                        price = price_tag.find_element_by_class_name('value').text
                        product = i.find_element_by_css_selector('h5').text

                        df = df.append(  # Append values into a dataframe
                            {'Category': j, 'Sub Category': o, 'Product': product, 'Price': price}, ignore_index=True)
                        dum+=1
                    driver.find_element_by_class_name('pag-next').click()  # Click next button below page.

                except StaleElementReferenceException:
                    time.sleep(1)
                    i = 0

            except NoSuchElementException:

                lmt += 1  # Increase value if there is no next button in product page.
                break



        print(f"Totaly {dum} record has been recorded.")
    print("***" * 10)
    print("DONE!")
driver.close()

df['Price']=list(map(fiyat_duzenle,df['Price']))

writer = pd.ExcelWriter('data.xlsx')
df.to_excel(writer)
writer.save()
print("All Done!")
print("--- %s seconds ---" % (time.time() - start_time))