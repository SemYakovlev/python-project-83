from bs4 import BeautifulSoup

def truncate(text, max_len=200):
    if text and len(text) > max_len:
        return f'{text[:max_len]}...'
    return text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    h1_tag = soup.find('h1')
    h1 = truncate(h1_tag.get_text().strip()) if h1_tag else ''

    title_tag = soup.find('title')
    title = truncate(title_tag.get_text().strip()) if title_tag else ''

    meta_description_tag = soup.find('meta', attrs={'name': 'description'})
    description = ''
    if meta_description_tag and meta_description_tag.get('content'):
        description = truncate(meta_description_tag.get('content').strip())

    return h1, title, description
