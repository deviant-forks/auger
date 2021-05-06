from urls import URLS
import xml.etree.ElementTree as ET
import psycopg2
import asyncio
import httpx

'''
[WHAT IS THIS]
This scrapes xml for it's article content or summary.
'''

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

select_urls_from_post = '''
SELECT article_url FROM posts;
''' 

update_transact = """
UPDATE posts SET article_host = %s, article_favicon = %s WHERE article_url ILIKE '%' || %s || '%', 
"""

async def main():
    async with httpx.AsyncClient() as client:
        for url in URLS:
            try: 
                response = await client.get(url, timeout=30.0)
                
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")
                continue
            
            try:
                #give root a body of XML as a string.
                root = ET.fromstring(response.text)
                                
            except:
                continue
            
            try:
                synopsis = [x for x in root if x.tag.split("}")[1] in ("entry", "item")]
            
            except IndexError:
                synopsis = [x for x in root if x.tag in ("entry", "item")]
                
            for syn in synopsis:
                try:
                    summary = [x.text for x in syn if x.tag.split("}")[1] == "summary"]
                    content = [x.text for x in syn if x.tag.split("}")[1] == "content"]
                    
                    if summary:
                        print(f"Found SUMMARY {summary[:200]} at {url}")
                    if content:
                        print(f"Found CONTENT {content[:200]} at {url}")
                                        
                except IndexError:
                    
                    if synopsis is not None:
                        print(synopsis)
                        
                    
                
                
                         
cur.close()
conn.close()  

if __name__ == '__main__':
    asyncio.run(main())