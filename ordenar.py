import re
import docx
import os
from docx.enum.text import WD_ALIGN_PARAGRAPH 
from docx.shared import Inches 
from spire.doc.common import *
from spire.doc import *


naoIndentificado= []
storm40 = []
storm60 = []
lite60 = []
lite70 = []
storm70 = []
bob90 = []
storm120 = []
lite120 = []
bob120 = []
storm200 = []
lite200 = []
mono200 = []
bob200 = []


def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def read_text(text):
    items = []
    current_item = {}

    # Divide o texto em itens separados
    item_texts = re.split(r'-{5,}', text)

    for item_text in item_texts:
        lines = item_text.strip().split('\n')
        for line in lines:
            if line.startswith("Modelo:"):
                if current_item:
                    if current_item:
                        if current_item['Modelo'] == "Nao indentificado":
                            naoIndentificado.append(format_item_dif(current_item))
                        if current_item['Modelo'] == "FONTE 40A":
                            storm40.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 60A LITE":
                            lite60.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 60A":
                            storm60.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 70A LITE":
                            lite70.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 70A":
                            storm70.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 90 BOB":
                            bob90.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 120":
                            storm120.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 120A LITE":
                            lite120.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 120 BOB":
                            bob120.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 200A":
                            storm200.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 200A LITE":
                            lite200.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 200 BOB":
                            bob200.append((format_item(current_item), current_item['Loja']))
                        if current_item['Modelo'] == "FONTE 200 MONO":
                            mono200.append((format_item(current_item), current_item['Loja']))
                        current_item = {}
                current_item['Modelo'] = line.split("Modelo:", 1)[1].strip()
                
            elif line.startswith("URL:"):
                current_item['URL'] = line.split("URL:", 1)[1].strip()
            elif line.startswith("Nome:"):
                current_item['Nome'] = line.split("Nome:", 1)[1].strip()
            elif line.startswith("Preço:"):
                current_item['Preço'] = line.split("Preço:", 1)[1].strip()
            elif line.startswith("Preço Previsto:"):
                current_item['Preço Previsto'] = line.split("Preço Previsto:", 1)[1].strip()
            elif line.startswith("Loja:"):
                current_item['Loja'] = line.split("Loja:", 1)[1].strip()
            elif line.startswith("Tipo:"):
                current_item['Tipo'] = line.split("Tipo:", 1)[1].strip()
            elif line.startswith("Lugar:"):
                current_item['Lugar'] = line.split("Lugar:", 1)[1].strip()
                
        if current_item:
            if current_item['Modelo'] == "Nao indentificado":
                naoIndentificado.append(format_item_dif(current_item))
            if current_item['Modelo'] == "FONTE 40A":
                storm40.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 60A LITE":
                lite60.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 60A":
                storm60.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 70A LITE":
                lite70.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 70A":
                storm70.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 90 BOB":
                bob90.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 120":
                storm120.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 120A LITE":
                lite120.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 120 BOB":
                bob120.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 200A":
                storm200.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 200A LITE":
                lite200.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 200 BOB":
                bob200.append((format_item(current_item), current_item['Loja']))
            if current_item['Modelo'] == "FONTE 200 MONO":
                mono200.append((format_item(current_item), current_item['Loja']))
            current_item = {}


def format_item(item):
    formatted_item = f"{item['Loja']} – {item['Lugar']} – Preço Anúncio: R$ {item['Preço']} – Preço Política: R$ {item['Preço Previsto']} ({item['Tipo']})\n{item['URL']}\n"
    return formatted_item

def format_item_dif(item):
    formatted_item = f"{item['URL']}\n"
    return formatted_item
lojas = {}

for item_path in os.listdir(r"dados/"):
    file_path = os.path.join(r"dados/", item_path)
    text = read_docx(file_path)

    read_text(text)

output_doc = docx.Document()
for item in storm40:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 40A"))
for item in lite60:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 60A LITE"))
for item in storm60:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 60A"))
for item in lite70:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 70A LITE"))
for item in storm70:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 70A"))
for item in bob90:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 90 BOB"))
for item in bob120:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 120 BOB"))
for item in lite120:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 120A LITE"))
for item in storm120:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 120"))
for item in bob200:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 200 BOB"))
for item in lite200:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 200A LITE"))
for item in mono200:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 200 MONO"))
for item in storm200:
    if item[1] not in lojas:
        lojas[item[1]] = []
    lojas[item[1]].append((item[0], "FONTE 200A"))
for i in lojas:
    output_doc.add_paragraph().add_run(f"*{i}*\n").bold = True
    for item, modelo in lojas[i]:
        output_doc.add_paragraph(f"{modelo} - {item}").paragraph_format.left_indent = Inches(0.5)
        
output_doc.save(r'dados_extraidos.docx')