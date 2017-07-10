from bs4 import BeautifulSoup
from qqmail import get_qqmail_pop
import requests
import json

def get_forum_location(url):
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
        print(url)
    return r.history[0].headers['Location']

def get_email_link(content):
    soup = BeautifulSoup(content, 'lxml')
    meta_content_tag = soup.find('meta', attrs={'content': '阅读整个主题'})
    try:
        link_tag = soup.find('a', text="查看主题") 
    except Exception as e:
        print(e)
        print(content)
    return link_tag['href']

def get_email_topic(subject):
    start_key = '['
    end_key = ']'
    s_index = subject.find(start_key)
    e_index = subject.find(end_key)
    if s_index != -1:
        return subject[s_index + len(start_key):e_index]
    return None

def get_email_question(subject):
    start_key = '] '
    s_index = subject.find(start_key)
    if s_index != -1:
        return subject[s_index + len(start_key):]
    return None

def is_udacity_forum(subject):
    key_word = '优达学城论坛'
    index = subject.find(key_word)
    if index != -1:
        return True
    return False

def get_robot_reply(email_results, data):
    reply_msg = [] 

    for email_result in email_results:
        headers = email_result['header']
        content_html = email_result['content'][-1]

        if is_udacity_forum(headers['Subject']) is True:
            msg = forum_send(headers, content_html, data)
            reply_msg += msg
    
    return reply_msg

def forum_send(headers, content_html, data):
    subject = headers['Subject']
    topic = get_email_topic(subject)
    question = get_email_question(subject)
    link = get_email_link(content_html)
    link = get_forum_location(link)

    reply_msg = []
    for item in data['forum_group']:
        if match_subject(subject, item['match_subject']) is False:
            continue

        forum_template = "主题: 【{0}】\n\n问题❓: {1} \n\n链接: {2}"
        message = forum_template.format(topic, question, link)
        msg = {}
        msg['group_name'] = item['group_name']
        msg['send_msg'] = message
        reply_msg.append(msg)

    return reply_msg 

def match_subject(subject, strings):
    for s in strings:
        if subject.find(s) != -1:
            return True
    return False

# TEST
# JSON_FILE = 'config.json'
# with open(JSON_FILE) as data_file:    
#     data = json.load(data_file)

# user_gmail = data['gmail_account']
# pwd_gmail = data['password']

# emails = get_qqmail_pop(user_gmail, pwd_gmail)
# send_msg = get_robot_reply(emails, data)

# print(get_robot_reply(emails, data))