import threading
import subprocess
import os
import time
from tqdm import tqdm
import shutil
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import *
import requests
import httpx
import asyncio

pasta = r"./dados"

# Verificar se a pasta existe
if os.path.exists(pasta):
    # Iterar sobre todos os itens na pasta
    for item in os.listdir(pasta):
        item_path = os.path.join(pasta, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Pasta removida: {item_path}")
        except Exception as e:
            print(f"Erro ao remover {item_path}: {e}")
else:
    print(f"A pasta {pasta} não existe.")
    
if os.path.exists(r"./dados_extraidos.docx"):
    os.remove(r"./dados_extraidos.docx")

def run_command(args):
    subprocess.run(args)

def make_req(cookie):
    # cookie = f"template=template-light; ai_user=EgV55|2024-05-28T11:45:48.501Z; _fbp=fb.1.1716896748573.875911634; lang_nubi=pt_br; hubspotutk=3b227fd6020f103ba35ecca053547573; intercom-id-re8wm274=4a6e9f6a-7d60-4e66-9f7b-3ff7f52b76be; intercom-device-id-re8wm274=76824f0d-e71f-4d6b-8781-c222868a73aa; _ga=GA1.3.836422724.1716896749; _gid=GA1.2.22320633.1718015641; _ce.clock_event=1; _ce.clock_data=117%2C177.91.74.213%2C1%2Cc92baae71318dc81de51a663df2f8b4f%2CChrome%2CBR; _gid=GA1.3.22320633.1718015641; TiPMix=68.25532366585887; x-ms-routing-name=self; ARRAffinity={ARRAffinity}; ARRAffinitySameSite={ARRAffinitySameSite}; i18next=pt_br; _ce.irv=returning; cebs=1; _hp2_ses_props.2056355555=%7B%22ts%22%3A1718100095134%2C%22d%22%3A%22app.nubimetrics.com%22%2C%22h%22%3A%22%2Faccount%2Flogin%22%2C%22q%22%3A%22%3FReturnUrl%3D%252fopportunity%252fcategoryDetail%22%2C%22g%22%3A%22%23%3Fcategory%3DMLB5672-MLB1747-MLB114675-MLB45905%22%7D; _clck=1ukw5r7%7C2%7Cfmj%7C0%7C1609; __hstc=154116135.3b227fd6020f103ba35ecca053547573.1716896751921.1718049731701.1718100102444.37; __hssrc=1; _gcl_au=1.1.81739417.1716896749.1599049596.1718100121.1718100123; ASP.NET_SessionId=b5adhrqkofmqmao1b1rc4y5o; .ASPXAUTH={cookie_new}; _ga=GA1.1.836422724.1716896749; _uetsid=f3bc7b10271411efa1bdb337a018ae5f; _uetvid=d4f1f2b01ce711efb06041a93bf318c4; cebsp_=2; _clsk=9h5rwt%7C1718100132757%7C2%7C1%7Cs.clarity.ms%2Fcollect; _hp2_id.2056355555=%7B%22userId%22%3A%221540691698154969%22%2C%22pageviewId%22%3A%221686909635118599%22%2C%22sessionId%22%3A%2261152993371345%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; __hssc=154116135.2.1718100102444; intercom-session-re8wm274=MmpBSFA2WXFPNUkzaC9wUW1aKzQ0WTZHbDZoc2VnTDF4a3o1MVBURmNUckQ3ZFJQb0pPTTJqSHJuLzBhUVJZOC0tTzZRTStVNE14RFNEZzZjZFBaUlMvQT09--a68e02f23ef3ecd3b01beee744de230eb8c749a6; _ga_X9JW5VPF68=GS1.1.1718100094.19.1.1718100227.60.0.0; _ga_26N5SV28FF=GS1.1.1718100094.61.1.1718100227.60.0.0; _ga_1BD6V1LPWP=GS1.1.1718100094.40.1.1718100227.60.0.0; _ce.s=v~7baa07f6ad267a180f8618e02b13f0b27eb93927~lcw~1718100217156~lva~1718100095462~vpv~17~v11.fhb~1718100131642~v11.lhb~1718100191669~v11.cs~229172~v11.s~965ae320-27d9-11ef-b617-6fe6200ecabb~v11.sla~1718100227797~v11.send~1718100207202~lcw~1718100227798; sc_is_visitor_unique=rx12923916.1718100230.D55E01C3D14F4F03DEB97B398CBAA0C5.34.25.20.18.12.10.4.4.2; ai_session=OunLY|1718100095207|1718100232246.4"
    pasta = r"./dados"


    commands = [
        ["python", "rodar.py", "Fonte Usina Bob 60A", cookie],
        ["python", "rodar.py", "Fonte Usina Bob 120A", cookie],
        ["python", "rodar.py", "Fonte Usina Bob 200A", cookie],
        ["python", "rodar.py", "Fonte Usina Battery Meter 50A", cookie],
        ["python", "rodar.py", "Fonte Usina Battery Meter 70A", cookie],
        ["python", "rodar.py", "Fonte Usina Battery Meter 100A", cookie],
        ["python", "rodar.py", "Fonte Usina Battery Meter 120A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 50A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 70A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 100A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 120A", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 200A MONO", cookie],
        ["python", "rodar.py", "Fonte Usina Smart 200A", cookie],
        ["python", "rodar.py", "Fonte Usina 220A", cookie],
        ["python", "rodar.py", "Carregador de Baterias Charger 60A", cookie],
    ]


    threads = []


    for cmd in commands:
        thread = threading.Thread(target=run_command, args=(cmd,))
        thread.start()
        threads.append(thread)


    for thread in tqdm(threads):
        thread.join()

    subprocess.run(["python", r"./ordenar.py"])

service = Service()
options = webdriver.ChromeOptions()
titulo_arquivo = ""
# options.add_argument("--headless=new")

options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)     


driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com.br/?hl=pt-BR")
time.sleep(3)
try:
    driver.get("https://app.nubimetrics.com/account/login?ReturnUrl=%2fopportunity%2fcategoryDetail#?category=MLB5672")#https://app.nubimetrics.com/opportunity/categoryDetail#?category=MLB263532
    counter = 0
    while True:
        test = driver.find_elements(By.XPATH, '//*[@id="content"]/div[1]/div/form/div/div[1]/fieldset/section[1]/label/input')
        if test:
            break
        else:
            counter += 1
            if counter > 20:
                break;
            time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/form/div/div[1]/fieldset/section[1]/label/input').send_keys("carlosbartojr@yahoo.com")
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/form/div/div[1]/fieldset/section[2]/label/input').send_keys("JFA2004")
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/form/div/footer/button').click()
except TimeoutException as e:
    print(f"Timeout ao tentar carregar a página ou encontrar um elemento: {e}")
except NoSuchElementException as e:
    print(f"Elemento não encontrado na página: {e}")
except WebDriverException as e:
    print(f"Erro no WebDriver: {e}")

driver.get("https://app.nubimetrics.com/search/layout#?op1=q-searchTypeOption3-icPubliActivas&op2=fonte%2060a%20jfa&category=")

time.sleep(5)
cookies_list = []

cookies = driver.get_cookies()
for cookie in cookies:
    objeto = cookie['name']
    value = cookie['value']
    cookies_list.append(f"{objeto}={value};")

cookie = "".join(cookies_list)
driver.quit()
# cookie = "template=template-light; ai_user=EgV55|2024-05-28T11:45:48.501Z; _fbp=fb.1.1716896748573.875911634; lang_nubi=pt_br; hubspotutk=3b227fd6020f103ba35ecca053547573; intercom-id-re8wm274=4a6e9f6a-7d60-4e66-9f7b-3ff7f52b76be; intercom-device-id-re8wm274=76824f0d-e71f-4d6b-8781-c222868a73aa; _ga=GA1.3.836422724.1716896749; _gid=GA1.2.22320633.1718015641; _ce.clock_event=1; _ce.clock_data=117%2C177.91.74.213%2C1%2Cc92baae71318dc81de51a663df2f8b4f%2CChrome%2CBR; _gid=GA1.3.22320633.1718015641; TiPMix=68.25532366585887; x-ms-routing-name=self; ARRAffinity=79eeb4b54e604f617f684d7356612a15816484c3a7ec082ffde6984b94014e04; ARRAffinitySameSite=79eeb4b54e604f617f684d7356612a15816484c3a7ec082ffde6984b94014e04; i18next=pt_br; _ce.irv=returning; cebs=1; _hp2_ses_props.2056355555=%7B%22ts%22%3A1718100095134%2C%22d%22%3A%22app.nubimetrics.com%22%2C%22h%22%3A%22%2Faccount%2Flogin%22%2C%22q%22%3A%22%3FReturnUrl%3D%252fopportunity%252fcategoryDetail%22%2C%22g%22%3A%22%23%3Fcategory%3DMLB5672-MLB1747-MLB114675-MLB45905%22%7D; _clck=1ukw5r7%7C2%7Cfmj%7C0%7C1609; __hstc=154116135.3b227fd6020f103ba35ecca053547573.1716896751921.1718049731701.1718100102444.37; __hssrc=1; _gcl_au=1.1.81739417.1716896749.1599049596.1718100121.1718100123; ASP.NET_SessionId=b5adhrqkofmqmao1b1rc4y5o; .ASPXAUTH=4789A260E18C89FCF79F50CC9C0EF0052722D15240E44C1F2D28C0298D5909543419AAEBD46A502D3A8F483C1DF190E93246ECBDF4C2BDCD1D427C4AE689B464EA162C0175948F2059376A29C22F56A8E2160A00D5E11CA1683DBB9084C0A2E919757EFB44F4B4DB1651EC02347937DADF1C9C2F5ACDA952C83B3ECCE87725117028D3F4EDF093C75F90CE3CEB35D2A6D6391CF96C35242873EDF100FFEF0FA4F840975729EBA77CDFCF4AC422EAD1A243B6718F5C0FA9950E17F680F3289891FF5945F2DACCC4B64CBAFB1AC15D1D765D85748CB3B4F84F5A77AEE9028E2D5F4D4E6B854B999F8430AC12E1B96BA977D620CF33B61E534A140B72F4BCF679B6; _ga=GA1.1.836422724.1716896749; _uetsid=f3bc7b10271411efa1bdb337a018ae5f; _uetvid=d4f1f2b01ce711efb06041a93bf318c4; cebsp_=2; _clsk=9h5rwt%7C1718100132757%7C2%7C1%7Cs.clarity.ms%2Fcollect; _hp2_id.2056355555=%7B%22userId%22%3A%221540691698154969%22%2C%22pageviewId%22%3A%221686909635118599%22%2C%22sessionId%22%3A%2261152993371345%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; __hssc=154116135.2.1718100102444; intercom-session-re8wm274=MmpBSFA2WXFPNUkzaC9wUW1aKzQ0WTZHbDZoc2VnTDF4a3o1MVBURmNUckQ3ZFJQb0pPTTJqSHJuLzBhUVJZOC0tTzZRTStVNE14RFNEZzZjZFBaUlMvQT09--a68e02f23ef3ecd3b01beee744de230eb8c749a6; _ga_X9JW5VPF68=GS1.1.1718100094.19.1.1718100227.60.0.0; _ga_26N5SV28FF=GS1.1.1718100094.61.1.1718100227.60.0.0; _ga_1BD6V1LPWP=GS1.1.1718100094.40.1.1718100227.60.0.0; _ce.s=v~7baa07f6ad267a180f8618e02b13f0b27eb93927~lcw~1718100217156~lva~1718100095462~vpv~17~v11.fhb~1718100131642~v11.lhb~1718100191669~v11.cs~229172~v11.s~965ae320-27d9-11ef-b617-6fe6200ecabb~v11.sla~1718100227797~v11.send~1718100207202~lcw~1718100227798; sc_is_visitor_unique=rx12923916.1718100230.D55E01C3D14F4F03DEB97B398CBAA0C5.34.25.20.18.12.10.4.4.2; ai_session=OunLY|1718100095207|1718100232246.4"
make_req(cookie)

    
    


# async def main():
#     async with httpx.AsyncClient() as client:
#         url = "https://app.nubimetrics.com/account/login"
#         payload = {
#             'email': 'carlosbartojr@yahoo.com',
#             'password': 'JFA2004'
#         }
#         response = await client.post(url, data=payload)
#         print(response.cookies)
#         cookie_new = response.cookies.get(".ASPXAUTH")
#         ARRAffinitySameSite = response.cookies.get("ARRAffinitySameSite")
#         ARRAffinity = response.cookies.get("ARRAffinity")
#         make_req(cookie_new, ARRAffinitySameSite, ARRAffinity)
        
# asyncio.run(main())
