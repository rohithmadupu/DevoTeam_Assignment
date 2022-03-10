#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys


# In[2]:


import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt


# In[3]:


csv_path = "C:/Users/lm185207/Desktop/case_studies/ecommerce_data.csv"

csv_url = "https://raw.githubusercontent.com/rohithmadupu/DevoTeam_Assignment/main/ecommerce_data.csv"


# In[4]:


df_ecomm = pd.read_csv(csv_url)


# In[5]:


df_ecomm.head()


# In[6]:


###Getting schema
df_ecomm.dtypes


# In[7]:


##Converting customer Id and estore ID to string
df_ecomm["CustomerID"] = df_ecomm["CustomerID"].astype("str")
df_ecomm["Estore_id"] = df_ecomm["Estore_id"].astype("str")


# In[8]:


####Checking if both Invoice Dates match and then removing one
if (df_ecomm['InvoiceDate'].equals(df_ecomm['InvoiceDate.1']) == True):
    df_ecomm = df_ecomm.drop(["InvoiceDate.1"], axis = 1)


# In[9]:


###creating a datefield
df_ecomm['Date'] = pd.to_datetime(df_ecomm.InvoiceDate,errors='coerce').dt.date


# In[10]:


###dimensions of df
df_ecomm.shape


# In[11]:


###Min and Max dates
f"Min and Max dates are {df_ecomm['Date'].min()} and {df_ecomm['Date'].max()}"


# In[12]:


####EDA - Number of records by Date
df_ecomm_cnt = pd.DataFrame(df_ecomm.groupby('Date').size().rename('Count').reset_index())


# In[13]:


df_ecomm_cnt.sort_values(by=['Count'], ascending=False)
####most records on 2011-October-6th and least on 2011-Feb-06


# In[14]:


plt.figure(figsize = (15,8))
sns.lineplot(x = 'Date', y = 'Count',data = df_ecomm_cnt)


# In[15]:


##Count of nulls by Column
print(df_ecomm.isnull().sum(axis=0))


# In[16]:


###count of negative values in Quantity and Unit Price
print(f"Negative Values in Quantity Column are {(df_ecomm['Quantity'] < 0).sum()}\n       Negative Values in UnitPrice Column are {(df_ecomm['UnitPrice'] < 0).sum()}")


# In[24]:


###negative values by Date
df_ecomm_cnt_neg = pd.DataFrame(df_ecomm[(df_ecomm['Quantity'] < 0)].groupby('Date').size().rename('Count').reset_index())

plt.figure(figsize = (15,8))
sns.lineplot(x = 'Date', y = 'Count',data = df_ecomm_cnt_neg)


# In[18]:


###Unique values by column excluding Nans

df_ecomm.dropna().nunique()

