import streamlit as st
import json
import requests

st.title('Auto Code Summarization Generator')
if not 'has_generated' in st.session_state:
    st.session_state['has_generated'] = False
if not 'code_summary' in st.session_state:
    st.session_state['code_summary'] = ""

# choose your language
language = st.selectbox('What language would you like to use?', ('Python','Java','C++'))

# taking user inputs
kind  = st.selectbox('what kind of code summary would you like to generate?',
                       ('What','Why','How-it-is-done','Property'))

# input code


code = st.text_area('Please input your function code to generate code summary', height=50)
st.markdown("```\n" + code, unsafe_allow_html=True)

generate_inputs = {'code':code, 'prompt':"\n // code summary:  ", 'language':language, 'kind':kind}

# when the user clicks the 'Generate' button
if st.button('Generate'):
    st.session_state['has_generated'] = True
    res = requests.post(url = 'http://127.0.0.1:8000/generate', data = json.dumps(generate_inputs))
    st.session_state['code_summary'] = res.text
       
if st.session_state['has_generated']:
    # 获取字符串
    code_summary = st.session_state['code_summary']

    # 将换行符替换为HTML的<br>标记
    code_summary = code_summary.replace('\\n', '\n')
    st.write('<span style="font-size: 18px;">Code Summary</span>', unsafe_allow_html=True)
    # 将字符串放在引用框中，并使用HTML标记
    st.markdown(f"```\n{code_summary}", unsafe_allow_html=True)
    
    rating = st.slider('How would you rate this summary?', 1, 5, 3) 
    # send the rating to the backend
    rating_inputs = {'code':code, 'summary':st.session_state['code_summary'], 'rating':rating}
    if st.button('Send Rating'):
        res = requests.post(url = 'http://127.0.0.1:8000/ratings', data = json.dumps(rating_inputs))
