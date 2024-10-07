from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

import re
import logger
#from google_images_search import GoogleImagesSearch

headers = {
    'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
}
#gis = GoogleImagesSearch(env.googAPIkey, env.googCX)
logger = logger.log(0)

def get_reddit_story(article_link):
    driver = webdriver.Chrome()
    logger.start('Getting reddit story')
    max_bytes = 1024
    if re.match(r'^https://(?:www\.)?.+\..+$', article_link):

        driver.get(article_link)
        post_pic = driver.find_element(By.XPATH, '/html/body/shreddit-app/div/div[1]/div/main/shreddit-post/div[1]')
        post_pic.screenshot('credit_bar.png')
        post_pic = driver.find_element(By.XPATH, '/html/body/shreddit-app/div/div[1]/div/main/shreddit-post/h1')

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = ''
        paragraphs = soup.find_all(name='p')
        for i, paragraph in enumerate(paragraphs):
            if i != 0:
                words = paragraph.text.split(' ')
                para = ''
                for word in words:
                    if re.match(r'[^-]+', word):
                        para += ' ' + word
                if len(result.encode('utf-8')) + len(para.encode('utf-8')) < max_bytes:
                    result += para
                else:
                    print('TTS String is ' + str(len(result.encode('utf-8'))))
                    break
        logger.end('Getting Reddit Story')
        clean_text = [paragraph.text for paragraph in paragraphs]
        txt = ''
        for text in clean_text:
            txt += (text + '\n')
        driver.quit()
        return [result, clean_text]
    else:
        logger.end('Getting Reddit Story')
        driver.quit()
        raise Exception("Your input for " + article_link + ' is not an appropriately formatted link, please try again copying the full link from your browser.')
    
    '''
def getImages(paragraphs):
    logger.start('getImages')
    for i, paragraph in enumerate(paragraphs):
        aiSearchParamer = {
            'q' : (paragraph),
            'num' : 1,
        }
        gis.search(
            search_params=aiSearchParamer,
            path_to_dir='output\images',
            custom_image_name='paragraph'+str(i)+'Image')
    logger.end('getImages')
    '''
