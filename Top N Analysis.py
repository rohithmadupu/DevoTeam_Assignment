# ### Top N analysis
# The purpose of this notebook is to identify the top e-stores that contribute to the revenue of GloboSales. In addition,  top countries for GloboSales to focus on and their top e-stores are identified. For the analysis, the rows where quantity is negative have been removed 

###Importing Libraries required
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


###Path for the url at which the data is saved
csv_url = "https://raw.githubusercontent.com/rohithmadupu/DevoTeam_Assignment/main/ecommerce_data.csv"


###reading the csv and displaying head
df_ecomm = pd.read_csv(csv_url)
df_ecomm.head()


##Converting customer Id and estore ID to string
df_ecomm["CustomerID"] = df_ecomm["CustomerID"].astype("str")
df_ecomm["CustomerID"] = df_ecomm["CustomerID"].str.replace('.0', '')

df_ecomm["Estore_id"] = df_ecomm["Estore_id"].astype("str")

####Checking if both Invoice Dates match and then removing one
if (df_ecomm['InvoiceDate'].equals(df_ecomm['InvoiceDate.1']) == True):
    df_ecomm = df_ecomm.drop(["InvoiceDate.1"], axis = 1)
    
###creating a datefield
df_ecomm['Date'] = pd.to_datetime(df_ecomm.InvoiceDate,errors='coerce').dt.date

df_ecomm['Year'] = pd.to_datetime(df_ecomm.InvoiceDate,errors='coerce').dt.year


print(df_ecomm.isnull().sum(axis=0))


###Removing nulls and negative values from Quantity Column from analysis 
#Could be hindering our analysis. It could be a data quality issue 

df_ecomm_new = df_ecomm[df_ecomm['Quantity'] >= 0]

df_ecomm_new.head() ### 


###Creating a Revenue column
df_ecomm_new["Revenue"] = df_ecomm_new.Quantity * df_ecomm_new.UnitPrice


##Revenue by EstoreId
df_estore_rev = pd.DataFrame(df_ecomm_new.groupby(["Estore_id"]).agg({'Revenue': 'sum'}).reset_index())


plt.figure(figsize = (15,10))

sns.barplot(x = 'Estore_id',
            y = 'Revenue',
            order = df_estore_rev.sort_values(['Revenue'],ascending = False).Estore_id,
            data = df_estore_rev,
            palette = 'Blues_r')
 
plt.show()

###Top 5 Estores are 1,31,4,30,17


df = pd.DataFrame(df_estore_rev[["Revenue"]])
df.index = df_estore_rev["Estore_id"]
df = df.sort_values(by='Revenue',ascending=False)
df["cumpercentage"] = df["Revenue"].cumsum()/df["Revenue"].sum()*100
df


fig = plt.figure(figsize=(100,80), dpi=55)

fig, ax = plt.subplots()
ax.bar(df.index, df["Revenue"], color="C0")
ax2 = ax.twinx()
ax2.plot(df.index, df["cumpercentage"], color="C1", marker="D", ms=2)
ax2.yaxis.set_major_formatter(PercentFormatter())

ax.tick_params(axis="y", colors="C0")
ax2.tick_params(axis="y", colors="C1")


###Identifyng top customers for estores 1,31,4
df_estore_cust_rev = pd.DataFrame(df_ecomm_new.groupby(["Estore_id","CustomerID"]).agg({'Revenue': 'sum'}).reset_index())

df_estore_cust_rev = df_estore_cust_rev[df_estore_cust_rev.CustomerID != "nan"]


