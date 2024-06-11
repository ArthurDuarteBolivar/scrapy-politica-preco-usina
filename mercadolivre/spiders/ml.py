import cv2
import requests
import numpy as np
from io import BytesIO
import logging
import pudb
import time
# pudb.set_trace()
import unidecode
import scrapy
import requests
import os
from docx import Document

# if os.path.exists("dados_scrapy.docx"):
#     doc = Document("dados_scrapy.docx")
# else:
doc = Document()

def extract_price(response):
  price_selectors = [
      '//*[@id="price"]/div/div[1]/div[1]/span[1]/span/span[2]/text()',
      '//html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[@class="ui-pdp-container__row ui-pdp-container__row--price"]/div/div[1]/div[1]/span/span/span[2]/text()',
      '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[3]/div[1]/div[1]/span/span/span[2]/text()',
      '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span[1]/span/span[2]/text()'
  ]
  
  for selector in price_selectors:
    price = response.xpath(selector).get()
    if price:
      price = price.replace('.', '')
      decimal_selector = selector.replace("span[2]/text()", "") + 'span[@class="andes-money-amount__cents andes-money-amount__cents--superscript-36"]/text()'
      price_decimal = response.xpath(decimal_selector).get()
      
      if price_decimal:
        return float(f"{price}.{price_decimal}")
      else:
        try:
          return float(price)
        except ValueError:
          pass

  return None  

def download_image_from_url(url):
    response = requests.get(url)
    img = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
    return img

def download_image(image_src, download_folder, desired_filename):
    return
    # os.makedirs("images", exist_ok=True)  
    # desired_filename = os.path.join('images', desired_filename + '.png')  # Append .png to the filename

    # response = requests.get(image_src, stream=True)

    # if response.status_code == 200:
    #     with open(desired_filename, 'wb') as f:
    #         for chunk in response.iter_content(chunk_size=1024):
    #             f.write(chunk)
    #     print("Image downloaded successfully:", desired_filename)
    #     return desired_filename  # Return the downloaded file path
    # else:
    #     print(f"Failed to download image: {response.status_code}")
    #     return None  # Return None on failure


options = ["Storm 40"]#, "Storm 60" ,"Lite 60","Storm 70", "Lite 70", "Bob 90", "Storm 120", "Lite 120", "Bob 120", "Storm 200", "Storm 200 MONO", "Bob 200", "Lite 200"



