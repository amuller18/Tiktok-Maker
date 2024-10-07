def inputNotLink(article_link):
    raise Exception("Your input for " + article_link + ' is not an appropriately formatted link, please try again copying the full link from your browser.')

def payloadSizeInvalid():
    raise Exception('Your text is greater than 5120 bytes and cannot be passed to IBM Watson.')