###estore1
df_es1 = (
    pd.DataFrame(
    df_estore_cust_rev[df_estore_cust_rev["Estore_id"] == "1"]
    .sort_values(by='Revenue',ascending=False)[["CustomerID","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'CustomerID',
            y = 'Revenue',
            data = df_es1,
            hue = "Estore_id")
 
plt.show()


###estore2
df_es2 = (
    pd.DataFrame(
    df_estore_cust_rev[df_estore_cust_rev["Estore_id"] == "31"]
    .sort_values(by='Revenue',ascending=False)[["CustomerID","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'CustomerID',
            y = 'Revenue',
            data = df_es2,
            hue = "Estore_id")
 
plt.show()


###estore3
df_es3 = (
    pd.DataFrame(
    df_estore_cust_rev[df_estore_cust_rev["Estore_id"] == "4"]
    .sort_values(by='Revenue',ascending=False)[["CustomerID","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'CustomerID',
            y = 'Revenue',
            data = df_es3,
            hue = "Estore_id")
 
plt.show()


###Identifyng top stocks for estores 1,31,4
df_estore_stock_rev = pd.DataFrame(df_ecomm_new.groupby(["Estore_id","StockCode"]).agg({'Revenue': 'sum'}).reset_index())
df_estore_stock_rev = df_estore_stock_rev[df_estore_stock_rev.StockCode != "nan"]


##estore1
df_es_stk1 = (
    pd.DataFrame(
    df_estore_stock_rev[df_estore_stock_rev["Estore_id"] == "1"]
    .sort_values(by='Revenue',ascending=False)[["StockCode","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'StockCode',
            y = 'Revenue',
            data = df_es_stk1,
            hue = "Estore_id")
 
plt.show()


###estore2
df_es_stk2 = (
    pd.DataFrame(
    df_estore_stock_rev[df_estore_stock_rev["Estore_id"] == "31"]
    .sort_values(by='Revenue',ascending=False)[["StockCode","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'StockCode',
            y = 'Revenue',
            data = df_es_stk2,
            hue = "Estore_id")
 
plt.show()


###estore3
df_es_stk3 = (
    pd.DataFrame(
    df_estore_stock_rev[df_estore_stock_rev["Estore_id"] == "4"]
    .sort_values(by='Revenue',ascending=False)[["StockCode","Revenue","Estore_id"]]
    .head(n= 10))
)

plt.figure(figsize = (10,7))

sns.barplot(x = 'StockCode',
            y = 'Revenue',
            data = df_es_stk3,
            hue = "Estore_id")
 
plt.show()

 ###Revenue by Country
df_country_rev = pd.DataFrame(df_ecomm_new.groupby(["Country"]).agg({'Revenue': 'sum'}).reset_index())


plt.figure(figsize = (15,10))

sns.barplot(x = 'Country',
            y = 'Revenue',
            order = df_country_rev.sort_values(['Revenue'],ascending = False).Country,
            data = df_country_rev,
            palette = 'Blues_r')
 
plt.show()

###Top 5 Countries are UK,Germany,France,EIRE,Netherlands

df_cntry = pd.DataFrame(df_country_rev[["Revenue"]])
df_cntry.index = df_country_rev["Country"]
df_cntry = df_cntry.sort_values(by='Revenue',ascending=False)
df_cntry["cumpercentage"] = df_cntry["Revenue"].cumsum()/df_cntry["Revenue"].sum()*100
df_cntry

fig = plt.figure(figsize=(10,8), dpi=100)

fig, ax = plt.subplots()
ax.bar(df_cntry.index, df_cntry["Revenue"], color="C0")
ax2 = ax.twinx()
ax2.plot(df_cntry.index, df_cntry["cumpercentage"], color="C1", marker="D", ms=2)
ax2.yaxis.set_major_formatter(PercentFormatter())

ax.tick_params(axis="y", colors="C0")
ax2.tick_params(axis="y", colors="C1")

plt.show()

###4 Countries UK,Germany,France,EIRE are contributing to 80% revenue -> goal is to focus more on them


###Identifyng top 3 Estores and customers for Countries UK,Germany,France,EIRE
df_country_estore_rev = pd.DataFrame(df_ecomm_new.groupby(["Country","Estore_id"]).agg({'Revenue': 'sum'}).reset_index())



####Identifying top e-stores associated with each country
###United Kingdom
df_uk_estore = (
    pd.DataFrame(
    df_country_estore_rev[df_country_estore_rev["Country"] == "United Kingdom"]
    .sort_values(by='Revenue',ascending=False)[["Country","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'Estore_id',
            y = 'Revenue',
            data = df_uk_estore,
            hue = "Country")
 
plt.show()


##Germany
df_de_estore = (
    pd.DataFrame(
    df_country_estore_rev[df_country_estore_rev["Country"] == "Germany"]
    .sort_values(by='Revenue',ascending=False)[["Country","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'Estore_id',
            y = 'Revenue',
            data = df_de_estore,
            hue = "Country")
 
plt.show()


###France
df_fr_estore = (
    pd.DataFrame(
    df_country_estore_rev[df_country_estore_rev["Country"] == "France"]
    .sort_values(by='Revenue',ascending=False)[["Country","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'Estore_id',
            y = 'Revenue',
            data = df_fr_estore,
            hue = "Country")
 
plt.show()


###EIRE
df_ir_estore = (
    pd.DataFrame(
    df_country_estore_rev[df_country_estore_rev["Country"] == "EIRE"]
    .sort_values(by='Revenue',ascending=False)[["Country","Revenue","Estore_id"]]
    .head(n= 10))
)


plt.figure(figsize = (10,7))

sns.barplot(x = 'Estore_id',
            y = 'Revenue',
            data = df_ir_estore,
            hue = "Country")
 
plt.show()

