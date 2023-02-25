import requests as r
import pandas as pd
import csv
import json


def main():
    headers_dict = {"API_KEY": "85f432d9-c835-443a-8542-569cca4c3e13"}
    URL = "https://apps.fas.usda.gov/OpenData/api/psd/commodity/0044000/country/all/year/2020"
    Commodity=["0410000", "0422110", "0451000", "0459200", "0612000", "0577901", "0577907", "0011000", "0013000", "0111000", "0113000", "0115000",
           "0223000", "0224200", "0224400", "0230000", "0240000", "0430000", "0440000", "0452000", "0459100", "0459900", "0572120", "0572220",
           "0574000", "0575100", "0577400", "0579305", "0711100", "0813100", "0813101", "0813200", "0813300", "0813500", "0813600", "0813700",
           "0813800", "0814200", "2631000", "4233000", "4235000", "4242000", "4243000", "4244000", "4234000", "4239100", "4232000", "4232001",
           "4236000", "2231000", "2223000", "2232000", "2221000", "2226000", "2222000", "2222001", "2224000", "0585100", "0571120", "0579309",
           "0579220", "0571220"]
    for i in Commodity:
        for j in range(1980, 2020):
            header= {'API_KEY': 'A9015057-C160-4A5B-8666-63F7BE89AFAE','accept': 'application/json', 'accept': 'text/csv'}
            url='https://apps.fas.usda.gov/PSDOnlineDataServices/api/CommodityData/GetCommodityDataByYear?'
            commodityCode = i
            marketYear = str(j)
            X= url+'commodityCode='+commodityCode+'&marketYear='+marketYear
            #print(x)
            response=r.get(X)
            Jsonresponse=r.get(X,headers=header).json()
            #print(response.status_code)
            content = json.dumps(Jsonresponse, indent = 2, sort_keys=True)
            print(content)
            df=json.loads(content)
            path=i+'_'+str(j)+'.csv'
            with open(path, 'w') as file:
                csv_file=csv.writer(file)
                csv_file.writerow(['Attribute', 'Commodity', 'Country','MarketYear','Unit','Value'])
                for item in df:
                    csv_file.writerow([item['AttributeDescription'],item['CommodityDescription'],item['CountryName'],item['MarketYear'],item['UnitDescription'],item['Value']])


    

    #wData = r.get(url=URL, headers=headers_dict)
    print(URL)
    print(r.get(url = URL, headers = headers_dict))




if __name__ == "__main__":
    main()