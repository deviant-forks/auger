from urls import URLS
from io import StringIO
from html.parser import HTMLParser
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
                synopsis = [x for x in root[0] if x.tag in ("entry", "item")]
                
            for syn in synopsis:
                try:
                    summary = [x.text for x in syn if x.tag.split("}")[1] == "summary"]
                    content = [x.text for x in syn if x.tag.split("}")[1] == "content"]
                    description = [x.text for x in syn if x.tag.split("}")[1] == "description"]
                    #temp
                    link_url = [x.attrib["href"] for x in syn if x.tag.split("}")[1] == "link"]
                    
                    if summary is not None:
                        summary_to_string = summary
                        string_summary = str(summary_to_string)
                        processed_summary = strip_tags(string_summary)
                        
                    if content is not None:
                        content_to_string = content
                        string_content = str(content_to_string)
                        processed_content = strip_tags(string_content)
                        
                    if description is not None:
                        description_to_string = description
                        string_description = str(description_to_string)
                        processed_description = strip_tags(string_description)
                        

                                        
                except IndexError:
                        summary = [syn.findtext('summary')]
                        content = [syn.findtext('content')]
                        description = [syn.findtext('description')]
                        #temp
                        link_url = [syn.findtext('link')]
                        
                        if summary is not None:
                            summary_to_string = summary
                            string_summary = str(summary_to_string)
                            processed_summary = strip_tags(string_summary)
                            
                        if content is not None:
                            content_to_string = content
                            string_content = str(content_to_string)
                            processed_content = strip_tags(string_content)
                        
                        if description is not None:
                            description_to_string = description
                            string_description = str(description_to_string)
                            processed_description = strip_tags(string_description)

                            
                if processed_summary or processed_content or processed_description:
                    print(f"PROCESSED SUMMARY {processed_summary[:5]} at {link_url}, {url}")
                    print(f"PROCESSED CONTENT {processed_content[:5]} at {link_url}, {url}")
                    print(f"PROCESSED DESCRIPTION  {processed_description[:200]} at {link_url}, {url}")


#strip html tags from string.

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()
    
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
                             
cur.close()
conn.close()  

if __name__ == '__main__':
    asyncio.run(main())