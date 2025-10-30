import streamlit as st
from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

# Page config
st.set_page_config(page_title="Simple CrewAI Demo", page_icon="🤖", layout="wide")

# Title
st.title("🤖ASK me anything👽")
st.markdown("**Three AI agents work together to create an article!**")

# Load env and set key for LiteLLM
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY", "")
if groq_key:
    os.environ["GROQ_API_KEY"] = groq_key

# Topic input
st.header("📝 What should the agents write about?")
topic = st.text_input(
    "Enter a topic:",
    value="How AI is changing education",
    placeholder="e.g., Benefits of renewable energy, Future of space travel..."
)

# Run the crew
if st.button("🚀 Run the AI Agents!", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic!")
    else:
        with st.spinner("🤖 AI agents are working together..."):
            try:
                # Create agents directly (no caching)
                researcher = Agent(
                    role="Researcher",
                    goal="Find interesting facts about the topic",
                    backstory="You are a curious researcher who loves finding cool facts.",
                    llm="groq/llama-3.1-8b-instant",
                    tools=[],
                    verbose=True
                )
                
                writer = Agent(
                    role="Writer",
                    goal="Write a simple, engaging article",
                    backstory="You write in simple language that anyone can understand.",
                    llm="groq/llama-3.1-8b-instant",
                    tools=[],
                    verbose=True
                )
                
                editor = Agent(
                    role="Editor", 
                    goal="Make the article perfect",
                    backstory="You fix grammar and make everything clear and organized.",
                    llm="groq/llama-3.1-8b-instant",
                    tools=[],
                    verbose=True
                )
                
                # Create tasks
                research_task = Task(
                    description=f"Research and find 5 interesting facts about: {topic}",
                    expected_output="A list of 5 interesting facts with brief explanations",
                    agent=researcher
                )
                
                write_task = Task(
                    description="Write a short article (3-4 paragraphs) using the research facts",
                    expected_output="A well-structured article with introduction, main points, and conclusion",
                    agent=writer
                )
                
                edit_task = Task(
                    description="Edit the article to make it perfect - fix grammar, improve flow, add a catchy title",
                    expected_output="A polished final article with a great title",
                    agent=editor
                )
                
                # Create crew
                crew = Crew(
                    agents=[researcher, writer, editor],
                    tasks=[research_task, write_task, edit_task],
                    process=Process.sequential,
                    verbose=True
                )
                
                # Run the crew
                result = crew.kickoff()
                
                # Display results
                st.success("✅ Done! Here's what the agents created:")
                st.markdown("---")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"❌ Something went wrong: {str(e)}")
                st.info("Try checking your API key or trying a different topic.")

# How it works section
with st.expander("🔍 How does this work?"):
    st.markdown("""
    **The Three Agents:**
    
    1. **🔍 Researcher** - Finds interesting facts about your topic
    2. **✍️ Writer** - Turns those facts into a readable article  
    3. **📝 Editor** - Fixes grammar and makes it perfect
    
    **The Process:**
    - Each agent does their job one after another
    - They pass information to each other
    - The final result is a polished article!
    
    **Why This is Cool:**
    - Each agent has a specific job (like a real team)
    - You can change what each agent does
    - You can add more agents or different tasks
    """)

# Tips section
with st.expander("💡 Tips for Better Results"):
    st.markdown("""
    **For better articles:**
    - Be specific with your topic (e.g., "AI in healthcare" vs "AI")
    - Use topics you're interested in
    - Try different topics to see how agents adapt
    
    **Example topics to try:**
    - "How robots help doctors"
    - "Why space exploration matters"
    - "The future of electric cars"
    - "How social media affects teenagers"
    """)

# Footer
st.markdown("---")
st.caption("🤖 This demo uses CrewAI with Groq's Llama model")