class MlSpider(scrapy.Spider):
    option_selected = ""
    name = 'ml'
    start_urls = ["https://lista.mercadolivre.com.br/fonte-jfa"]
    
    def __init__(self, palavra=None, cookie=None, *args, **kwargs):
        super(MlSpider, self).__init__(*args, **kwargs)
        self.palavra = palavra
        self.cookie = cookie
    
    
    def parse(self, response, **kwargs):
        # yield from self.parse_all("Storm 40")
        # yield from self.parse_all("Lite 60")
        # yield from self.parse_all("Storm 60")
        # yield from self.parse_all("Storm 70")
        # yield from self.parse_all("Lite 70")
        # yield from self.parse_all("Bob 90")
        # yield from self.parse_all("Storm 120")
        # yield from self.parse_all("Lite 120")
        # yield from self.parse_all("Bob 120")
        yield from self.parse_all(self.palavra)
        # yield from self.parse_all("Storm 200 MONO")
        # yield from self.parse_all("Bob 200")
        # yield from self.parse_all("Lite 200")
        
        
        
        
    def parse_all(self, option_function):
        self.option_selected = option_function
        search = ""
        if self.option_selected == "Storm 40":
            search = "fonte storm 40a jfa"
        if self.option_selected == "Lite 60":
            search = "fonte lite 60a jfa"
        elif self.option_selected == "Storm 60":
            search = "fonte storm 60a jfa"
        if self.option_selected == "Lite 70":
            search = "fonte lite 70a jfa"
        elif self.option_selected == "Storm 70":
            search = "fonte storm 70a jfa"
        elif self.option_selected == "Bob 90":
            search = "fonte bob 90a jfa"
        elif self.option_selected == "Storm 120":
            search = "fonte storm 120a jfa"
        elif self.option_selected == "Lite 120":
            search = "fonte lite 120a jfa"
        elif self.option_selected == "Bob 120":
            search = "fonte bob 120a jfa"
        elif self.option_selected == "Storm 200":
            search = "fonte storm 200a jfa"
        elif self.option_selected == "Lite 200":
            search = "fonte lite 200a jfa"
        elif self.option_selected == "Bob 200":
            search = "fonte bob 200a jfa"
        elif self.option_selected == "Storm 200 MONO":
            search = "fonte storm 200a mono jfa"
        search = search.replace(" ", "%20")
        # search = "fonte%2040a%20jfa"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": self.cookie,
            "Host": "app.nubimetrics.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        
        request = requests.get(
            f"https://app.nubimetrics.com/api/search/items?attributes=results,available_filters,paging,filters&buying_mode=buy_it_now&exportData=false&isControlPrice=false&language=pt_BR&limit=200&offset=0&order=price_asc&pvp=0&search_filters=condition%3Dnew@&seller_id=1242763049&site_id=MLB&to_search={search}&typeSearch=q",
            headers=headers
        )
        
        request.raise_for_status()
        data = request.json()
        paging_data = data.get('data', {}).get('paging', {}) 

        total = paging_data.get('total') 
        offset = paging_data.get('offset') 
        limit = paging_data.get('limit') 
        
        while offset < total:
            request = requests.get(
                f"https://app.nubimetrics.com/api/search/items?attributes=results,available_filters,paging,filters&buying_mode=buy_it_now&exportData=false&isControlPrice=false&language=pt_BR&limit=200&offset={offset}&order=price_asc&pvp=0&search_filters=condition%3Dnew@&seller_id=1242763049&site_id=MLB&to_search={search}&typeSearch=q",
                headers=headers
            )
            request.raise_for_status()
            data = request.json()
            paging_data = data.get('data', {}).get('paging', {}) 
            total = paging_data.get('total') 
            offset = paging_data.get('offset') 
            limit = paging_data.get('limit') 
            offset = offset + limit;
            
            for item in data.get('data', {}).get('results', []):
                name = item.get('title')
                id = item.get('id')
                permalink = item.get("permalink");
                # url = "https://produto.mercadolivre.com.br/MLB-" + id.replace("MLB", "")
                if "/p/" in permalink:
                    url = permalink + f"?pdp_filters=item_id:{id}"
                else:
                    url = permalink
                # if id != "MLB3727486257":
                #     continue
                # else:
                #     print(item.get("permalink"))
                    # url = "https://www.mercadolivre.com.br/fonte-carregador-jfa-bob-storm-90a-bivolt-automatico-cor-preto/p/MLB21562641?pdp_filters=item_id:MLB4448891798"
                listing_type = item.get('listing_type_id')
                loja = item.get('sellernickname')
                price = item.get('price')
                new_name = name.lower();
                new_name = unidecode.unidecode(new_name)
                if self.option_selected == "Storm 40":       
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "40a" in new_name or "40" in new_name or "40 amperes" in new_name or "40amperes" in new_name or "36a" in new_name or "36" in new_name or "36 amperes" in new_name or "36amperes" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-40a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                elif self.option_selected == "Storm 60":
                       
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "60a" in new_name or "60" in new_name or "60 amperes" in new_name or "60amperes" in new_name or "60 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-60a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                elif self.option_selected == "Lite 60":
                    if "bob" not in new_name and ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "60a" in new_name or "60" in new_name or "60 amperes" in new_name or "60amperes" in new_name or "60 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-60a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                elif self.option_selected == "Storm 70":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-70a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Lite 70":
                    
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-70a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Bob 90":
                    
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "90a" in new_name or "90" in new_name or "90 amperes" in new_name or "90amperes" in new_name or "90 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-90a-bob-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Storm 120":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price,'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Lite 120":
                    
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Bob 120":
                    
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price,'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-bob-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Storm 200":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'monovolt' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Storm 200 MONO":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and 'mono' in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price,'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-mono-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Lite 200":
                    
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "Bob 200":
                    
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'monovolt' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-bob-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a-bo_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a-bo_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a-bo_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a-bo_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

    
                
    def parse_product(self, response):
        name = response.meta['name']
        loja = response.meta['loja']
        listing_type = response.meta['listing_type']
        # price = response.meta['price']
        
        id_anuncio = response.xpath('//*[@id="denounce"]/div/p/span/text()').get().replace("#", "")
        imagem = response.xpath('//*[@id="gallery"]/div/div/span[2]/figure/img/@data-zoom').get()
        if imagem:
            download_image(imagem, self.option_selected, f"{self.option_selected}-{id_anuncio}")
        
        price = extract_price(response)
        new_price_float = price
           
        
        
            
        parcelado = response.xpath('//*[@id="pricing_price_subtitle"]/text()').get()
        if parcelado:
            parcelado = int(parcelado.replace("x", "").strip())
        else:
            parcelado = 0
        
        other_price = response.xpath('//*[@id="pricing_price_subtitle"]/span[2]/span/span[2]/text()').get()
        other_price_decimal = response.xpath('//*[@id="pricing_price_subtitle"]/span[2]/span/span[4]/text()').get()
        
        if other_price and other_price_decimal:
            new_price_other = f"{other_price},{other_price_decimal}"
        elif other_price:
            new_price_other = other_price
        else:
            new_price_other = '0'

        try:
            new_price_other_float = float(new_price_other.replace('.', '').replace(',', '.'))
            new_price_other_float = round((new_price_other_float * parcelado), 3)
        except ValueError:
            new_price_other_float = 0.0
            

        target_id = response.xpath('//*[@id="denounce"]/div/p/span/text()').get()
        if target_id:
            target_id = target_id.replace("#", "")
    
        if listing_type:
            if listing_type == "gold_pro":
                tipo = "Premium"
            else:
                tipo = "Clássico" 
        else:
            tipo = "Clássico" 
        
            
        if tipo == "Clássico" and new_price_float:
            if self.option_selected == "Storm 40" and new_price_float >= 402.79:
                return;
            elif self.option_selected == "Lite 60" and new_price_float >= 364.95:
                return;
            elif self.option_selected == "Storm 60" and new_price_float >= 443.07:
                return;
            elif self.option_selected == "Lite 70" and new_price_float >= 408.73:
                return;
            elif self.option_selected == "Storm 70" and new_price_float >= 493.42:
                return;
            elif self.option_selected == "Bob 90" and new_price_float >= 422.93:
                return;
            elif self.option_selected == "Bob 120" and new_price_float >= 499.46:
                return;
            elif self.option_selected == "Lite 120" and new_price_float >= 536.26:
                return;
            elif self.option_selected == "Storm 120" and new_price_float >= 634.40:
                return;
            elif self.option_selected == "Bob 200" and new_price_float >= 624.33:
                return;
            elif self.option_selected == "Lite 200" and new_price_float >= 681.83:
                return;
            elif self.option_selected == "Storm 200 MONO" and new_price_float >= 736.61:
                return;
            elif self.option_selected == "Storm 200" and new_price_float >= 805.59:
                return;
        elif tipo == "Premium" and new_price_float:
            if self.option_selected == "Storm 40" and new_price_float >= 433.00:
                return;
            elif self.option_selected == "Lite 60" and new_price_float >= 390.43:
                return;
            elif self.option_selected == "Storm 60" and new_price_float >= 473.28:
                return;
            elif self.option_selected == "Lite 70" and new_price_float >= 434.42:
                return;
            elif self.option_selected == "Storm 70" and new_price_float >= 523.63:
                return;
            elif self.option_selected == "Bob 90" and new_price_float >= 443.07:
                return;
            elif self.option_selected == "Bob 120" and new_price_float >= 539.74:
                return;
            elif self.option_selected == "Lite 120" and new_price_float >= 573.36:
                return;
            elif self.option_selected == "Storm 120" and new_price_float >= 674.68:
                return;
            elif self.option_selected == "Bob 200" and new_price_float >= 694.82:
                return;
            elif self.option_selected == "Lite 200" and new_price_float >= 716.71:
                return;
            elif self.option_selected == "Storm 200 MONO" and new_price_float >= 774.88:
                return;
            elif self.option_selected == "Storm 200" and new_price_float >= 845.87:
                return;


        location_url = f'https://www.mercadolivre.com.br/perfil/{loja.replace(" ", "+")}'

        yield scrapy.Request(url=location_url, callback=self.parse_location, meta={'url': response.url, 'name': name, 'price': new_price_float, 'qtde_parcelado': parcelado, 'price_parcelado': new_price_other_float, 'loja': loja, 'tipo': tipo })


    def finish(self, total_price, url, nomeFonte, loja, lugar):
        if self.option_selected == "Storm 40" and total_price >= 352.97:
            return;
        elif self.option_selected == "Lite 60" and total_price >= 321.09:
            return;
        elif self.option_selected == "Storm 60" and total_price >= 391.13:
            return;
        elif self.option_selected == "Lite 70" and total_price >= 362.36:
            return;
        elif self.option_selected == "Storm 70" and total_price >= 438.83:
            return;
        elif self.option_selected == "Bob 90" and total_price >= 372.05:
            return;
        elif self.option_selected == "Bob 120" and total_price >= 444.55:
            return;
        elif self.option_selected == "Lite 120" and total_price >= 484.94:
            return;
        elif self.option_selected == "Storm 120" and total_price >= 572.39:
            return;
        elif self.option_selected == "Bob 200" and total_price >= 562.85:
            return;
        elif self.option_selected == "Lite 200" and total_price >= 624.50:
            return;
        elif self.option_selected == "Storm 200 MONO" and total_price >= 602.61:
            return;
        elif self.option_selected == "Storm 200" and total_price >= 734.57:
            return;
        
        parcelado = self.get_price_previsto("NA")

        doc.add_paragraph(f'Modelo: {self.option_selected}')
        doc.add_paragraph(f'URL: {url}')
        doc.add_paragraph(f'Nome: {nomeFonte}')
        doc.add_paragraph(f'Preço: {total_price}')
        doc.add_paragraph(f'Preço Previsto: {parcelado}')
        doc.add_paragraph(f'Loja: {loja}')
        doc.add_paragraph('Tipo: ')
        doc.add_paragraph(f'Lugar: {lugar}')
        doc.add_paragraph("--------------------------------------------------------------------")
        doc.add_paragraph('')
        doc.save(fr"C:\workspace\mercado-livre\mercadolivre\dados\{self.option_selected}.docx")
            
        yield {
            'url': url,
            'name': nomeFonte,
            'price': total_price,
            'loja': loja,
            'tipo': "",
            'lugar': lugar
        }


    def parse_radicalson(self, response):
        loja = "RADICALSOM"
        lugar = "Artur nogueira, São Paulo."
        for i in response.xpath('//*[@id="root-app"]/div/div[3]/section/ol/li'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[2]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if self.option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                    
    def parse_lsdistribuidora(self, response):
        loja = "LS DISTRIBUIDORA"
        lugar = "Elísio Medrado, Bahia"
        for i in response.xpath('//*[@id="root-app"]/div/div[3]/section/ol/li'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[2]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if self.option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)                

    
    def parse_bestonline(self, response):
        loja = "BESTONLINE"
        lugar = "Rosario, Santa Fe."
        for i in response.xpath('//li[@class="ui-search-layout__item shops__layout-item shops__layout-item ui-search-layout__stack"]'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[2]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if self.option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
            
    
    def parse_renovonline(self, response):
        loja = "RENOV ONLINE"
        lugar = "São João da Boa Vista - SP"
        for i in response.xpath('//li[@class="ui-search-layout__item shops__layout-item shops__layout-item ui-search-layout__stack"]'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[1]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if self.option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)                
        
    def parse_shoppratico(self, response):
        loja = "SHOPPRATICO"
        lugar = "Sorocaba, São Paulo."
        for i in response.xpath('//li[@class="ui-search-layout__item shops__layout-item shops__layout-item ui-search-layout__stack"]'):
            nomeFonte = i.xpath('.//div/div/div/div/a/h2/text()').get()
            price = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[2]/text()').get()
            cents = i.xpath('.//div/div/div[3]/div/div[1]/div/div/div/div/span/span[4]/text()').get()
            url = i.xpath('.//div/div/div[3]/div[2]/a/@href').get()
            nomeFonte = nomeFonte.lower()
            nomeFonte = unidecode.unidecode(nomeFonte)
            if not cents:
                cents = 0
            if price:
                price = price.replace('.', '')
                total_price = float(f"{price}.{cents}")
            if self.option_selected == "Storm 40":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 60":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 60":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 70":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 70":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 90":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 120":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Lite 120":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 120":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Storm 200":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "Storm 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Lite 200":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "Bob 200":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)       
        
    def get_price_previsto(self, tipo):
        if tipo == "Clássico":
            if self.option_selected == "Storm 40":
                return 402.79;
            elif self.option_selected == "Lite 60":
                return 364.95;
            elif self.option_selected == "Storm 60":
                return 443.07;
            elif self.option_selected == "Lite 70":
                return 408.73;
            elif self.option_selected == "Storm 70":
                return 493.42;
            elif self.option_selected == "Bob 90":
                return 422.93;
            elif self.option_selected == "Bob 120":
                return 499.46;
            elif self.option_selected == "Lite 120":
                return 536.26;
            elif self.option_selected == "Storm 120":
                return 634.40;
            elif self.option_selected == "Bob 200":
                return 624.33;
            elif self.option_selected == "Lite 200":
                return 681.83;
            elif self.option_selected == "Storm 200 MONO":
                return 736.61;
            elif self.option_selected == "Storm 200":
                return 805.59;
        elif tipo == "Premium":
            if self.option_selected == "Storm 40":
                return 433.00;
            elif self.option_selected == "Lite 60":
                return 390.43;
            elif self.option_selected == "Storm 60":
                return 473.28;
            elif self.option_selected == "Lite 70":
                return 434.42;
            elif self.option_selected == "Storm 70":
                return 523.63;
            elif self.option_selected == "Bob 90":
                return 443.07;
            elif self.option_selected == "Bob 120":
                return 539.74;
            elif self.option_selected == "Lite 120":
                return 573.36;
            elif self.option_selected == "Storm 120":
                return 674.68;
            elif self.option_selected == "Bob 200":
                return 694.82;
            elif self.option_selected == "Lite 200":
                return 716.71;
            elif self.option_selected == "Storm 200 MONO":
                return 774.88;
            elif self.option_selected == "Storm 200":
                return 845.87;
        elif tipo == "NA":
            if self.option_selected == "Storm 40":
                return 352.97;
            elif self.option_selected == "Lite 60":
                return 321.09;
            elif self.option_selected == "Storm 60":
                return 391.13;
            elif self.option_selected == "Lite 70":
                return 362.36;
            elif self.option_selected == "Storm 70":
                return 438.83;
            elif self.option_selected == "Bob 90":
                return 372.05;
            elif self.option_selected == "Bob 120":
                return 444.55;
            elif self.option_selected == "Lite 120":
                return 484.94;
            elif self.option_selected == "Storm 120":
                return 572.39;
            elif self.option_selected == "Bob 200":
                return 562.85;
            elif self.option_selected == "Lite 200":
                return 624.50;
            elif self.option_selected == "Storm 200 MONO":
                return 602.61;
            elif self.option_selected == "Storm 200":
                return 734.57;

    def parse_location(self, response):
        name = response.meta['name']
        url = response.meta['url']
        new_price_float = response.meta['price']
        tipo = response.meta['tipo']
        parcelado = self.get_price_previsto(tipo)
        loja = response.meta['loja']
        lugar = response.xpath('//*[@id="profile"]/div/div[2]/div[1]/div[3]/p/text()').get()


        doc.add_paragraph(f'Modelo: {self.option_selected}')
        doc.add_paragraph(f'URL: {url}')
        doc.add_paragraph(f'Nome: {name}')
        doc.add_paragraph(f'Preço: {new_price_float}')
        doc.add_paragraph(f'Preço Previsto: {parcelado}')
        doc.add_paragraph(f'Loja: {loja}')
        doc.add_paragraph(f'Tipo: {tipo}')
        doc.add_paragraph(f'Lugar: {lugar}')
        doc.add_paragraph("--------------------------------------------------------------------")
        doc.add_paragraph('')
        
        yield {
            'url': url,
            'name': name,
            'price': new_price_float,
            'price_previsto': parcelado,
            'loja': loja,
            'tipo': tipo,
            'lugar': lugar
        }
        doc.save(fr"C:\workspace\mercado-livre\mercadolivre\dados\{self.option_selected}.docx")

        
        
