from dotenv import load_dotenv
import os
import streamlit as st
from pydantic import BaseModel
from openai import OpenAI


# Load environment variables from a local .env file (if present).
# Example .env:
# OPENAI_API_KEY=your_openai_api_key_here
# OPENAI_MODEL=gpt-5.6-luna
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

if not OPENAI_API_KEY:
    st.error(
        "OPENAI_API_KEY is not set. Add it to your environment or .env file, "
        "then restart the Streamlit app."
    )
    st.stop()

# Standard OpenAI client — no Azure endpoint, deployment name, or API version needed.
client = OpenAI(api_key=OPENAI_API_KEY)


class AgentResponse(BaseModel):
    sense: str
    plan: str
    act: str
    reflection: str
    final_answer: str


def call_openai(prompt: str) -> str:
    """Call the OpenAI Responses API and return plain text output."""
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text.strip()


def calculator_tool(expression: str) -> str:
    """Evaluate simple arithmetic expressions such as '5*7+2'."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


st.title("🤖 Agentic AI Workflow Demo")
st.write(
    """
### Includes:
- AI Agents
- Sense → Plan → Act → Reflect workflow
- Calculator tool for arithmetic expressions
- Direct OpenAI API (no Azure OpenAI credentials)
"""
)

st.caption(f"Model: {OPENAI_MODEL}")

user_input = st.text_input("Enter your question or task:")


if user_input:
    try:
        # 1. SENSE: Understand the user's request.
        sense_prompt = f"""
You are the Sense stage of an agentic AI workflow.
Understand the user's request and summarize the intent, important details,
and constraints in 2-4 concise sentences.

User query: {user_input}
"""
        sense = call_openai(sense_prompt)

        # 2. PLAN: Decide what should happen next.
        plan_prompt = f"""
You are the Plan stage of an agentic AI workflow.
Based on the understanding below, create a short practical plan for answering
or completing the user's request. Do not execute the plan yet.

Understanding:
{sense}
"""
        plan = call_openai(plan_prompt)

        # 3. ACT: Use the calculator tool for arithmetic; otherwise use the LLM.
        if any(op in user_input for op in ["+", "-", "*", "/", "**"]):
            calc_result = calculator_tool(user_input)
            act = f"Used calculator_tool('{user_input}') → {calc_result}"
            final_answer = calc_result
        else:
            act_prompt = f"""
You are the Act stage of an agentic AI workflow.
Answer the user's question directly and concisely.
Use the following understanding and plan as context.

User query: {user_input}

Understanding:
{sense}

Plan:
{plan}
"""
            final_answer = call_openai(act_prompt)
            act = "Generated the answer using the OpenAI model."

        # 4. REFLECT: Check the result for quality.
        reflection_prompt = f"""
You are the Reflection stage of an agentic AI workflow.
Review the proposed answer against the original user query.
Briefly state whether it is correct, relevant, and complete, and mention any
important limitation. Do not rewrite the full answer unless necessary.

User query: {user_input}

Proposed answer:
{final_answer}
"""
        reflection = call_openai(reflection_prompt)

        structured = AgentResponse(
            sense=sense,
            plan=plan,
            act=act,
            reflection=reflection,
            final_answer=final_answer,
        )

        st.subheader("🧠 Sense (Understand)")
        st.write(structured.sense)

        st.subheader("🧩 Plan (Decide Next Actions)")
        st.write(structured.plan)

        st.subheader("⚙️ Act (Reason / Use Tool)")
        st.write(structured.act)

        st.subheader("💭 Reflection (Self-Evaluation)")
        st.write(structured.reflection)

        st.subheader("✅ Final Answer")
        st.success(structured.final_answer)

    except Exception as e:
        st.error(f"OpenAI API call failed: {e}")
