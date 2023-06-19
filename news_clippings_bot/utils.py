import re

def get_urls_from_message(message):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex, message)

    print('urls: ', urls)

    if len(urls) > 0:
        urls_raw = [list(filter(None, url)) for url in urls]
        urls = [item for sub_list in urls_raw for item in sub_list]

        print('urls: ', urls)

        return urls

    return []


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
        tags = match.group(1).split(',')
        trimmed_tags = [tag.strip() for tag in tags]
        print('trimmed_tags: ', trimmed_tags)
        return trimmed_tags
        

def get_is_valid_email(email): 
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email):
        return True
    else:
        return False
