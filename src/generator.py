import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(retrieved_chunks, weights, query, show_sources=True):
    """
    Generate response using rank-weighted chunks from scientific paper sections
    
    Args:
        retrieved_chunks: List of dicts with 'text', 'section', 'section_start'
        weights: Array of weights for each chunk (based on relevance rank)
        query: User's question
        show_sources: Whether to include source sections in response
    """
    
    # Build weighted context with section information
    context_parts = []
    section_info = []
    
    for i, (chunk, weight) in enumerate(zip(retrieved_chunks, weights)):
        # Higher weight = more important, so we emphasize it
        importance = "PRIMARY" if i == 0 else "SECONDARY" if i < 3 else "SUPPORTING"
        
        context_parts.append(
            f"[{importance} CONTEXT - Relevance: {weight:.2%}]\n"
            f"Section: {chunk['section']}\n"
            f"Content: {chunk['text']}\n"
        )
        
        section_info.append({
            'section': chunk['section'],
            'relevance': weight,
            'rank': i + 1
        })

    context = "\n".join(context_parts)

    prompt = f"""
You are an expert research assistant analyzing a scientific paper. Use ONLY the provided context to answer the question.

IMPORTANT INSTRUCTIONS:
- Pay MORE attention to PRIMARY context (highest relevance) than SECONDARY or SUPPORTING context
- Cite the section names when providing information (e.g., "According to the Methods section...")
- Synthesize information across sections when relevant
- If the answer requires information from multiple sections, integrate them coherently
- Provide specific, factual answers based on the paper's content
- If the context doesn't contain enough information, state: "This information is not available in the provided sections of the paper."

CONTEXT FROM SCIENTIFIC PAPER:
{context}

QUESTION:
{query}

Provide a clear, well-structured answer with proper citations to paper sections.
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Using GPT-4 for better scientific reasoning
        messages=[
            {"role": "system", "content": "You are an expert research assistant helping analyze scientific papers with high factual accuracy."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,  # Lower temperature for more factual responses
        max_tokens=800
    )

    answer = response.choices[0].message.content
    
    # Optionally append source information
    if show_sources:
        sources = "\n\n---\n**Sources Used:**\n"
        seen_sections = set()
        for info in section_info[:3]:  # Show top 3 sources
            if info['section'] not in seen_sections:
                sources += f"- {info['section']} (Relevance: {info['relevance']:.1%})\n"
                seen_sections.add(info['section'])
        answer += sources
    
    return answer
