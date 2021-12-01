import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

markdown_text = '''
The gender wage gap is simply the difference in income earnings between males and females. Men consistently earn more than women, and the difference is even more apparent in women of color. [American Progress](https://americanprogress.org/article/quick-facts-gender-wage-gap/) displayed a simple bar plot showing this gap with data from the 2018 census. The bar plot shows for every 1 dollar a white male makes, a white female makes 0.79 dollars, a black female makes 0.62 dollars, a hispanic or latino female makes 0.54 dollars, an Asian female makes 0.9 dollars, and an American Indian makes 0.57 dollars. [Pew Research](https://www.pewresearch.org/fact-tank/2021/05/25/gender-pay-gap-facts/) states, in 2020, it would have take approximately 42 additional days of work for women to earn as much as men.

The General Social Survey (GSS) has been collecting sociological data since 1972. The [National Science Foundation] (https://www.nsf.gov/pubs/2007/nsf0748/nsf0748_3.pdf) (NSF) mentioned that the GSS survey measures social changes in our communities, trends, attitudes, behaviors and attributes of the adult population. The GSS data is collected by randomly selecting individuals in households to complete the survey. 
'''

gss_display = gss_clean.groupby('sex').agg({'income':'mean',
                                            'job_prestige':'mean',
                                            'socioeconomic_index' : 'mean',
                                            'education' : 'mean'})
gss_display =gss_display.rename({'income':'Income',
                                   'job_prestige':'Occupational Prestige',
                                   'socioeconomic_index':'Socioeconomic Index',
                                   'education':'Yeas of Education'}, axis=1)
gss_display = round(gss_display, 2)
gss_display = gss_display.reset_index().rename({'sex':'Sex'}, axis=1)
table = ff.create_table(gss_display)
table.show()

gss_bar = gss_clean[['male_breadwinner','sex']].value_counts().reset_index()
gss_bar = gss_bar.rename({'sex':'male_female'})
gss_bar = gss_bar.rename({0:'count'},axis=1)
gss_bar
fig_bar = px.bar(gss_bar,
       x='male_breadwinner',
       y='count',
       color='sex',
       labels={'sex' : 'Sex','male_breadwinner' : 'Should Everyone Involve','count' : 'Number of People Responded'},
       hover_data = ['sex','male_breadwinner','count'],
       text = 'count',
       barmode='group')
fig_bar.show()

fig = px.scatter(gss_clean.head(200), x='job_prestige', y='income', color = 'sex', 
                 height=600, width=600, trendline = 'ols',
                 labels={'job_presige':'Job Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig.update(layout=dict(title=dict(x=0.5)))
fig.show()

fig = px.box(gss_clean, x='income', color = 'sex',
                   labels={'income':'Income'})
fig.update(layout=dict(title=dict(x=0.5)))
fig.update_layout(showlegend=False)


fig.show()

fig = px.box(gss_clean, x='job_prestige', color = 'sex',
                   labels={'job_prestige':'Prestige', 'sex':''})
fig.update(layout=dict(title=dict(x=0.5)))
fig.update_layout(showlegend=False)
fig.show()

gss_clean_new = gss_clean[['income','sex','job_prestige']].dropna()

gss_new = gss_clean[['income','sex','job_prestige']]
gss_new['job_prestige_cats'] = pd.cut(gss_clean.job_prestige,bins=6)
gss_new = gss_new.dropna()
gss_new
fig_box_job_cat = px.box(gss_new, x='income', y = 'sex', color = 'sex',
             facet_col='job_prestige_cats', facet_col_wrap=2,
             color_discrete_map = {'male':'blue', 'female':'pink'},
             title = 'Distribution of Job Prestige')
fig_box_job_cat.update(layout=dict(title=dict(x=0.5)))
fig_box_job_cat.show()
