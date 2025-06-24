import google.generativeai as genai

genai.configure(api_key="AI-your-full-key-here")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Say hello")
print(response.text)
