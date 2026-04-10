from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3

import pandas as pd
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        return f"Error: {e}"
    

prompt = ["""
You are an expert in converting English questions to SQL query.

Database:
Table: STUDENTS
Columns: NAME, CLASS, AGE

Rules:
- Only return SQL query
- No explanation
- No markdown
- No ``` or text
- Output must be executable SQL only

Examples:

Q: How many records are present?
A: SELECT COUNT(*) FROM STUDENTS;

Q: Show students in 9th class
A: SELECT * FROM STUDENTS WHERE CLASS = '9th';
"""]


st.set_page_config(page_title="I can retrieve SQL queries")
st.header("Gemini Pro to retrieve SQL queries")

question=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

if submit:
    sql_query = get_gemini_response(question, prompt)

    st.subheader("Generated SQL Query:")
    st.code(sql_query, language="sql")

    db_path = r"D:\GenAI\Gemini Pro Project\studentdb.db"
    response = read_sql_query(sql_query, db_path)
    st.write("Using DB path:", db_path)

    st.subheader("Query Result:")
    if isinstance(response, str):
        st.error(response)
    else:
        df = pd.DataFrame(response, columns=["NAME", "CLASS", "AGE"])
        st.dataframe(df)


