import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configure API key ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Initialize model with fixed system prompt ---
system_prompt = "Speaking in causual mode and giveing perfect answers to the users"
model = genai.GenerativeModel(os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash"))

st.title("🫥😐🤨🙄😶")

# User prompt only
prompt = st.text_area("Enter your prompt:", height=100)

# Generation parameters
#col1, col2, col3 = st.columns(3)
#with col1:
#    temp = st.slider("Temperature (Creativity)", 0.1, 1.0, 0.7)
#with col2:
#    max_tokens = st.slider("Max Tokens (Output Length)", 1000, 10000, 5000)
#with col3:
#    top_p = st.slider("Top-p (Probability Sampling)", 0.1, 1.0, 0.9)

# Generate output
if st.button("If U HAVE guts THEN CLick It"):
    try:
        response = model.generate_content(
            prompt,
#            generation_config={
#                "temperature": temp,
#                "max_output_tokens": max_tokens,
#                "top_p": top_p
#            }
        )
        # Combine system prompt with user prompt
        full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
        
        response = model.generate_content(full_prompt)
        
        if response.text:
            st.subheader("🪄 Output:")
            st.write(response.text)
        else:
            st.error("No response generated. The content may have been filtered.")
            
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
