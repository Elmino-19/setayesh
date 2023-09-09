import os
import streamlit as st
import math
import streamlit.components.v1 as components
IS_RELEASE = True


PINNED_NAV_STYLE = """
                    <style>
                    .reportview-container .sidebar-content {
                        padding-top: 0rem;
                    }
                    .reportview-container .main .block-container {
                        padding-top: 1rem;
                        padding-right: 1rem;
                        padding-left: 1rem;
                        padding-bottom: 0rem;
                    }
                    </style>
                """

STICKY_NAV_STYLE = """
                    <style>
                    div[data-stale="false"] > iframe[title="sehat_components.NavBar.nav_bar"] {
                        position: fixed;
                        width: 100%;
                        z-index: 99;
                        box-sizing: border-box;
                        top: 0;
                    }
                    </style>
                """

HIDE_ST_STYLE = """
                <style>
div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
				.appview-container .main .block-container{
                padding-top: 0rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 0rem;
                        }  
                        .appview-container .sidebar-content {
                            padding-top: 0rem;
                        }
                        .reportview-container {
                            padding-top: 0rem;
                            padding-right: 3rem;
                            padding-left: 3rem;
                            padding-bottom: 0rem;
                        }
                        .reportview-container .sidebar-content {
                            padding-top: 0rem;
                        }
                        header[data-testid="stHeader"] {
                            z-index: -1;
                        }
                        div[data-testid="stToolbar"] {
                        z-index: 100;
                        }
                        div[data-testid="stDecoration"] {
                        z-index: 100;
                        }
                        .reportview-container .sidebar-content {
                            padding-top: 0rem;
                        }
                        div[data-stale="false"] > iframe[title="sehat_components.NavBar.nav_bar"] {
                        z-index: 99;
                    }
                </style>
                """

if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("nav_bar", path=build_path)
else:
    _component_func = components.declare_component("nav_bar", url="http://localhost:3000")


def nav_bar(menu_definition, first_select=0, key=None,home_name=None,login_name=None,override_theme=None, sticky_nav=True,force_value=None,use_animation=True,hide_streamlit_markers=True,sticky_mode='pinned', option_menu=False):
    """
    first_select: int (پیش‌فرض 0)
        اولین ورودی انتخاب شده زمانی که نوار ناوبری ایجاد می شود، از یک مرجع 2 رقمی استفاده می کند، 10 اولین ورودی است، بنابراین ورودی دوم در مورد سوم یک زیر منو 32 است.
    کلید:
        یک کلید یا نام منحصر به فرد برای این مؤلفه
    home_name:
        یک ورودی خاص برای اولین یا خانه ورود، در صورت عدم استفاده از بسته صحت، لازم نیست
    override_theme: dict
        طرح زمینه Streamlit اعمال شده در نوار ناوبری را لغو کنید
        {'txc_inactive': 'سفید', 'menu_background':'بنفش','txc_active':'زرد','option_active':'آبی'}

    sticky_nav: bool (پیش‌فرض True)
        نوار ناوبری باید به بالای پنجره چسبیده باشد یا خیر
    use_animation: bool (پیش‌فرض True)
        از انیمیشن برای انتقال آیتم های ناوبری یا استاتیک استفاده کنید
    hide_streamlit_markers: bool (پیش‌فرض True)
        منوی همبرگر ساده و برچسب پاورقی را پنهان کنید
    sticky_mode: str (پیش‌فرض «پین شده»)
        حالت چسبنده، اگر به طور دائم در هنگام چرخاندن به بالا چسبیده باشد یا خیر

    برمی گرداند
    """

    first_select = math.floor(first_select/10)

    if type(home_name) is str:
        home_data = {'id': home_name, 'label': home_name, 'icon': "fa fa-home", 'ttip': home_name}
    else:
        home_data = home_name


    if type(login_name) is str:
        login_data = {'id': login_name, 'login_datalabel': login_name, 'icon': "fa fa-user-circle", 'ttip': login_name}
    else:
        login_data = login_name

    
    if option_menu:
        max_len = 0
        for mitem in menu_definition:
            label_len = len(mitem.get('label',''))
            if label_len > max_len:
                max_len = label_len

        for i, mitem in enumerate(menu_definition):
            menu_definition[i]['label'] = f"{mitem.get('label',''):^{max_len+10}}"
    

    component_value = _component_func(menu_definition=menu_definition, first_select=first_select,key=key,home=home_data,fvalue=force_value,login=login_data,override_theme=override_theme,use_animation=use_animation)

    if sticky_nav:
        if sticky_mode == 'pinned':
            st.markdown(PINNED_NAV_STYLE,unsafe_allow_html=True)
        else:
            st.markdown(STICKY_NAV_STYLE,unsafe_allow_html=True)

    if hide_streamlit_markers:
        st.markdown(HIDE_ST_STYLE,unsafe_allow_html=True)


    if component_value is None:
        if first_select > len(menu_definition):
            if login_name is not None:
                return login_name
            else:
                menu_item = menu_definition[-1]

        elif home_name is None:
            menu_item = menu_definition[first_select]

        else:
            if first_select == 0:
                return home_data.get('id')
            else:
                menu_item = menu_definition[(first_select-1)]

        if 'id' in menu_item:
            return menu_item.get('id')
        else:
            return menu_item.get('label')
    else:
        return component_value

