import requests
import mysql.connector
import unidecode
import scrapy
import requests
from docx import Document
import pandas

start_row = 20  
end_row = 33
num_rows = end_row - start_row


df = pandas.read_excel("GESTÃO DE AÇÕES E-COMMERCE.xlsx", usecols='C:K', skiprows=start_row, nrows=num_rows, engine='openpyxl')

df.columns = ['PRODUTO', 'SITE', 'COLUNA3', 'CLÁSSICO ML', 'COLUNA5', 'PREMIUM ML', 'COLUNA7', 'MARKETPLACES', 'COLUNA9']


for index, i in df.iterrows():
    if i['PRODUTO'] == "FONTE 40A":
        fonte40Marketplace = round(i['COLUNA3'], 2);
        fonte40Classico = round(i['COLUNA5'], 2);
        fonte40Premium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 60A":
        fonte60Marketplace = round(i['COLUNA3'], 2);
        fonte60Classico = round(i['COLUNA5'], 2);
        fonte60Premium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 60A LITE":
        fonte60liteMarketplace = round(i['COLUNA3'], 2);
        fonte60liteClassico = round(i['COLUNA5'], 2);
        fonte60litePremium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 70A":
        fonte70Marketplace = round(i['COLUNA3'], 2);
        fonte70Classico = round(i['COLUNA5'], 2);
        fonte70Premium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 70A LITE":
        fonte70liteMarketplace = round(i['COLUNA3'], 2);
        fonte70liteClassico = round(i['COLUNA5'], 2);
        fonte70litePremium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 90 BOB":
        fonte90bobMarketplace = round(i['COLUNA3'], 2);
        fonte90bobClassico = round(i['COLUNA5'], 2);
        fonte90bobPremium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 120 BOB":
        fonte120bobMarketplace = round(i['COLUNA3'], 2);
        fonte120bobClassico = round(i['COLUNA5'], 2);
        fonte120bobPremium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 120A LITE":
        fonte120liteMarketplace = round(i['COLUNA3'], 2);
        fonte120liteClassico = round(i['COLUNA5'], 2);
        fonte120litePremium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 120A":
        fonte120Marketplace = round(i['COLUNA3'], 2);
        fonte120Classico = round(i['COLUNA5'], 2);
        fonte120Premium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 200 BOB":
        fonte200bobMarketplace = round(i['COLUNA3'], 2);
        fonte200bobClassico = round(i['COLUNA5'], 2);
        fonte200bobPremium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 200A LITE":
        fonte200liteMarketplace = round(i['COLUNA3'], 2);
        fonte200liteClassico = round(i['COLUNA5'], 2);
        fonte200litePremium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 200 MONO":
        fonte200monoMarketplace = round(i['COLUNA3'], 2);
        fonte200monoClassico = round(i['COLUNA5'], 2);
        fonte200monoPremium = round(i['COLUNA7'], 2);
    elif i['PRODUTO'] == "FONTE 200A":
        fonte200Marketplace = round(i['COLUNA3'], 2);
        fonte200Classico = round(i['COLUNA5'], 2);
        fonte200Premium = round(i['COLUNA7'], 2);

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


