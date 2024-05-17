import streamlit as st
import pandas as pd


# Sample data: items table, warehouse tables

@st.cache_data
def load_model(model_name, sheet_name=None):
    if sheet_name:
        data = pd.read_excel(model_name, sheet_name=sheet_name)
    else:
        data = pd.read_excel(model_name)
    return data

items_data = load_model('Items B2B data.xlsx','Items B2B')
wh1_df = load_model('Stocks Warehouse wise/Sunkadkate.xlsx')
wh2_df = load_model('Stocks Warehouse wise/Makali.xlsx')
wh3_df = load_model('Stocks Warehouse wise/Magadi.xlsx')

# Inspect columns of items_data and wh1_df
st.write("Columns of items_data:", items_data.columns)
st.write("Columns of wh1_df:", wh1_df.columns)
# Merge warehouse tables with items table

# First Merge with Warehouse1
merge_df = pd.merge(items_data,wh1_df,left_on='Item SKU',right_on='sku',how='left').fillna(0)[['AY','Grades','Volume','Subject','Item Name','Item Category', 'Item SKU', 'quantity_available']]
# Rename 'quantity_available' column to 'Quantity_Warehouse1'
merge_df.rename(columns={'quantity_available': 'Sunkadkate'}, inplace=True)

# Second Merge with Warehouse2
merge_df = pd.merge(merge_df,wh2_df,left_on='Item SKU',right_on='sku',how='left').fillna(0)[['AY','Grades','Volume','Subject','Item Name','Item Category', 'Item SKU','Sunkadkate', 'quantity_available']]
merge_df.rename(columns={'quantity_available':'Makali'},inplace=True)

# Third Merge with Warehouse3
merge_df = pd.merge(merge_df,wh3_df,left_on='Item SKU',right_on='sku',how='left').fillna(0)[['AY','Grades','Volume','Subject','Item Name','Item Category', 'Item SKU','Sunkadkate','Makali' ,'quantity_available']]
merge_df.rename(columns={'quantity_available':'Magadi'},inplace=True)

#Total Stock Column
merge_df['Total Stock']= merge_df['Sunkadkate']+merge_df['Makali']+merge_df['Magadi']

# Sidebar
st.sidebar.header('Filter')
ay = st.sidebar.multiselect('AY',merge_df['AY'].unique())
grades = st.sidebar.multiselect('Grades',merge_df['Grades'].unique())
category = st.sidebar.multiselect('Item Category',merge_df['Item Category'].unique())

# Select AY
if not ay:
    merge_df2 = merge_df.copy()
else:
    merge_df2 = merge_df[merge_df['AY'].isin(ay)]
    
# Select Grade 
if not grades:
    merge_df3 = merge_df2.copy()
else:
    merge_df3 = merge_df2[merge_df2['Grades'].isin(grades)]
    
# Select Category
if not ay and not grades and not category:
    filter_df = merge_df.copy()
elif not grades and not category:
    filter_df = merge_df[merge_df['AY'].isin(ay)]
elif not ay and not category:
    filter_df = merge_df[merge_df['Grades'].isin(grades)]
elif not ay and not grades:
    filter_df = merge_df[merge_df['Item Category'].isin(category)]
    

# Merge Table
st.subheader('Stock Details')
st.write(merge_df3)


st.pyplot




