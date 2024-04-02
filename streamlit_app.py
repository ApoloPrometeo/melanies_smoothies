# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on Snoothie')
st.write('The name on your Smoothie will be', name_on_order)



##option = st.selectbox(
##    'What is your favorite fruit?',
##    ('Banana', 'Strawberry', 'Peaches'))

##st.write('You favorite fruit is:', option)


## Display the Fruit Options List in Your Streamlit in Snowflake (SiS) App.
session = get_active_session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
##st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen

    st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients)
                        values('""" + ingredients_string + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order');

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


