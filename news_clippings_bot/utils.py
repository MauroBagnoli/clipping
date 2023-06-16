import re

def get_urls_from_message(message):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = list(filter(None, re.findall(regex, message)))

    return urls

def get_message_without_urls(message):
    # create a regex pattern that matches substrings starting with https:// or www.
    pattern = r"https?://\S+|www\.\S+"
    # use re.sub to replace the matched substrings with empty strings
    result = re.sub(pattern, "", message)
    # return the result
    return result

def get_author_from_message(message): 
    pattern2 = r"autor:(.*?)(tags|$)"
    match = re.search(pattern2, message)
    if match:
        return match.group(1)

def get_tag_from_message(message): 
    pattern2 = r"tags:(.*?)(autor:|$)"
    match = re.search(pattern2, message)
    if match:
        return match.group(1)
