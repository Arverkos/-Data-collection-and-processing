import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['posts_db']
posts_db = db.posts


def tf_get_post_info(key_word, max_scroll_range=2):

    DRIVER_PATH = 'chromedriver.exe'

    url = 'https://vk.com/tokyofashion'

    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(url)

    find_url = driver.find_element_by_class_name('ui_tab_search').get_attribute('href')
    driver.get(find_url)
    find_el = driver.find_element_by_id('wall_search')
    find_el.send_keys(key_word)
    time.sleep(2)
    find_el.send_keys(Keys.ENTER)

    for scroll in range(max_scroll_range):
        time.sleep(1)
        try:
            button = driver.find_element_by_class_name('JoinForm__notNow')
            if button:
                button.click()
        except Exception as e:
            print(e)
        finally:
            driver.find_element_by_tag_name('html').send_keys(Keys.END)
            time.sleep(1)
            wall = driver.find_element_by_id('fw_load_more')
            stop_scroll = wall.get_attribute('style')
            if stop_scroll == 'display: none;':
                break

    posts_list = driver.find_elements_by_xpath('//div[@class="_post_content"]//..//img[contains(@alt, "Tokyo Fashion")]/../../..')

    posts_info_list = []

    for post in posts_list:
        post_info = {}

        post_info['date'] = post.find_element_by_class_name("rel_date").text
        post_info['body'] = post.find_element_by_class_name('wall_post_text').text
        post_info['url'] = post.find_element_by_class_name('post_link').get_attribute('href')
        post_info['likes'] = post.find_elements_by_class_name('like_button_count')[0].text
        post_info['shares'] = post.find_elements_by_class_name('like_button_count')[1].text

        posts_info_list.append(post_info)

    return posts_info_list


def add_posts_info_to_db(db, posts_info_list):
    for el in posts_info_list:
        db.update_one({"$and": [{'date': {"$eq": el["date"]}}, {'url': {"$eq": el["url"]}}]},
                      {"$set": el}, upsert=True)
    print("Посты добавлены")


key_word = input('Введите ключевое слово, по котором будет производиться поиск: ',)
scroll_range = int(input('Введите количество скроллингов страницы: ',))

posts_info_list = tf_get_post_info(key_word, scroll_range)
pprint(posts_info_list)
print('_____________________________________')
add_posts_info_to_db(posts_db, posts_info_list)




