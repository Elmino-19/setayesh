import streamlit as st
from streamlit_lottie import st_lottie
import json
import pandas as pd
import os

if os.path.exists("upload.csv"):
    os.remove("upload.csv")



def main():
    
    st.markdown("""<style>body {direction: ltr !important;}</style>""", unsafe_allow_html=True)

    def get(path: str):
        with open(path, "r") as p:
            return json.load(p)
    lot_sehat = get("static/sehat_lottie.json")

    page_title = "مقدار زوایای مورد نظر را برای هر مفصل انتخاب کنید "
    page_icon = "📝" 
    layout = "centered"

    st.title(page_title + " " + page_icon)

    lot = st_lottie(animation_source=lot_sehat,
                    speed=.5,
                    reverse=False,
                    loop=True,
                    quality="low",
                    height=225,
                    width=400,
                    key="lot_t")

    name_dict = {
    'آرنج راست': 'right_elbow',
    'آرنج چپ': 'left_elbow',
    'شانه راست': 'right_shoulder',
    'شانه چپ': 'left_shoulder',
    'سمت چپ کمر': 'right_hip',
    'سمت راست کمر': 'left_hip',
    'زانو راست': 'right_knee',
    'زانو چپ': 'left_knee',
    'مچ پای راست': 'right_ankle',
    'مچ پای چپ': 'left_ankle'}

    values = {}
    lst = []

    for name in name_dict.keys():
        lst.append(name)
    options = st.multiselect('مفاصل',lst)

    for option in options:
        value = st.slider(option, 0, 180, (50, 100))
        values[option] = value
    df = pd.DataFrame(values)
    with st.form("entry_form", clear_on_submit=True):
        with st.expander("راهنما"):
            st.text("""باتوجه به ورزش مورد نظر خود بازه زوایا را مشخص کنید""")
        submitted = st.form_submit_button("ذخیره داده‌ها")
        df_rename = df.rename(columns={col: name_dict[col] for col in df.columns if col in name_dict.keys()})
        for joint in name_dict.values():
            if joint not in df_rename.columns:
                df_rename[joint] = 0
        if submitted:
            df_rename.to_csv("upload.csv", index=False)
            st.write(df)

if __name__ == "__main__":
    main()