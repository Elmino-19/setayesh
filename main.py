# به منظور اجرای برنامه Streamlit، شما باید ابتدا کتابخانه‌های مورد نیاز را نصب کنید. برای این کار، می‌توانید از فایل requirements.txt استفاده کنید. در ترمینال، به مسیر پروژه خود بروید و دستور زیر را وارد کنید:
#pip install -r requirements.txt
# این دستور، تمام کتابخانه‌های مورد نیاز را بر اساس فایل requirements.txt نصب خواهد کرد.
#
# سپس، برای اجرای برنامه، باید دستور زیر را در ترمینال وارد کنید:
#
#  streamlit run main.py
#
#در نهایت برنامه بر روی مرورگر شما قابل اجرا است

# Importing required libraries
import yaml
import streamlit as st

from NavBar import nav_bar
from process.authentication import login_form

import json


def main():
    # Placeholder for streamlit content

    with open('static/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    def get(path: str):
        with open(path, "r") as p:
            return json.load(p)

    # Loading config from .streamlit/config.yaml
    with open('.streamlit/config.yaml') as file:
        config = yaml.safe_load(file)

    # Creating the authenticator object
        menu_data = [
            {'icon': "fas fa-file-upload", 'label':"بارگذاری ویدیو"},
            {'icon': "fas fa-camera", 'label':"بررسی صحت حرکت"},
            {'icon': "fas fa-list", 'label':"تنظیم زوایا "}
        ]
        over_theme = {'txc_inactive': '#FFFFFF'}
        menu_id = nav_bar(
            menu_definition=menu_data,
            override_theme=over_theme,
            home_name='صفحه اصلی',
            login_name='ورود/خروج',
            hide_streamlit_markers=True,
            sticky_nav=False,
            sticky_mode='pinned',
        )
    # Authentication
    # place_holder = st.empty()
    with st.sidebar:
        login_form()

    # NavBar and Content
    if st.session_state['authentication_status']:
        place_holder1 = st.empty()

        if menu_id == 'ورود/خروج':
            with place_holder1.container():
                # کاربر خارج می‌شود، تنظیم authentication_status به False
                st.session_state['authentication_status'] = False
        elif menu_id == 'صفحه اصلی':
            with place_holder1.container():
                from process.main_page import main
                main()
        elif menu_id == "بارگذاری ویدیو":
            with place_holder1.container():
                from process.upload_video import main
                main()
        elif menu_id == "تنظیم زوایا ":
            with place_holder1.container():
                from process.input_joints import main
                main()
        elif menu_id == "بررسی صحت حرکت":
            with place_holder1.container():
                from process.camera import main
                main()

if __name__ == "__main__":
    main()
