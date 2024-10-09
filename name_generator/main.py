from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os

# Load environment variables
load_dotenv()

# Load the Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize the LLM model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=gemini_api_key)

# Streamlit UI title
st.title("Restaurant Name Generator")

# Prompt template for restaurant name generation
prompt_name = PromptTemplate.from_template(
    "I want to open a restaurant for {cuisine} food. Suggest only a single name for this. There should only be one name."
)

# Generate restaurant name using cuisine
cuisine = st.text_input("Enter a cuisine type", "Punjabi")  # Input box in Streamlit for cuisine type
if st.button("Generate Restaurant Name"):

    chain = prompt_name | llm
    restaurant_name_response = chain.invoke({"cuisine": cuisine})
    # restaurant_name_prompt = prompt_name.format(cuisine=cuisine)
    # restaurant_name_response = llm(restaurant_name_prompt)
    restaurant_name = restaurant_name_response.content.strip()  # Extract the name

    # Display the restaurant name
    st.subheader(f"Restaurant Name: {restaurant_name}")

    # Now, use the restaurant name to generate menu items
    prompt_menu = PromptTemplate.from_template(
        "Suggest only ten menu items for the restaurant name {restaurant_name}. Return it as comma-separated."
    )
    
    #menu_prompt = prompt_menu.format(restaurant_name=restaurant_name)
    menu_chain = prompt_menu | llm
    #menu_response = llm(menu_prompt)
    menu_response = menu_chain.invoke({"restaurant_name": restaurant_name})
    print("menu-response: ",menu_response)
    menu_items = menu_response.content.strip()  # Extract menu items

    secttions = menu_items.split(",")

    # Display the menu
    st.subheader("Menu Suggestions:")
    for section in secttions:

        st.write("-", section)
