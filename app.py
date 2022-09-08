
import pandas as pd
import streamlit as st
from pyecharts.charts import *
from pyecharts.components import Table
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from streamlit_echarts import st_pyecharts
import datetime

st.set_page_config(page_title='Dashboard',page_icon=':notebook:',layout='wide')

st.title(':mortar_board: 玩数圈App')
st.markdown('---')

df=pd.read_excel(r'userPyOut.xlsx')


st.sidebar.header('请在此处进行筛选: ')
month = st.sidebar.multiselect(
    "请选择要查看的月份:",
    options=df['Month'].unique(),
    default=df['Month'].unique())

df_selection=df.query(
    "Month == @month "
)

if st.checkbox('查看数据'):
    st.dataframe(df_selection)

st.title(':1234: KPIs')
st.markdown('###')  

total = df_selection['用户id'].count()
st.subheader('总人数:')
st.subheader(f'{total} :mens: :womens:')

st.markdown('---')

tab1,tab2,tab3 = st.tabs(['柱状图','折线图','日历'])

with tab1:
    def render_bar_py():
        st.title(":bar_chart: Hello Bar Charts !")
        grouped_by_hours = df_selection.groupby(by=['Date']).count()[['用户id']]
        ##with st.echo("below"):
        a = (
            Bar(init_opts=opts.InitOpts(theme= 'westeros'))
            .add_xaxis(grouped_by_hours.index.to_list())
            .add_yaxis("注册人数",grouped_by_hours['用户id'].to_list())
            .set_global_opts(
                    title_opts=opts.TitleOpts(title='',pos_left='center'),
                    datazoom_opts=[opts.DataZoomOpts()])
            )
            ##st.dataframe(df)
        return a
    st_pyecharts(render_bar_py())

with tab2:
    def render_line_py():
        st.title(":chart_with_upwards_trend: Hello Line Charts !")
        grouped_by_hours = df_selection.groupby(by=['Date']).count()[['用户id']]
        ##with st.echo("below"):
        b = (
            Line(init_opts=opts.InitOpts(theme= 'westeros'))
            .add_xaxis(grouped_by_hours.index.to_list())
            .add_yaxis("",grouped_by_hours['用户id'].to_list())
            .set_global_opts(
                    title_opts=opts.TitleOpts(title='注册人数',pos_left='center'),
                    datazoom_opts=[opts.DataZoomOpts(type_='inside')])
        )
        return b
    st_pyecharts(render_line_py())

with tab3:
    def render_calendar_py():
        st.title(":calendar: Hello Canlendar !")
        grouped_by_date = df_selection.groupby(by=['Date']).count()[['用户id']]
        grouped_by_date=grouped_by_date.reset_index()
        data=grouped_by_date[['Date','用户id']].values.tolist()
        max_count=grouped_by_date['用户id'].max()
        min_count=grouped_by_date['用户id'].min()
        ##with st.echo("below"):
        c = (
            Calendar(init_opts=opts.InitOpts(theme= 'westeros'))
            .add('', data,calendar_opts=opts.CalendarOpts(range_='2022'))
            .set_global_opts(
                title_opts=opts.TitleOpts(title='不同日期注册人数',pos_left='center'),
                legend_opts=opts.LegendOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(
                    max_=max_count,
                    min_=min_count,
                    orient='horizontal',
                    is_piecewise=False,
                    pos_top='230px',
                    pos_left='50px',
                )
            )
        )
        return c
    st_pyecharts(render_calendar_py())

hide_at_style= """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
    """
st.markdown(hide_at_style,unsafe_allow_html=True)