class MlSpider(scrapy.Spider):
    option_selected = ""
    option_selected_new = ""
    name = 'ml'
    start_urls = ["https://lista.mercadolivre.com.br/fonte-jfa"]
    
    def __init__(self, palavra=None, cookie=None, *args, **kwargs):
        super(MlSpider, self).__init__(*args, **kwargs)
        self.palavra = palavra
        self.cookie = cookie
    
    
    def parse(self, response, **kwargs):
        yield from self.parse_all(self.palavra)
        
        
    def parse_catalog(self, search_coming, headers):
        request = requests.get(
            f"https://app.nubimetrics.com/api/search/catalogs?order=relevance&search_filters=condition%3Dnew@&seller_id=1242763049&site_id=MLB&to_search={search_coming}&typeFind=q",
            headers=headers
        )
        request.raise_for_status()
        data = request.json()
        data = data.get('data', [])
        for i in data:
            name = i.get("Name")
            loja = i.get('BuyBoxWinner', {}).get("Nickname")
            listing_type = i.get('BuyBoxWinner', {}).get("ListingTypeId")
            if name and loja and listing_type:
                new_name = name.lower();
                new_name = unidecode.unidecode(new_name)
                if self.option_selected == "FONTE 40A":       
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "40a" in new_name or "40" in new_name or "40 amperes" in new_name or "40amperes" in new_name or "36a" in new_name or "36" in new_name or "36 amperes" in new_name or "36amperes" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                                
                elif self.option_selected == "FONTE 60A":
                       
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "60a" in new_name or "60" in new_name or "60 amperes" in new_name or "60amperes" in new_name or "60 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                elif self.option_selected == "FONTE 60A LITE":
                    if "bob" not in new_name and ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "60a" in new_name or "60" in new_name or "60 amperes" in new_name or "60amperes" in new_name or "60 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})                                      
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                elif self.option_selected == "FONTE 70A":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 70A LITE":
                    
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 90 BOB":
                    
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "90a" in new_name or "90" in new_name or "90 amperes" in new_name or "90amperes" in new_name or "90 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 120A":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 120A LITE":
                    
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 120 BOB":
                    
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 200A":
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'mono' not in new_name and 'monovolt' not in new_name and '220v' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 200 MONO":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and ("mono" in new_name or "220v" in new_name or "monovolt" in new_name):
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 200A LITE":
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'monovolt' not in new_name and '220v' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
                            
                            
                elif self.option_selected == "FONTE 200 BOB":
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'mono' not in new_name and 'monovolt' not in new_name and '220v' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=i.get('Permalink'), callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})          
                            for item in i.get('Sellers', []):
                                loja = item.get("Nickname")
                                name = i.get("Name")
                                listing_type = item.get("ListingTypeId")
                                if loja and name and listing_type:
                                    yield scrapy.Request(url=f'{i.get('Permalink')}?pdp_filters=item_id:{item.get('ItemId')}', callback=self.parse_product, meta={'name': name, 'loja': loja, 'listing_type': listing_type})
                                else:
                                    print("Missing loja or name for item:", i.get("Name"))
    
    def parse_all(self, option_function):
        self.option_selected = option_function
        self.option_selected_new = option_function
        search = ""
        if self.option_selected == "FONTE 40A":
            search = "fonte storm 40a"
        if self.option_selected == "FONTE 60A LITE":
            search = "fonte lite 60a"
        elif self.option_selected == "FONTE 60A":
            search = "fonte storm 60a"
        if self.option_selected == "FONTE 70A LITE":
            search = "fonte lite 70a"
        elif self.option_selected == "FONTE 70A":
            search = "fonte storm 70a"
        elif self.option_selected == "FONTE 90 BOB":
            search = "fonte bob 90a"
        elif self.option_selected == "FONTE 120A":
            search = "fonte storm 120a"
        elif self.option_selected == "FONTE 120A LITE":
            search = "fonte lite 120a"
        elif self.option_selected == "FONTE 120 BOB":
            search = "fonte bob 120a"
        elif self.option_selected == "FONTE 200A":
            search = "fonte storm 200a"
        elif self.option_selected == "FONTE 200A LITE":
            search = "fonte lite 200a"
        elif self.option_selected == "FONTE 200 BOB":
            search = "fonte bob 200a"
        elif self.option_selected == "FONTE 200 MONO":
            search = "fonte storm 200a mono"
        search = search.replace(" ", "%20")
        
        search_catalog = ""
        if self.option_selected == "FONTE 40A":
            search_catalog = "fonte 40a"
        if self.option_selected == "FONTE 60A LITE":
            search_catalog = "fonte 60a"
        elif self.option_selected == "FONTE 60A":
            search_catalog = "fonte 60a"
        if self.option_selected == "FONTE 70A LITE":
            search_catalog = "fonte 70a"
        elif self.option_selected == "FONTE 70A":
            search_catalog = "fonte 70a"
        elif self.option_selected == "FONTE 90 BOB":
            search_catalog = "fonte 90a"
        elif self.option_selected == "FONTE 120A":
            search_catalog = "fonte 120a"
        elif self.option_selected == "FONTE 120A LITE":
            search_catalog = "fonte 120a"
        elif self.option_selected == "FONTE 120 BOB":
            search_catalog = "fonte 120a"
        elif self.option_selected == "FONTE 200A":
            search_catalog = "fonte 200a"
        elif self.option_selected == "FONTE 200A LITE":
            search_catalog = "fonte 200a"
        elif self.option_selected == "FONTE 200 BOB":
            search_catalog = "fonte 200a"
        elif self.option_selected == "FONTE 200 MONO":
            search_catalog = "fonte 200a mono"
        search_catalog = search_catalog.replace(" ", "%20")
        
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
        
        yield from self.parse_catalog(search_catalog, headers)
                
        
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
                if "/p/" in permalink:
                    url = permalink + f"?pdp_filters=item_id:{id}"
                else:
                    url = permalink
                listing_type = item.get('listing_type_id')
                loja = item.get('sellernickname')
                price = item.get('price')
                new_name = name.lower();
                new_name = unidecode.unidecode(new_name)
                if self.option_selected == "FONTE 40A":       
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "40a" in new_name or "40" in new_name or "40 amperes" in new_name or "40amperes" in new_name or "36a" in new_name or "36" in new_name or "36 amperes" in new_name or "36amperes" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-40a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-40a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})
                            
                elif self.option_selected == "FONTE 60A":
                       
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "60a" in new_name or "60" in new_name or "60 amperes" in new_name or "60amperes" in new_name or "60 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-60a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-60a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                elif self.option_selected == "FONTE 60A LITE":
                    if "bob" not in new_name and ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "60a" in new_name or "60" in new_name or "60 amperes" in new_name or "60amperes" in new_name or "60 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-60a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-60a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                elif self.option_selected == "FONTE 70A":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-70a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-70a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 70A LITE":
                    
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-70a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-70a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 90 BOB":
                    
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "90a" in new_name or "90" in new_name or "90 amperes" in new_name or "90amperes" in new_name or "90 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-90a-bob-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-90a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 120A":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price,'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 120A LITE":
                    
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 120 BOB":
                    
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name:
                        if "120a" in new_name or "120" in new_name or "120 amperes" in new_name or "120amperes" in new_name or "120 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price,'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-120a-bob-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-120a-bob_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 200A":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'mono' not in new_name and 'monovolt' not in new_name and '220v' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 200 MONO":
                    
                    if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and ("mono" in new_name or "220v" in new_name or "monovolt" in new_name):
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price,'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-mono-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a-mono_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 200A LITE":
                    if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'monovolt' not in new_name and '220v' not in new_name:
                        if "200a" in new_name or "200" in new_name or "200 amperes" in new_name or "200amperes" in new_name or "200 a" in new_name:
                            yield scrapy.Request(url=url, callback=self.parse_product, meta={'name': name, 'loja': loja, 'price':price, 'listing_type': listing_type})
                            yield scrapy.Request(url='https://www.radicalsom.com.br/fonte-200a-lite-jfa_OrderId_PRICE_NoIndex_True', callback=self.parse_radicalson, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.bestonline.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_bestonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.shoppratico.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_shoppratico, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.renovonline.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_renovonline, meta={'name': name, 'loja': loja, 'price':price})
                            yield scrapy.Request(url='https://www.lsdistribuidora.com.br/fonte-jfa-200a-lite_OrderId_PRICE_NoIndex_True', callback=self.parse_lsdistribuidora, meta={'name': name, 'loja': loja, 'price':price})

                            
                            
                elif self.option_selected == "FONTE 200 BOB":
                    if "bob" in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and 'mono' not in new_name and 'mono' not in new_name and 'monovolt' not in new_name and '220v' not in new_name:
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

        self.option_selected_new = self.option_selected
        price = extract_price(response)
        if not price:
            return        
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
            if self.option_selected_new == "FONTE 40A" and new_price_float >= fonte40Classico:
                return;
            elif self.option_selected_new == "FONTE 60A LITE" and new_price_float >= fonte60liteClassico:
                return;
            elif self.option_selected_new == "FONTE 60A" and new_price_float >= fonte60Classico:
                return;
            elif self.option_selected_new == "FONTE 70A LITE" and new_price_float >= fonte70liteClassico:
                return;
            elif self.option_selected_new == "FONTE 70A" and new_price_float >= fonte70Classico:
                return;
            elif self.option_selected_new == "FONTE 90 BOB" and new_price_float >= fonte90bobClassico:
                return;
            elif self.option_selected_new == "FONTE 120 BOB" and new_price_float >= fonte120bobClassico:
                return;
            elif self.option_selected_new == "FONTE 120A LITE" and new_price_float >= fonte120liteClassico:
                return;
            elif self.option_selected_new == "FONTE 120A" and new_price_float >= fonte120Classico:
                return;
            elif self.option_selected_new == "FONTE 200 BOB" and new_price_float >= fonte200bobClassico:
                return;
            elif self.option_selected_new == "FONTE 200A LITE" and new_price_float >= fonte200liteClassico:
                return;
            elif self.option_selected_new == "FONTE 200 MONO" and new_price_float >= fonte200monoClassico:
                return;
            elif self.option_selected_new == "FONTE 200A" and new_price_float >= fonte200Classico:
                return;
        elif tipo == "Premium" and new_price_float:
            if self.option_selected_new == "FONTE 40A" and new_price_float >= fonte40Premium:
                return;
            elif self.option_selected_new == "FONTE 60A LITE" and new_price_float >= fonte60litePremium:
                return;
            elif self.option_selected_new == "FONTE 60A" and new_price_float >= fonte60Premium:
                return;
            elif self.option_selected_new == "FONTE 70A LITE" and new_price_float >= fonte70litePremium:
                return;
            elif self.option_selected_new == "FONTE 70A" and new_price_float >= fonte70Premium:
                return;
            elif self.option_selected_new == "FONTE 90 BOB" and new_price_float >= fonte90bobPremium:
                return;
            elif self.option_selected_new == "FONTE 120 BOB" and new_price_float >= fonte120bobPremium:
                return;
            elif self.option_selected_new == "FONTE 120A LITE" and new_price_float >= fonte120litePremium:
                return;
            elif self.option_selected_new == "FONTE 120A" and new_price_float >= fonte120Premium:
                return;
            elif self.option_selected_new == "FONTE 200 BOB" and new_price_float >= fonte200bobPremium:
                return;
            elif self.option_selected_new == "FONTE 200A LITE" and new_price_float >= fonte200litePremium:
                return;
            elif self.option_selected_new == "FONTE 200 MONO" and new_price_float >= fonte200monoPremium:
                return;
            elif self.option_selected_new == "FONTE 200A" and new_price_float >= fonte200Premium:
                return;


        location_url = f'https://www.mercadolivre.com.br/perfil/{loja.replace(" ", "+")}'

        yield scrapy.Request(url=location_url, callback=self.parse_location, meta={'url': response.url, 'name': name, 'price': new_price_float, 'qtde_parcelado': parcelado, 'price_parcelado': new_price_other_float, 'loja': loja, 'tipo': tipo })


    def finish(self, total_price, url, nomeFonte, loja, lugar):
        if self.option_selected_new == "FONTE 40A" and total_price >= fonte40Marketplace:
            return;
        elif self.option_selected_new == "FONTE 60A LITE" and total_price >= fonte60liteMarketplace:
            return;
        elif self.option_selected_new == "FONTE 60A" and total_price >= fonte60Marketplace:
            return;
        elif self.option_selected_new == "FONTE 70A LITE" and total_price >= fonte70liteMarketplace:
            return;
        elif self.option_selected_new == "FONTE 70A" and total_price >= fonte70Marketplace:
            return;
        elif self.option_selected_new == "FONTE 90 BOB" and total_price >= fonte90bobMarketplace:
            return;
        elif self.option_selected_new == "FONTE 120 BOB" and total_price >= fonte120bobMarketplace:
            return;
        elif self.option_selected_new == "FONTE 120A LITE" and total_price >= fonte120liteMarketplace:
            return;
        elif self.option_selected_new == "FONTE 120A" and total_price >= fonte120Marketplace:
            return;
        elif self.option_selected_new == "FONTE 200 BOB" and total_price >= fonte200bobMarketplace:
            return;
        elif self.option_selected_new == "FONTE 200A LITE" and total_price >= fonte200liteMarketplace:
            return;
        elif self.option_selected_new == "FONTE 200 MONO" and total_price >= fonte200monoMarketplace:
            return;
        elif self.option_selected_new == "FONTE 200A" and total_price >= fonte200Marketplace:
            return;
        
        parcelado = self.get_price_previsto("NA")

        doc.add_paragraph(f'Modelo: {self.option_selected_new}')
        doc.add_paragraph(f'URL: {url}')
        doc.add_paragraph(f'Nome: {nomeFonte}')
        doc.add_paragraph(f'Preço: {total_price}')
        doc.add_paragraph(f'Preço Previsto: {parcelado}')
        doc.add_paragraph(f'Loja: {loja}')
        doc.add_paragraph('Tipo: ')
        doc.add_paragraph(f'Lugar: {lugar}')
        doc.add_paragraph("--------------------------------------------------------------------")
        doc.add_paragraph('')
        doc.save(fr"dados/{self.option_selected_new}.docx")
            
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
            if self.option_selected == "FONTE 40A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 70A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 70A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 90 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 120A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200 BOB":
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
            if self.option_selected == "FONTE 40A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 70A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 70A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 90 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 120A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200 BOB":
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
            if self.option_selected == "FONTE 40A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 70A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 70A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 90 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 120A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200 BOB":
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
            if self.option_selected == "FONTE 40A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 70A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 70A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 90 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 120A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200 BOB":
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
            if self.option_selected == "FONTE 40A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "40a" in nomeFonte or "40" in nomeFonte or "40 amperes" in nomeFonte or "40amperes" in nomeFonte or "36a" in nomeFonte or "36" in nomeFonte or "36 amperes" in nomeFonte or "36amperes" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 60A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "60a" in nomeFonte or "60" in nomeFonte or "60 amperes" in nomeFonte or "60amperes" in nomeFonte or "60 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 70A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 70A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "70a" in nomeFonte or "70" in nomeFonte or "70 amperes" in nomeFonte or "70amperes" in nomeFonte or "70 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 90 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "90a" in nomeFonte or "90" in nomeFonte or "90 amperes" in nomeFonte or "90amperes" in nomeFonte or "90 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 120A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 120 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "120a" in nomeFonte or "120" in nomeFonte or "120 amperes" in nomeFonte or "120amperes" in nomeFonte or "120 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                        
            elif self.option_selected == "FONTE 200 MONO":
                if "bob" not in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200A LITE":
                if "bob" not in nomeFonte and "lite" in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)
                    
                        
            elif self.option_selected == "FONTE 200 BOB":
                if "bob" in nomeFonte and "lite" not in nomeFonte and "controle" not in nomeFonte and 'jfa' in nomeFonte and 'mono' not in nomeFonte and 'monovolt' not in nomeFonte:
                    if "200a" in nomeFonte or "200" in nomeFonte or "200 amperes" in nomeFonte or "200amperes" in nomeFonte or "200 a" in nomeFonte:
                        yield from self.finish(total_price, url, nomeFonte, loja, lugar)       
        
    def get_price_previsto(self, tipo):
        if tipo == "Clássico":
            for index, i in df.iterrows():
                if self.option_selected_new == "FONTE 40A" and i['PRODUTO'] == "FONTE 40A":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 60A" and i['PRODUTO'] == "FONTE 60A":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 60A LITE" and i['PRODUTO'] == "FONTE 60A LITE":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 70A" and i['PRODUTO'] == "FONTE 70A":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 70A LITE" and i['PRODUTO'] == "FONTE 70A LITE":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 90 BOB" and i['PRODUTO'] == "FONTE 90 BOB":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 120 BOB" and i['PRODUTO'] == "FONTE 120 BOB":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 120A LITE" and i['PRODUTO'] == "FONTE 120A LITE":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 120A" and i['PRODUTO'] == "FONTE 120A":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 200 BOB" and i['PRODUTO'] == "FONTE 200 BOB":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 200A LITE" and i['PRODUTO'] == "FONTE 200A LITE":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 200 MONO" and i['PRODUTO'] == "FONTE 200 MONO":
                    return round(i['COLUNA5'], 2);
                elif self.option_selected_new == "FONTE 200A" and i['PRODUTO'] == "FONTE 200A":
                    return round(i['COLUNA5'], 2);
        elif tipo == "Premium":
            for index, i in df.iterrows():
                if self.option_selected_new == "FONTE 40A" and i['PRODUTO'] == "FONTE 40A":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 60A" and i['PRODUTO'] == "FONTE 60A":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 60A LITE" and i['PRODUTO'] == "FONTE 60A LITE":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 70A" and i['PRODUTO'] == "FONTE 70A":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 70A LITE" and i['PRODUTO'] == "FONTE 70A LITE":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 90 BOB" and i['PRODUTO'] == "FONTE 90 BOB":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 120 BOB" and i['PRODUTO'] == "FONTE 120 BOB":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 120A LITE" and i['PRODUTO'] == "FONTE 120A LITE":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 120A" and i['PRODUTO'] == "FONTE 120A":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 200 BOB" and i['PRODUTO'] == "FONTE 200 BOB":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 200A LITE" and i['PRODUTO'] == "FONTE 200A LITE":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 200 MONO" and i['PRODUTO'] == "FONTE 200 MONO":
                    return round(i['COLUNA7'], 2);
                elif self.option_selected_new == "FONTE 200A" and i['PRODUTO'] == "FONTE 200A":
                    return round(i['COLUNA7'], 2);
        elif tipo == "NA":
            for index, i in df.iterrows():
                if self.option_selected_new == "FONTE 40A" and i['PRODUTO'] == "FONTE 40A":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 60A" and i['PRODUTO'] == "FONTE 60A":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 60A LITE" and i['PRODUTO'] == "FONTE 60A LITE":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 70A" and i['PRODUTO'] == "FONTE 70A":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 70A LITE" and i['PRODUTO'] == "FONTE 70A LITE":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 90 BOB" and i['PRODUTO'] == "FONTE 90 BOB":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 120 BOB" and i['PRODUTO'] == "FONTE 120 BOB":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 120A LITE" and i['PRODUTO'] == "FONTE 120A LITE":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 120A" and i['PRODUTO'] == "FONTE 120A":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 200 BOB" and i['PRODUTO'] == "FONTE 200 BOB":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 200A LITE" and i['PRODUTO'] == "FONTE 200A LITE":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 200 MONO" and i['PRODUTO'] == "FONTE 200 MONO":
                    return round(i['COLUNA3'], 2);
                elif self.option_selected_new == "FONTE 200A" and i['PRODUTO'] == "FONTE 200A":
                    return round(i['COLUNA3'], 2);

    def parse_location(self, response):
        name = response.meta['name']
        url = response.meta['url']
        new_price_float = response.meta['price']
        tipo = response.meta['tipo']
        parcelado = self.get_price_previsto(tipo)
        loja = response.meta['loja']
        lugar = response.xpath('//*[@id="profile"]/div/div[2]/div[1]/div[3]/p/text()').get()


        doc.add_paragraph(f'Modelo: {self.option_selected_new}')
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
        doc.save(fr"dados/{self.option_selected_new}.docx")

        
        
