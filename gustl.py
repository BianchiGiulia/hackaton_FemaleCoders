import streamlit as st
import pandas as pd
import random

# Load data
data = pd.read_csv('https://github.com/BianchiGiulia/hackaton_FemaleCoders/blob/main/clean_data2.csv')

# Initialize session state variables if not already present
if 'selected_cuisine' not in st.session_state:
    st.session_state['selected_cuisine'] = ""
if 'selected_prices' not in st.session_state:
    st.session_state['selected_prices'] = []
if 'selected_zip' not in st.session_state:
    st.session_state['selected_zip'] = ""

# Function for Random Recommendation
def random_recommendation():
    if not data.empty:
        random_restaurant = data.sample()
        restaurant_info = random_restaurant[['restaurant_name', 'address', 'avg_rating']]
        restaurant_info.reset_index(drop=True, inplace=True)
        restaurant_info.columns = ['Restaurant Name', 'Address', 'Average Rating']
        st.write("Here's a random restaurant recommendation:")
        st.dataframe(restaurant_info, hide_index=True, use_container_width=True)
    else:
        st.write("No data available for recommendations.")

# Function to handle the conversation based on user input or button click
def handle_conversation():
    # Display the question
    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = "What is your favorite type of food?"
    st.write("Gustl: " + st.session_state['current_question'])

    suggested_cuisines = ['Italian', 'Mexican', 'Chinese', 'American']
    cols = st.columns(len(suggested_cuisines))
    for i, cuisine in enumerate(suggested_cuisines):
        if cols[i].button(cuisine):
            st.session_state['selected_cuisine'] = cuisine
            st.session_state['selected_prices'] = []
            st.session_state['selected_zip'] = ""

    user_input = st.text_input("Or enter another type of food here:", st.session_state['selected_cuisine'], key="user_input")
    if user_input and user_input != st.session_state['selected_cuisine']:
        st.session_state['selected_cuisine'] = user_input
        st.session_state['selected_prices'] = []
        st.session_state['selected_zip'] = ""

    if st.session_state['selected_cuisine']:
        price_levels = ['€', '€€', '€€€']
        selected_prices = st.multiselect("Select price levels:", price_levels, key='price_select')
        if selected_prices:
            st.session_state['selected_prices'] = selected_prices

        zip_input = st.text_input("Enter a ZIP code to refine your search:", key="zip_input")
        if zip_input:
            st.session_state['selected_zip'] = zip_input

        if st.button('Show Restaurants'):
            filtered_restaurants = data[data['cuisines'].str.contains(st.session_state['selected_cuisine'], case=False, na=False)]
            if st.session_state['selected_prices']:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['price_level'].isin(st.session_state['selected_prices'])]
            if st.session_state['selected_zip']:
                filtered_restaurants = filtered_restaurants[filtered_restaurants['address'].astype(str).str.contains(st.session_state['selected_zip'])]

            if not filtered_restaurants.empty:
                result = filtered_restaurants[['restaurant_name', 'address', 'avg_rating']]
                result.reset_index(drop=True, inplace=True)
                result.columns = ['Restaurant Name', 'Address', 'Average Rating']
                st.dataframe(result, hide_index=True, use_container_width=True)
            else:
                st.write(f"No restaurants found for '{st.session_state['selected_cuisine']}' with prices '{', '.join(st.session_state['selected_prices'])}' in ZIP '{st.session_state['selected_zip']}'. Try another filter.")

def main():
    st.title('GourmetGustl')
    if 'init' not in st.session_state:
        st.session_state['init'] = True
        st.write("Hello! I'm a simple chatbot. Let's talk!")

    handle_conversation()

    # Sidebar for random recommendation
    if st.sidebar.button('Get Random Recommendation'):
        random_recommendation()

if __name__ == '__main__':
    main()
