import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(context_chunks, query):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful assistant reading a document. Use ONLY the context below to answer the question.

Context:
{context}

Question:
{query}

Respond with bullet points, paragraphs, or tables. If the answer is not in the context, say:
"This information is not available in the document."
"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content
