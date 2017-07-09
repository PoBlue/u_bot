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
    link = get_email_link(content_html)

    reply_msg = []
    for item in data['forum_group']:
        if match_subject(subject, item['match_subject']) is False:
            continue

        forum_template = "问题: {0} \n\n链接: {1}"
        message = forum_template.format(topic, link)
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

