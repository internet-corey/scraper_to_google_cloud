# stdlib
import time

# 3rd party
from pandas import DataFrame
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException


def remove_chars(value):
    '''removes fluff characters from specified string.
    :Args:
    - value - string from price web element
    :Returns:
    - value - the modified string as a float
    '''
    value = str(value).replace('$', '').replace('% OFF', '').replace(' ', '').replace('Fullpricewas\n', '')
    try:
        return float(value)
    except ValueError:
        return None


def scrape_xbox_sale(url):
    '''gets metadata from a specified xbox.com sale URL.
    :Args:
    - url - str
    '''

    def get_data(driver, button, platform):
        '''grabs metadata for specified platform titles'''
        button.click()
        time.sleep(2)
        nav_next_class = ''
        while 'pag-disabled' not in nav_next_class:
            time.sleep(1)
            box = driver.find_element_by_css_selector('.gameList')
            promos = box.find_elements_by_css_selector('.gameDivLink')
            for promo in promos:
                try:
                    title = promo.find_element_by_css_selector('.x1GameName').text
                except NoSuchElementException:
                    title = None
                try:
                    percent_off = remove_chars(promo.find_element_by_css_selector('.badge-silver').text)
                except NoSuchElementException:
                    percent_off = None
                try:
                    price = remove_chars(promo.find_element_by_css_selector('.c-price > s').text)
                    sale_price = remove_chars(promo.find_element_by_css_selector('.textpricenew').text)
                except NoSuchElementException:
                    price = None
                    sale_price = None
                data_dict = {
                    'date': date,
                    'title': title,
                    'platform': platform,
                    '%_off': percent_off,
                    'price': price,
                    'sale_price': sale_price,
                }
                data_dict_list.append(data_dict)
                print(
                    title,
                    percent_off,
                    price,
                    sale_price
                )

            # clicks next button until it is disabled on the last page
            try:
                nav_next_page = box.find_element_by_css_selector('.paginatenext')
                nav_next_class = nav_next_page.get_attribute('class')
                if 'pag-disabled' not in nav_next_class:
                    nav_next_page.click()

            # single-page list of items
            except ElementNotVisibleException:
                break

    date = time.strftime('%m-%d-%y')
    data_dict_list = []
    csv_columns = [
        'product_id',
        'date',
        'title',
        'platform',
        '%_off',
        'member_%_off',
        'price',
        'sale_price',
        'member_sale_price'
    ]
    driver = webdriver.Chrome(
        'C:/code/python/scraper_to_google_cloud/drivers/chromedriver.exe'
    )
    print('Scraping sale on xbox.com')
    driver.get(url)
    driver.implicitly_wait(5)

    # the total sale items are split into 3 possible platform categories
    xb1_games = driver.find_elements_by_link_text('All Xbox One Games')
    xb360_games = driver.find_elements_by_css_selector('.all360text')
    pc_games = driver.find_elements_by_link_text('All PC Games')
    time.sleep(1)

    # goes thru each present category and grabs data, updates dict_list
    if xb1_games:
        get_data(
            driver,
            xb1_games[0],
            'xb1'
        )
    if xb360_games:
        get_data(
            driver,
            xb360_games[0],
            '360'
        )
    if pc_games:
        get_data(
            driver,
            pc_games[0],
            'pc'
        )

    # dict list to dataframe then saves to CSV file
    ts_file = time.strftime('%m-%d-%y_%I-%M-%S', time.localtime())
    filename = f'xbox_sale_results_{ts_file}.csv'
    filepath = f'C:/code/python/scraper_to_google_cloud/{filename}'
    df = DataFrame(
        data_dict_list,
        columns=csv_columns
    )
    df.to_csv(
        filepath,
        index=False,
        encoding='utf-8'
    )
    return filepath
