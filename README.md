# foodieapp
# AI Restaurant Recommender Chatbot

This is a Streamlit-based chatbot that recommends the best restaurants near your location using Google search and stores chat history using Supabase.

## Features

- Chatbot interface to ask food-related queries
- Suggests top restaurants with clickable links
- Stores and retrieves chat history using Supabase
- Supports Google Search via Gemini AI

## Project Structure

food-bot-chat/
├── app.py                # Main Streamlit app
├── .env                  # Environment variables (not pushed to GitHub)
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── utils/
    ├── tools.py          # Handles Gemini API and restaurant search logic
    └── memory.py         # Supabase integration for storing chat memory
