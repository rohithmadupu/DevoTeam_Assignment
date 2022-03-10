#!/usr/bin/env python
# coding: utf-8

# ### EDA
# The Notebook gives an EDA of the dataset provided. We are looking at the transactions provided in the dataset and hightlight any issues in the data.


###Importing Libraries required
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt


###Path for the url at which the data is saved
csv_url = "https://raw.githubusercontent.com/rohithmadupu/DevoTeam_Assignment/main/ecommerce_data.csv"



###reading the csv and displaying head
df_ecomm = pd.read_csv(csv_url)
df_ecomm.head()



###Getting schema of the dataframe imported
df_ecomm.dtypes


# In[5]:


##Converting customer Id and estore ID to string
###for customerid  -> also removing .0 at the end
df_ecomm["CustomerID"] = df_ecomm["CustomerID"].astype("str")
df_ecomm["CustomerID"] = df_ecomm["CustomerID"].str.replace('.0', '')
df_ecomm["Estore_id"] = df_ecomm["Estore_id"].astype("str")




####Checking if both Invoice Dates match and then removing one
if (df_ecomm['InvoiceDate'].equals(df_ecomm['InvoiceDate.1']) == True):
    df_ecomm = df_ecomm.drop(["InvoiceDate.1"], axis = 1)


###creating a datefield and year field from Invoice Date
df_ecomm['Date'] = pd.to_datetime(df_ecomm.InvoiceDate,errors='coerce').dt.date

df_ecomm['Year'] = pd.to_datetime(df_ecomm.InvoiceDate,errors='coerce').dt.year



###Getting dimensions of the Dataframe
df_ecomm.shape


###Min and Max dates for which the data is available
f"Min and Max dates are {df_ecomm['Date'].min()} and {df_ecomm['Date'].max()}"

###Count of nulls by Column
print(df_ecomm.isnull().sum(axis=0))   # Around 120k nulls in Stockcode,desc and quantity. No nulls in others


###count of negative values in Quantity and Unit Price 
print(f"Negative Values in Quantity Column are {(df_ecomm['Quantity'] < 0).sum()}\n       Negative Values in UnitPrice Column are {(df_ecomm['UnitPrice'] < 0).sum()}")

###Comment - No nulls in unit price

#### Getting number of transactions by Date
df_ecomm_cnt = pd.DataFrame(df_ecomm.groupby('Date').size().rename('Count').reset_index())
df_ecomm_cnt.sort_values(by=['Count'], ascending=False)
#--most transactions on 2011-October-6th and least on 2011-Feb-06


###Unique values by column excluding Nans

df_ecomm.dropna().nunique()


### Line plot - Count of transactions by Date
plt.figure(figsize = (15,8))
sns.lineplot(x = 'Date', y = 'Count',data = df_ecomm_cnt)



###Number of Transactions by Year
df_yr_cnt = df_ecomm.groupby(['Year']).size().rename('Count').reset_index()

plt.figure(figsize = (15,8))

(
    sns.barplot(x = 'Year',
                y = 'Count',
                data = df_yr_cnt,
                order = df_yr_cnt.sort_values("Count",ascending = False).Year,
                palette = "Blues_r")
)



###Number of transactions by Store 
df_store_cnt = df_ecomm.groupby(['Estore_id']).size().rename('Count').reset_index()
plt.figure(figsize = (15,8))

(
    sns.barplot(x = 'Estore_id',
                y = 'Count',
                data = df_store_cnt,
                order = df_store_cnt.sort_values("Count",ascending = False).Estore_id,
                palette = "Blues_r")
)



###Number of transactions by Customer ID 
df_cust_cnt = df_ecomm.groupby(['CustomerID']).size().rename('Count').reset_index()
plt.figure(figsize = (15,8))

(
    sns.barplot(x = 'CustomerID',
                y = 'Count',
                data = df_cust_cnt,
                order = df_cust_cnt.sort_values("Count",ascending = False).CustomerID[1:20],
                palette = "Blues_r")
)



###Number of transactions by Invoice number
df_inv_cnt = df_ecomm.groupby(['InvoiceNo']).size().rename('Count').reset_index()
plt.figure(figsize = (15,8))

(
    sns.barplot(x = 'InvoiceNo',
                y = 'Count',
                data = df_inv_cnt,
                order = df_inv_cnt.sort_values("Count",ascending = False).InvoiceNo[1:20],
                palette = "Blues_r")
)



###Number of transactions by Country
df_cntry_cnt = df_ecomm.groupby(['Country']).size().rename('Count').reset_index()
plt.figure(figsize = (15,8))

(
    sns.barplot(x = 'Country',
                y = 'Count',
                data = df_cntry_cnt,
                order = df_cntry_cnt.sort_values("Count",ascending = False).Country,
                palette = "Blues_r")
)



###Number of transactions by StockCode
df_stock_cnt = df_ecomm.groupby(['StockCode']).size().rename('Count').reset_index()
plt.figure(figsize = (15,8))

(
    sns.barplot(x = 'StockCode',
                y = 'Count',
                data = df_stock_cnt,
                order = df_stock_cnt.sort_values("Count",ascending = False).StockCode[1:20],
                palette = "Blues_r")
)



###negative values by Date
df_ecomm_cnt_neg = pd.DataFrame(df_ecomm[(df_ecomm['Quantity'] < 0)].groupby('Date').size().rename('Count').reset_index())

plt.figure(figsize = (15,8))
sns.lineplot(x = 'Date', y = 'Count',data = df_ecomm_cnt_neg)

