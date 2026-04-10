# ================================
# PROFIT & LOSS MULTI-QUESTION SOLVER
# (Robust JSON handling)
# ================================

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import json
import re

load_dotenv()

# ----------------
# LLM (OpenRouter)
# ----------------
llm = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")
# ----------------
# Read PDF
# ----------------
def read_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    return " ".join(p.page_content for p in pages)

# ----------------
# Split Questions
def split_questions(text):
    # Split strictly on Q.<number>/5 markers
    chunks = re.split(r'(?i)(?=Q\.\d+/5)', text)

    questions = []
    for chunk in chunks:
        chunk = chunk.strip()

        # Ignore headers and empty chunks
        if chunk.startswith("Q.") and "Step wise textual explanation" in chunk:
            questions.append(chunk)

    return questions

# ----------------
# Extract JSON safely
# ----------------
def extract_json(text):
    # remove code fences
    text = re.sub(r"```.*?```", lambda m: m.group(0)[3:-3], text, flags=re.S)
    
    # find first JSON block
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found in model output")
    
    return json.loads(match.group())

# ----------------
# Prompt
# ----------------
prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are an aptitude mathematics expert. You have to read the solution starting with the word 'Sol:'
this will be given for example 'Q. An article has a marked price of ₹ 2240. 
It is sold at a discount of 20 % on the marked price, but the seller still makes a profit of 
12 %. Find the cost price. 
 
Sol: SP = 2240 × 0.80 = 1792 
 
Profit = 12 % → SP = 1.12 × CP 
CP = 1792/1.12 = 1600 
 
Answer → Cost Price = ₹ 1600' You need to extract the value from the 'Sol:' that will get fit in Visual diagram. 

2. An attempt to map the question's numbers to a specific Visual Diagram that requires 3 parameters:
   - Markup_Percent (e.g. 40)
   - Discount_Percent (e.g. 10)
   - Profit_Amount (e.g. 36)
   (Do your best to map the problem into these 3 variables, even if it requires creative interpretation, because the visual diagram MUST be rendered).

Return ONLY valid JSON (no explanation, no markdown).

{{
  "Textual_Solution": [
    "Sol: Let the cost price = ₹ x",
    "1. Marked Price = 1.40 x",
    "2. After 10 % discount -> Selling Price = 1.40x X 0.90 = 1.26x",
    "3. Profit = SP - CP = 1.26x - x = 0.26x",
    "Given profit = ₹ 36",
    "0.26x = 36",
    "=> x = 36/0.26 ≈ 138.46",
    "Answer -> Cost Price ≈ ₹ 138.46"
  ],
  "Visual_Variables": {{
    "Markup_Percent": 40,
    "Discount_Percent": 10,
    "Profit_Amount": 36
  }}
}}

Question:
{question}
"""
)

chain = prompt | llm

# ----------------
# Run for ALL questions
# ----------------
def extract_all_profit_loss(pdf_path):
    text = read_pdf(pdf_path)
    questions = split_questions(text)
    results = []

    for i, q in enumerate(questions, start=1):
        response = chain.invoke({"question": q})
        try:
            solution = extract_json(response.content)
        except Exception as e:
            solution = {
                "error": "Failed to parse JSON",
                "raw_output": response.content
            }

        results.append({
            "Question_No": i,
            "Question_Text": q,
            "Solution": solution
        })

    return results


if __name__ == "__main__":
    output = extract_all_profit_loss("input.pdf")

    for item in output:
        print(f"\n📘 Question {item['Question_No']}")
        print(json.dumps(item["Solution"], indent=2))
