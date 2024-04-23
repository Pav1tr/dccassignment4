import fitz as fz
import pandas as pd

pdf1=fz.open('purchase details.pdf')
pgcount1=pdf1.page_count
purchase=pd.DataFrame()
for i in range(0,pgcount1):
    page1=pdf1[i]
    table1=page1.find_tables()
    purchase=pd.concat([purchase,table1[0].to_pandas()])
purchase.to_csv('purchase.csv',index=False)
pdf1.close()

pdf2=fz.open('redemption details.pdf')
pgcount2=pdf2.page_count
redemption=pd.DataFrame()
for j in range(0,pgcount2):
    page2=pdf2[j]
    table2=page2.find_tables()
    redemption=pd.concat([redemption,table2[0].to_pandas()])
redemption.to_csv('redemption.csv',index=False)
pdf2.close()