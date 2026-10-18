import os
import json
from typing import TypedDict, Any
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

st.set_page_config(page_title="AI Travel Planner", page_icon="🧭", layout="wide")
st.title("🧭 AI Travel Planner")
st.caption("Personalized day-wise itineraries with estimated budgets — verify prices and opening hours before travelling.")

class TravelState(TypedDict, total=False):
    destination: str
    start_date: str
    duration_days: int
    travelers: int
    budget: float
    interests: list[str]
    travel_style: str
    itinerary: str
    estimated_cost: float
    budget_status: str
    final_plan: str
    error: str

def model():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("Set GROQ_API_KEY in your environment before starting the app.")
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    return ChatGroq(model=model_name, temperature=0.2, max_retries=2)

def generate_plan(state: TravelState) -> dict:
    llm = model()
    prompt = f"""
Create a practical travel itinerary in plain Markdown.
Destination: {state['destination']}
Start date: {state['start_date'] or 'Not specified'}
Duration: {state['duration_days']} days
Travellers: {state['travelers']}
Total budget: INR {state['budget']:.0f}
Interests: {', '.join(state['interests'])}
Travel style: {state['travel_style']}

Requirements:
- Create a day-wise schedule with approximate times.
- Group nearby attractions on the same day where possible.
- Give a cost breakdown for the whole group: accommodation, food, local transport,
  activities/entry fees, and miscellaneous.
- State assumptions, including whether travel to/from the destination is included.
- Keep the estimated total at or below the budget if reasonably possible; if not,
  explain the shortfall and suggest specific savings.
- Do not claim prices, opening hours, or availability are live-verified.
- Mention that the user must verify local details before booking.
- Do not invent citations or claim to have checked websites.
"""
    response = llm.invoke([
        SystemMessage(content="You are a careful travel-planning assistant. Be transparent about uncertainty."),
        HumanMessage(content=prompt)
    ])
    plan = str(response.content)
    # Budget is estimated by the model in text; do not pretend to have exact structured cost data.
    return {"itinerary": plan, "final_plan": plan}

def build_graph():
    graph = StateGraph(TravelState)
    graph.add_node("generate_plan", generate_plan)
    graph.add_edge(START, "generate_plan")
    graph.add_edge("generate_plan", END)
    return graph.compile()

with st.sidebar:
    st.header("Trip details")
    destination = st.text_input("Destination", "Goa")
    start_date = st.date_input("Start date")
    duration = st.number_input("Duration (days)", min_value=1, max_value=30, value=4)
    travelers = st.number_input("Number of travellers", min_value=1, max_value=20, value=2)
    budget = st.number_input("Total budget (INR)", min_value=1, value=25000, step=1000)
    interests = st.multiselect(
        "Interests",
        ["Beaches", "Food", "Culture", "History", "Nature", "Adventure", "Shopping",
         "Nightlife", "Family activities", "Spiritual places"],
        default=["Beaches", "Food", "Nightlife"]
    )
    style = st.selectbox("Travel style", ["Relaxed", "Balanced", "Packed", "Luxury", "Budget"])

if st.button("Generate my itinerary", type="primary"):
    if not destination.strip():
        st.error("Please enter a destination.")
    elif not interests:
        st.error("Choose at least one interest.")
    else:
        initial: TravelState = {
            "destination": destination.strip(),
            "start_date": str(start_date),
            "duration_days": int(duration),
            "travelers": int(travelers),
            "budget": float(budget),
            "interests": interests,
            "travel_style": style,
        }
        try:
            with st.spinner("Building your travel plan..."):
                result = build_graph().invoke(initial)
            st.markdown(result["final_plan"])
            st.download_button(
                "Download itinerary as Markdown",
                data=result["final_plan"],
                file_name="travel_itinerary.md",
                mime="text/markdown"
            )
        except Exception as exc:
            st.error(f"Could not generate the itinerary: {exc}")
            st.info("Check your GROQ_API_KEY, model availability, internet connection, and installed package versions.")
