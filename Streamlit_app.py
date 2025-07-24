# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """**Choose the fruits you want in your custom Smoothie!**
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select((col('FRUIT_NAME')))


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string=''
# converting list into string
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

# 🥋 Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                        values('"""+ingredients_string+ """','"""+name_on_order+ """')"""
 
    #add submit order button
    time_to_insert = st.button('Submit Order')
    # inserting data into snowflake table
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    
# New Section to display smoothie fruit nutrition information
import requests
smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())




