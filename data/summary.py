from bs4 import BeautifulSoup
import urllib.parse
import psycopg2
import asyncio
import httpx


'''
[WHAT IS THIS]
This scrapes a list of xml feeds located in urls.py in the URLS var for
their links and titles.
'''

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

sql_extract_article_url = '''select posts(%s);
'''

select_urls_from_post = '''
SELECT article_url FROM posts;
''' 

async def main():
    db_urls = row_match()
    async with httpx.AsyncClient() as client:
        for url in db_urls:
            try:
                response = await client.get(url, timeout=30.0)
                
            except httpx.RequestError as exc:
                print(f"An error occured while making request {exc.request.url!r}.")
                
            try: 
                root = BeautifulSoup(response.text, features="lxml")
            
            except:
                print("exception caught after second try.")
                
            try:
                print(url, root)
                
            except:
                print("fail")

def row_match():
    cur.execute(select_urls_from_post)
    all_articles = cur.fetchall()
    stg_urls = []
    
    for article in all_articles:
        staged_articles = article
        print(staged_articles)
        if staged_articles is not None:
            stg_urls.append(staged_articles) #We break a list, add it to another lol
        else:
            print("else else", staged_articles)   
        
    return stg_urls


if __name__ == '__main__':
    asyncio.run(main())
    
cur.close()
conn.close()