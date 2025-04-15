import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from utils.tools import search_restaurants

load_dotenv()

# Load API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# App UI
st.set_page_config(page_title="🍽️ Gemini Restaurant Chatbot")
st.title("🍽️ FoodieBot – Your AI Food Guide")
st.markdown("Chat with me to discover **awesome food places near you!** 🍕🍜")

# Chat history memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your food buddy 🍔. Tell me what you're craving and where!"}
    ]
if "user_prefs" not in st.session_state:
    st.session_state.user_prefs = {}

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_query := st.chat_input("What do you feel like eating today?"):
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        # Use Gemini to extract info and craft a response
        prompt = f"""
You're a restaurant chatbot. The user asked: "{user_query}"

1. If they mention a cuisine or dish (e.g., biryani, pizza, dosa), identify it.
2. If they mention a location (like Mumbai, Delhi, Tirunelveli), extract it.
3. Then use those to form a search query like "best biryani places in Mumbai".
Return a short summary to show and suggest 3-5 restaurant links.
If nothing is found, ask them to rephrase.

Return format:
- Cuisine: xxx
- Location: xxx
- Suggested query: xxx
"""

        gemini_response = model.generate_content(prompt)
        response_text = gemini_response.text

        # Extract location + dish from response using basic parsing (for now)
        try:
            lines = response_text.splitlines()
            cuisine = lines[0].split(":")[1].strip()
            location = lines[1].split(":")[1].strip()
            search_query = lines[2].split(":")[1].strip()
        except:
            cuisine = "food"
            location = "your city"
            search_query = user_query

        # Save preferences in memory
        st.session_state.user_prefs["last_cuisine"] = cuisine
        st.session_state.user_prefs["last_location"] = location

        # Call search
        with st.spinner("Finding some delicious spots... 🍽️"):
            search_results = search_restaurants(search_query, location)

        if search_results.get("organic"):
            st.markdown(f"Here are some top places for **{cuisine}** in **{location}**:")
            for r in search_results["organic"][:5]:
                st.subheader(r.get("title"))
                st.write(r.get("snippet"))
                st.markdown(f"[🌍 View on Map]({r.get('link')})", unsafe_allow_html=True)
        else:
            st.warning("I couldn’t find anything. Maybe try rephrasing?")

        # Add bot response to memory
        st.session_state.messages.append({"role": "assistant", "content": response_text})
