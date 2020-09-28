import requests
from bs4 import BeautifulSoup        
import csv

def parse_scp(scp_num):

    URL = 'http://www.scp-wiki.net/scp-'+str(scp_num)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')

    page_content = soup.find(id='page-content')
    info = page_content.find_all(['p','blockquote','ul','li'])

    imp_headers = [] #index 0 = Item , 1 = Object Class, 2 = Special Containment Procedures
    descriptions = []#holds scp description
    details = []#holds misc details not covered in imp_headers and descriptions

    for i in range(len(info)-1):
        content = info[i].contents

        if "Item #:" in content[0]:
            if len(content)>1:
                imp_headers.append(content[1:])
            while('Object Class:' not in info[i+1].contents[0]):
                if '\n' in info[i+1].contents[0:]:
                    info[i+1].contents[0:].remove('\n')
                imp_headers.append(str(info[i+1].contents[0:]).strip())
                i+=1
        elif 'Object Class:' in content[0]:
            if len(content)>1:
                imp_headers.append(content[1:])
            while('Special Containment Procedures:' not in info[i+1].contents[0]):
                if '\n' in info[i+1].contents[0:]:
                    info[i+1].contents[0:].remove('\n')
                imp_headers.append(str(info[i+1].contents[0:]).strip())
                i+=1
        elif 'Special Containment Procedures:' in content[0]:
            if len(content)>1:
                imp_headers.append(content[1:])
            while('Description:' not in info[i+1].contents[0]):
                if '\n' in info[i+1].contents[0:]:
                    info[i+1].contents[0:].remove('\n')
                imp_headers.append(str(info[i+1].contents[0:]).strip())
                i+=1
        elif 'Description:' in content[0]:
            descriptions.append(content[1])
            for j in range(2,len(content)):
                if '<strong>' not in content[j]: 
                    descriptions.append(content[j]) 
        else:
            while '\n' in content:
                content.remove('\n')
            for i in content:
                if list(str(i).strip()) not in imp_headers and list(str(i).strip()) not in descriptions: 
                    details.append(str(i).strip())
                else:
                    continue

    descriptions = [i for i in descriptions if len(i)>=1]
    details = [i for i in details if len(i)>=1]
    imp_headers = [i for i in imp_headers if len(i)>=1]

    return imp_headers,descriptions,details

blacklisted = []

'''imp_headers,descriptions,misc = parse_scp(1893)

print('HEADERS:\n',imp_headers,'\n')
print('DESCRIPTION:\n',descriptions,'\n')
print('MISCELLANEOUS:\n',misc,'\n')'''

with open('D:\\Datasets\\test_scp_store.csv',mode='w',encoding='utf-8') as test:
    headers = ['SCP_Number','Object_Class','Special_Containment_Procedures','Description','Misc_Details']
    writer = csv.DictWriter(test,fieldnames=headers)
    writer.writeheader()
    print('writing to csv...')
    for i in range(1001,2000):
        if i%100==0:
            print(i,'th iteration')
        try:
            imp,desc,misc = parse_scp(i)
            writer.writerow({'SCP_Number':imp[0],'Object_Class':imp[1],
                            'Special_Containment_Procedures':imp[2:],'Description':desc,
                            'Misc_Details':misc})
        except IndexError:
            blacklisted.append(i)

print('done writing to csv')
black = open('D:\\Datasets\\blacklisted_scp.txt','a')
for scp in blacklisted:
    black.write(str(scp))
print('done writing indexerror causing scps')
