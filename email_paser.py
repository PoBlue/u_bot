from bs4 import BeautifulSoup
from qqmail import get_qqmail_pop
import json

def get_email_link(content):
    soup = BeautifulSoup(content, 'lxml')
    meta_content_tag = soup.find('meta', attrs={'content': '阅读整个主题'})
    link_tag = meta_content_tag.parent.find('link')
    return link_tag['href']

def get_email_topic(subject):
    key_word = '优达学城论坛'
    index = subject.find(key_word)
    if index != -1:
        return subject[index + len(key_word):]
    return None

def is_udacity_forum(subject):
    key_word = '优达学城论坛'
    index = subject.find(key_word)
    if index != -1:
        return True
    return False


# get data for test 
JSON_FILE = 'config.json'
with open(JSON_FILE) as data_file:    
    data = json.load(data_file)
    

user_gmail = data['gmail_account']
pwd_gmail = data['password']

email_results = get_qqmail_pop(user_gmail, pwd_gmail)
for email_result in email_results:
    content_html = email_result['content'][-1]
    headers = email_result['header']

    if is_udacity_forum(headers['Subject']) == True:
        topic = get_email_topic(headers['Subject'])
        link = get_email_link(content_html)
        