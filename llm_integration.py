import google.generativeai as genai
import streamlit as st

class CineFusionLLM:
    def __init__(self, model_name="gemini-2.5-flash", temperature=0.7, api_key=None):
        if api_key:
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": temperature,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )

    def generate(self, query, context_list):
        if not context_list:
            return "I don't have enough information from the database."
        
        context = "\n\n".join(context_list)
        prompt = f"""You are CineFusion AI, a movie recommendation expert.

Use ONLY the following movie context:
{context}

User question:
{query}

Rules:
- Answer clearly.
- Do not hallucinate.
- If context is insufficient, say:
  "I don't have enough information from the database."
"""
        response = self.model.generate_content(prompt)
        return response.text

    def select_best_movies(self, query, movie_descriptions):
        prompt = f"""
User query:
{query}

Candidate movies:
{movie_descriptions}

Task:
- Select the BEST 6 movies.
- Return ONLY movie titles as a numbered list.
"""
        response = self.model.generate_content(prompt)
        return response.text

    def explain_recommendations(self, query, movies_text):
        prompt = f"""
User query:
{query}

Recommended movies:
{movies_text}

Explain why EACH movie is recommended.
Use bullet points.
Limit 1–2 lines per movie.
"""
        response = self.model.generate_content(prompt)
        return response.text
