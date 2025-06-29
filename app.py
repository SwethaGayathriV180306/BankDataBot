import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

st.set_page_config(page_title="BankDataBot", layout="centered")
st.title("🏦 BankDataBot ")

num_records = st.slider("Number of records to generate:", 5, 50, 10)

if st.button("Generate Synthetic Data"):
    with st.spinner("Contacting Gemini..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            Generate {num_records} fake Indian banking customer records in markdown table format.
            Each record should have: Name, Age, Account Type (Savings or Current), Balance (₹),
            Transaction Type (Debit/Credit), Amount (₹), Date (YYYY-MM-DD), and City (India).
            """
            response = model.generate_content(prompt)
            output = response.text
            st.markdown("### 🔍 Generated Markdown Table")
            st.markdown(output)
            table_lines = [line for line in output.split("\n") if line.startswith("|")]
            if len(table_lines) >= 3:
                headers = [h.strip() for h in table_lines[0].split("|")[1:-1]]
                data = []
                for row in table_lines[2:]:
                    cells = [c.strip() for c in row.split("|")[1:-1]]
                    data.append(cells)
                df = pd.DataFrame(data, columns=headers)
                st.success("✅ Parsed table successfully.")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", data=csv, file_name="synthetic_bankdata.csv")
            else:
                st.warning("⚠️ Gemini response didn’t include a proper table.")
        except Exception as e:
            st.error(f"❌ Gemini API Error: {e}")
