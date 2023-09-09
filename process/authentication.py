# Importing required libraries
import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

def login_form():
    # Placeholder for streamlit content
    place_holder = st.empty()
    
    # Loading config from pages/static/config.yaml
    with open('.streamlit/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Creating the authenticator object
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # Selectbox for login options
    login_out = st.selectbox("ورود به برنامه", ("ورود", "ثبت نام", "بازیابی رمز"))

    if login_out == "ورود":
        with st.container():
            # creating a login widget
            name, authentication_status, username = authenticator.login('Login', 'main')
            if authentication_status:
                authenticator.logout('Logout', 'main', key='unique_key')
                st.write(f'خوش آمدی *{name}*')
                st.session_state["name"] = name
                st.session_state["authentication_status"] = authentication_status
                st.session_state["username"] = username


                with open('.streamlit/config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.title("صحت اپلیکیشن کمک یار ورزش")
            elif authentication_status is False:
                st.error('رمز ورود / نام کاربری اشتباه است')
            elif authentication_status is None:
                st.warning('نام کاربری و رمز عبور خود را وارد کنید')

    elif login_out == "ثبت نام":
        with st.container():
            # Creating a new user registration widget
            try:
                if authenticator.register_user('Register user', preauthorization=False):
                    st.success('ثبت نام موفقیت آمیز بود')
                    with open('.streamlit/config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                st.error(e)

    elif login_out == "بازیابی رمز":
        try:
            username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('بازیابی رمز عبور')
            if username_forgot_pw:
                st.success("رمز عبور با موفقیت تغییر کرد")
                st.write(random_password)
                config['random_password'] = random_password
                with open('.streamlit/config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            else:
                st.error('نام کاربری یافت نشد')
        except Exception as e:
            st.error(e)


if __name__ == "__main__":
    login_form()
