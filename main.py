import basicScraperGUI
from regex import findall

"""
Outline: Uses basic GUI w/ file opener, runner, and label
Input: Address to scrape from
Output: Text file containing newline seperated email addresses
"""

def scrape_emails(text):
    email = r'[-a-zA-Z0-9_.]+@[-a-zA-Z0-9]+\.(?:[-a-zA-Z0-9.]+)+'
    out = findall(email, text)
    for i in out:
        if i[-1] == '.':
            i = i[:-1]
        yield i


if __name__ == '__main__':
    basicScraperGUI.Scraper(scrape_emails)
