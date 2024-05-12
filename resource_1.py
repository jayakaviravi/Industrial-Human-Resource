import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")
from wordcloud import WordCloud
import io
import streamlit as st
from streamlit_option_menu import option_menu
pd.set_option('display.max_columns', None)


# setting page configuration
st.set_page_config(page_title="Industrial Human Resource", 
                    layout="wide",
                    initial_sidebar_state="auto") 

# page header transparent color
page_background_color = """
<style>

[data-testid="stHeader"] 
{
background: rgba(0,0,0,0);
}

</style>
"""
st.markdown(page_background_color, unsafe_allow_html=True)

# title and position
st.markdown(f'<h1 style="text-align: center; color:salmon">Industrial Human Resource Geo-Visualization</h1>',unsafe_allow_html=True)

# Add colored divider
st.markdown(
    """<div style="height: 2px; background-color:teal; margin: 20px 0;"></div>""",
    unsafe_allow_html=True)

def dataframe():
    df_1=pd.read_csv('C:/Users/JAYAKAVI/New folder/re_file.csv')
    return df_1
df=dataframe()

# CREATING OPTION MENU
selected = option_menu(None,  ["Home", "Data Visualization", "Insights"],
                       icons=["house", "bar-chart","Magnifying Glass"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "-3px",
                                            "--hover-color": "#545454"},
                               "icon": {"font-size": "20px"},
                               "container": {"max-width": "3000px"},
                               "nav-link-selected": {"background-color": "violet"}})

if selected=='Home':

    st.subheader(":green[Technologies]")

    st.markdown('####  EDA, Visualization, NLP')

    st.subheader(':green[Overview]')

    st.markdown('#### This study aims to provide updated insights into the industrial classification of main and marginal workers in India, excluding cultivators and agricultural laborers. By analyzing data on workforce distribution by gender and across different sections, divisions, and classes, the study aims to offer policymakers accurate information for effective decision-making in employment planning and policy formulation.')

if selected=='Data Visualization':
    
    with st.sidebar:
        select = option_menu(None, ['Gender','Groups','Class','Division','Districts','Industries'], 
                            default_index=0,
                            orientation="horizontal",
                            styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "0px", 
                                                    "--hover-color": "white"},
                                    "icon": {"font-size": "15px"},
                                    "container" : {"max-width": "3000px"},
                                    "nav-link-selected": {"background-color": "violet"}})
    
    
    if select=='Gender':

        # Top 10 States: Distribution of Workers by Gender
        
        df['Total Workers - Males'] = df['Main Workers - Total - Males'] + df['Marginal Workers - Total - Males']
        df['Total Workers - Females'] = df['Main Workers - Total - Females'] + df['Marginal Workers - Total - Females']
        df['Total Workers'] = df['Total Workers - Males'] + df['Total Workers - Females']

        # Group the data by state and calculate the total number of workers
        state_workers = df.groupby('India/States').sum().reset_index()

        # Sort the data by the total number of workers in descending order and select the top 10 states
        top_10_states = state_workers.sort_values(by='Total Workers', ascending=False).head(10)
        custom_colors = ['brown','#1f77b4']

        # Create a stacked bar chart for the top 10 states
        fig_1 = px.bar(top_10_states, x='India/States',
                                        y=['Total Workers - Males', 'Total Workers - Females'],color_discrete_sequence=custom_colors,
                                        title='Top 10 States: Distribution of Workers by Gender',pattern_shape_sequence = ['.'],
                                        barmode='stack')
        fig_1.update_layout( height=450,width=900,title_font_color='orange',title_font=dict(size=20),title_x=0.2)
        st.plotly_chart(fig_1)

        # Distribution of Main Workers by Gender
        
        main_workers_columns = ['Main Workers - Total - Males', 'Main Workers - Total - Females',
                        'Main Workers - Rural - Males', 'Main Workers - Rural - Females',
                        'Main Workers - Urban - Males', 'Main Workers - Urban - Females']


        main_workers_sum = df[main_workers_columns].sum()

        fig_2 = px.pie(names=main_workers_sum.index, values=main_workers_sum.values,hole=0.5,
                                title='Distribution of Main Workers by Gender')
        fig_2.update_traces(textposition='outside', textinfo='percent')
        fig_2.update_layout( height=450,width=800,title_font_color='orange',title_font=dict(size=20),title_x=0.2)
        st.plotly_chart(fig_2)

        # Distribution of Marginal Workers by Gender
        marginal_workers_columns = ['Marginal Workers - Total - Males', 'Marginal Workers - Total - Females',
                             'Marginal Workers - Rural - Males', 'Marginal Workers - Rural - Females',
                             'Marginal Workers - Urban - Males', 'Marginal Workers - Urban - Females']

        marginal_workers_sum = df[marginal_workers_columns].sum()
        gender_labels = ['Total Males', 'Total Females', 'Rural Males', 'Rural Females', 'Urban Males', 'Urban Females']
        marginal_workers_df = pd.DataFrame({'Gender': gender_labels, 'Count': marginal_workers_sum.values})
        fig_3 = px.bar(marginal_workers_df, x='Gender', y='Count', 
                    title='Distribution of Marginal Workers by Gender',
                    barmode='group', labels={'Count': 'Count of Marginal Workers'})
        fig_3.update_traces(textfont_size=12,marker_color=px.colors.diverging.Spectral)
        fig_3.update_layout( height=500,width=600,title_font_color='orange',title_font=dict(size=20),title_x=0.2)
        st.plotly_chart(fig_3)

    if select=='Groups':

        # Distribution of Total Main Workers for Top 10 Groups
        
        total_workers_by_state = df.groupby('Group')['Main Workers - Total -  Persons'].sum().reset_index()
        top_10_group =total_workers_by_state .sort_values(by='Main Workers - Total -  Persons', ascending=False).head(10)
        df_top_10_groups = df[df['Group'].isin(top_10_group['Group'])]
        fig_4= px.bar(top_10_group, y='Main Workers - Total -  Persons', x='Group',
                                        color='Group',
                                        title='Distribution of Total Main Workers for Top 10 Groups',width=900)
        fig_4.update_layout( height=500,width=730,title_font_color='orange',title_font=dict(size=20),title_x=0.2,showlegend=False)
        st.plotly_chart(fig_4)

        # Distribution of Total Marginal Workers for Top 10 Groups

        total_workers_by_state = df.groupby('Group')['Marginal Workers - Total -  Persons'].sum().reset_index()
        top_10_group =total_workers_by_state .sort_values(by='Marginal Workers - Total -  Persons', ascending=False).head(10)
        df_top_10_groups = df[df['Group'].isin(top_10_group['Group'])]
        fig_5= px.pie(top_10_group, values='Marginal Workers - Total -  Persons', names='Group',
                                        color_discrete_sequence=px.colors.sequential.Agsunset,
                                        title='Distribution of Total Marginal Workers for Top 10 Groups',width=900)
        fig_5.update_traces(textposition='outside', textinfo='percent')
        fig_5.update_layout( height=460,width=750,title_font_color='orange',title_font=dict(size=20),title_x=0.2)
        st.plotly_chart(fig_5)


    if select=='Class':


        # Distribution of Main workers across top and least 10 classes
        st.markdown("<h4 style='text-align:center; color:orange;'>Distribution of Main workers across top and least 10 classes</h4>", unsafe_allow_html=True)

        main_workers_class = df.groupby('Class')['Main Workers - Total -  Persons'].sum().reset_index()
        sorted_classes_top_10 = main_workers_class.nlargest(10, 'Main Workers - Total -  Persons')
        sorted_classes_least_10 = main_workers_class.nsmallest(10, 'Main Workers - Total -  Persons')
        
        colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)',
                'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)', 'rgb(23, 190, 207)']
        fig_6= make_subplots(rows=1, cols=2, subplot_titles=(".", "."),specs=[[{"type": "domain"}, {"type": "domain"}]])
      
        fig_6.add_trace(go.Pie(labels=sorted_classes_top_10['Class'], values=sorted_classes_top_10['Main Workers - Total -  Persons'], hole=0.5,
                                marker=dict(colors=colors)), row=1, col=1)
        fig_6.add_trace(go.Pie(labels=sorted_classes_least_10['Class'], values=sorted_classes_least_10['Main Workers - Total -  Persons'],hole=0.5,
                                marker=dict(colors=colors)), row=1, col=2)

        fig_6.update_traces(textposition='inside', textinfo='percent')
        fig_6.update_layout(autosize=False,  width=800, height=460, showlegend=False)
        for annotation in fig_6['layout']['annotations']:
            annotation['font'] = {'color': 'black','size':20}
        st.plotly_chart(fig_6)
        


        # Top 10 Classes by Marginal Workers", "Least 10 Classes by Marginal Workers

        st.markdown("<h4 style='text-align:center; color:orange;'>Distribution of Marginal workers across top and least 10 classes</h4>", unsafe_allow_html=True)

        marginal_workers_class = df.groupby('Class')['Marginal Workers - Total -  Persons'].sum().reset_index()

        # Sorting the classes by total marginal workers
        sorted_classes_top_10 = marginal_workers_class.nlargest(10, 'Marginal Workers - Total -  Persons')
        sorted_classes_least_10 = marginal_workers_class.nsmallest(10, 'Marginal Workers - Total -  Persons')

        
        fig_7 = make_subplots(rows=1, cols=2, subplot_titles=(".", "."),
                    specs=[[{"type": "domain"}, {"type": "domain"}]])
        
        fig_7.add_trace(go.Pie(labels=sorted_classes_top_10['Class'], values=sorted_classes_top_10['Marginal Workers - Total -  Persons']), row=1, col=1)
        fig_7.add_trace(go.Pie(labels=sorted_classes_least_10['Class'], values=sorted_classes_least_10['Marginal Workers - Total -  Persons']), row=1, col=2)
        fig_7.update_traces(textposition='inside', textinfo='percent')
        fig_7.update_layout(autosize=False, width=800, height=410,showlegend=False, margin=dict(t=40))
        for annotation in fig_7['layout']['annotations']:
            annotation['font'] = {'color': 'black','size':20}
        st.plotly_chart(fig_7)

         # Relationship between Main Workers and Marginal Workers in Rural Areas
        fig_r = px.scatter(df, x='Main Workers - Rural -  Persons', y='Marginal Workers - Rural -  Persons',color_discrete_sequence=px.colors.qualitative.Light24_r,
                          color='India/States', title='Relationship between Main Workers and Marginal Workers in Rural Areas')
        fig_r.update_layout( height=500,width=750,title_font_color='orange',title_font=dict(size=20),title_x=0.1,showlegend=False)
        fig_r.update_traces(marker=dict(size=12))
        st.plotly_chart(fig_r)

        # Relationship between Main Workers and Marginal Workers in Urban Areas
        fig_r1 = px.scatter(df, x='Main Workers - Urban -  Persons', y='Marginal Workers - Urban -  Persons',color_discrete_sequence=px.colors.qualitative.Vivid_r,
                          color='India/States', title='Relationship between Main Workers and Marginal Workers in Urban Areas')
        fig_r1.update_layout( height=500,width=750,title_font_color='orange',title_font=dict(size=20),title_x=0.1,showlegend=False)
        fig_r1.update_traces(marker=dict(size=12))
        st.plotly_chart(fig_r1)


    if select=='Division':

        # Trends in Main Workers vs Marginal Workers by Division

        grouped_data = df.groupby('Division').sum().reset_index()
        fig_8 = px.line(grouped_data, x='Division',
                                    y=['Main Workers - Total -  Persons','Marginal Workers - Total -  Persons'],
                                    color_discrete_map={'Main Workers - Total -  Persons': 'skyblue', 'Marginal Workers - Total -  Persons': 'red'},
                                    title='Trends in Main Workers vs Marginal Workers by Division')
        fig_8.update_layout(title_font_color='orange',title_font=dict(size=20),title_x=0.2,showlegend=False,width=750)
        fig_8.update_traces(mode="lines", line_shape='linear')
        st.plotly_chart(fig_8)

        # Distribution of Main Workers by Gender in Each Division
        
        main_workers_gender_division = df.groupby('Division')[['Main Workers - Total - Males', 'Main Workers - Total - Females']].sum().reset_index()

        main_workers_gender_division = main_workers_gender_division.melt(id_vars='Division', var_name='Gender', value_name='Count')
        fig_9= px.pie(main_workers_gender_division, names='Gender', values='Count',color_discrete_sequence=px.colors.diverging.Armyrose_r,
                                        title='Distribution of Main Workers by Gender in Each Division')

        fig_9.update_layout( height=460,width=900,title_font_color='orange',title_font=dict(size=20),title_x=0.1)
        st.plotly_chart(fig_9)

        # Distribution of Marginal Workers by Gender in Each Division

        marginal_workers_gender_division = df.groupby('Division')[['Marginal Workers - Total - Males', 'Marginal Workers - Total - Females']].sum().reset_index()
        marginal_workers_gender_division = marginal_workers_gender_division.melt(id_vars='Division', var_name='Gender', value_name='Count')
        fig_10 = px.pie(marginal_workers_gender_division, names='Gender', values='Count',color_discrete_sequence=px.colors.diverging.Temps,
                        title='Distribution of Marginal Workers by Gender in Each Division')
        fig_10.update_layout( height=460,width=900,title_font_color='orange',title_font=dict(size=20),title_x=0.1)
        st.plotly_chart(fig_10)      

    
    if select=='Districts':

        # Distribution of Main Workers by Top 10 Districts and Gender

        melted_df = pd.melt(df, id_vars=['District Code'], value_vars=['Main Workers - Total - Males',
                                                               'Main Workers - Total - Females'],
                    var_name='Gender', value_name='Number of Workers')
        main_workers_district = melted_df.groupby('District Code')['Number of Workers'].sum().reset_index()

        top_10_main_workers_district = main_workers_district.nlargest(10, 'Number of Workers')
        melted_top_10_df = melted_df[melted_df['District Code'].isin(top_10_main_workers_district['District Code'])]

        color_map = {'Main Workers - Total - Males': 'indianred', 'Main Workers - Total - Females': 'teal'}
        fig_11 = px.bar(melted_top_10_df  , x='District Code', y='Number of Workers',color='Gender',hover_name='Gender',barmode='group',
                    title='Distribution of Main Workers by Top 10 Districts and Gender',color_discrete_map=color_map)
        fig_11.update_xaxes(title='District Code')
        fig_11.update_yaxes(title='Number of Workers')
        fig_11.update_layout( height=500,width=900,title_font_color='orange',title_font=dict(size=20),title_x=0.1)
        st.plotly_chart(fig_11)


        # Distribution of Main Workers by least 10 Districts and Gender

        melted_df_s = pd.melt(df, id_vars=['District Code'], value_vars=['Main Workers - Total - Males',
                                                               'Main Workers - Total - Females'],
                    var_name='Gender', value_name='Number of Workers')
        main_workers_district = melted_df_s.groupby('District Code')['Number of Workers'].sum().reset_index()
        least_10_main_workers_district = main_workers_district.nsmallest(10, 'Number of Workers')
        melted_least_10_df = melted_df_s[melted_df_s['District Code'].isin(least_10_main_workers_district['District Code'])]

        color_map = {'Main Workers - Total - Males': 'lightblue', 'Main Workers - Total - Females':'coral'}
        fig_12 = px.bar(melted_least_10_df  , x='District Code', y='Number of Workers',color='Gender',hover_name='Gender',
                    title='Distribution of Main Workers by least 10 Districts and Gender',barmode='group',color_discrete_map=color_map)
        fig_12.update_xaxes(title='District Code')
        fig_12.update_yaxes(title='Number of Workers')
        fig_12.update_layout( height=500,width=900,title_font_color='orange',title_font=dict(size=20),title_x=0.1)
        st.plotly_chart(fig_12)


        # Comparison of Main Workers in Rural and Urban Areas for Top and Least 10 Districts
        main_workers_district = df.groupby('District Code')[['Main Workers - Rural -  Persons', 'Main Workers - Urban -  Persons']].sum()
        main_workers_district['Total Main Workers'] = main_workers_district.sum(axis=1)

        # Sorting the districts by total main workers and selecting the top 10 and least 10 districts
        top_10_main_workers_district = main_workers_district.nlargest(10, 'Total Main Workers')
        least_10_main_workers_district = main_workers_district.nsmallest(10, 'Total Main Workers')
        melted_top_10_df = top_10_main_workers_district.reset_index().melt(id_vars='District Code', var_name='Area', value_name='Number of Workers')
        melted_least_10_df = least_10_main_workers_district.reset_index().melt(id_vars='District Code', var_name='Area', value_name='Number of Workers')


        fig_13 = make_subplots(rows=1, cols=2, subplot_titles=("Top 10 Districts", "Least 10 Districts"))

        fig_13.add_trace(go.Bar(x=melted_top_10_df[melted_top_10_df['Area'] == 'Main Workers - Rural -  Persons']['District Code'], 
                                y=melted_top_10_df[melted_top_10_df['Area'] == 'Main Workers - Rural -  Persons']['Number of Workers'], 
                                name='Rural', marker_color='indianred'), row=1, col=1)
        fig_13.add_trace(go.Bar(x=melted_top_10_df[melted_top_10_df['Area'] == 'Main Workers - Urban -  Persons']['District Code'], 
                                y=melted_top_10_df[melted_top_10_df['Area'] == 'Main Workers - Urban -  Persons']['Number of Workers'], 
                                name='Urban', marker_color='lightgreen'), row=1, col=1)
        fig_13.add_trace(go.Bar(x=melted_least_10_df[melted_least_10_df['Area'] == 'Main Workers - Rural -  Persons']['District Code'], 
                                y=melted_least_10_df[melted_least_10_df['Area'] == 'Main Workers - Rural -  Persons']['Number of Workers'], 
                                name='Rural', marker_color='orange'), row=1, col=2)
        fig_13.add_trace(go.Bar(x=melted_least_10_df[melted_least_10_df['Area'] == 'Main Workers - Urban -  Persons']['District Code'], 
                                y=melted_least_10_df[melted_least_10_df['Area'] == 'Main Workers - Urban -  Persons']['Number of Workers'], 
                                name='Urban', marker_color='brown'), row=1, col=2)
        fig_13.update_layout(title="Comparison of Main Workers in Rural and Urban Areas in Districts",
                        xaxis=dict(title='District Code'),
                        yaxis=dict(title='Number of Workers'),height=500,width=900,title_font_color='orange',title_font=dict(size=20),title_x=0.1,
                        barmode='group')
        st.plotly_chart(fig_13)

        # Comparison of Marginal Workers in Rural and Urban Areas for Top and Least 10 Districts

        marginal_workers_district = df.groupby('District Code')[['Marginal Workers - Rural -  Persons', 'Marginal Workers - Urban -  Persons']].sum()
        marginal_workers_district['Total Marginal Workers'] = marginal_workers_district.sum(axis=1)

        # Sorting the districts by total marginal workers and selecting the top 10 and least 10 districts
        top_10_marginal_workers_district = marginal_workers_district.nlargest(10, 'Total Marginal Workers')
        least_10_marginal_workers_district = marginal_workers_district.nsmallest(10, 'Total Marginal Workers')
        melted_top_10_df = top_10_marginal_workers_district.reset_index().melt(id_vars='District Code', var_name='Area', value_name='Number of Workers')
        melted_least_10_df = least_10_marginal_workers_district.reset_index().melt(id_vars='District Code', var_name='Area', value_name='Number of Workers')


        fig_14 = make_subplots(rows=1, cols=2, subplot_titles=("Top 10 Districts", "Least 10 Districts"))

        #  top 10 districts
        fig_14.add_trace(go.Bar(x=melted_top_10_df[melted_top_10_df['Area'] == 'Marginal Workers - Rural -  Persons']['District Code'], 
                                y=melted_top_10_df[melted_top_10_df['Area'] == 'Marginal Workers - Rural -  Persons']['Number of Workers'], 
                                name='Rural', marker_color='indianred'), row=1, col=1)
        fig_14.add_trace(go.Bar(x=melted_top_10_df[melted_top_10_df['Area'] == 'Marginal Workers - Urban -  Persons']['District Code'], 
                                y=melted_top_10_df[melted_top_10_df['Area'] == 'Marginal Workers - Urban -  Persons']['Number of Workers'], 
                                name='Urban', marker_color='skyblue'), row=1, col=1)

        # least 10 districts
        fig_14.add_trace(go.Bar(x=melted_least_10_df[melted_least_10_df['Area'] == 'Marginal Workers - Rural -  Persons']['District Code'], 
                                y=melted_least_10_df[melted_least_10_df['Area'] == 'Marginal Workers - Rural -  Persons']['Number of Workers'], 
                                name='Rural', marker_color='orange'), row=1, col=2)
        fig_14.add_trace(go.Bar(x=melted_least_10_df[melted_least_10_df['Area'] == 'Marginal Workers - Urban -  Persons']['District Code'], 
                                y=melted_least_10_df[melted_least_10_df['Area'] == 'Marginal Workers - Urban -  Persons']['Number of Workers'], 
                                name='Urban', marker_color='purple'), row=1, col=2)
        fig_14.update_layout(title="Comparison of Marginal Workers in Rural and Urban Areas in Districts",
                        xaxis=dict(title='District Code'),
                        yaxis=dict(title='Number of Workers'),height=500,width=900,title_font_color='orange',title_font=dict(size=20),title_x=0.1,
                        barmode='group')
        st.plotly_chart(fig_14)

        
        #  Comparison of Main and Marginal Workers Across Top and Least 10 Districts
        district_totals = df.groupby('District Code')[['Main Workers - Total -  Persons', 'Marginal Workers - Total -  Persons']].sum()
        district_totals['Total Workers'] = district_totals.sum(axis=1)

        top_10_districts = district_totals.nlargest(10, 'Total Workers').index
        least_10_districts = district_totals.nsmallest(10, 'Total Workers').index
        top_10_df = df[df['District Code'].isin(top_10_districts)]
        least_10_df = df[df['District Code'].isin(least_10_districts)]


        top_10_df['Total Workers'] = top_10_df['Main Workers - Total -  Persons'] + top_10_df['Marginal Workers - Total -  Persons']
        least_10_df['Total Workers'] = least_10_df['Main Workers - Total -  Persons'] + least_10_df['Marginal Workers - Total -  Persons']

        main_color = 'turquoise' 
        marginal_color = 'pink'  

        fig_15= make_subplots(rows=1, cols=2, subplot_titles=("Top 10 Districts", "Least 10 Districts"))

        fig_15.add_trace(go.Bar(name='Main Workers', x=top_10_df['District Code'], y=top_10_df['Main Workers - Total -  Persons'], orientation='v', legendgroup='top', marker=dict(color=main_color)),
                    row=1, col=1)
        fig_15.add_trace(go.Bar(name='Marginal Workers', x=top_10_df['District Code'], y=top_10_df['Marginal Workers - Total -  Persons'], orientation='v', legendgroup='top', marker=dict(color=marginal_color)),
                    row=1, col=1)
        fig_15.add_trace(go.Bar(name='Main Workers', x=least_10_df['District Code'], y=least_10_df['Main Workers - Total -  Persons'], orientation='v', legendgroup='least', marker=dict(color=main_color)),
                    row=1, col=2)
        fig_15.add_trace(go.Bar(name='Marginal Workers', x=least_10_df['District Code'], y=least_10_df['Marginal Workers - Total -  Persons'], orientation='v', legendgroup='least', marker=dict(color=marginal_color)),
                    row=1, col=2)

        fig_15.update_layout(barmode='stack', title='Comparison of Main and Marginal Workers in Districts',
                        xaxis_title='District Code', yaxis_title='Number of Workers', legend_title='Worker Type',title_font_color='orange',
                        title_font=dict(size=20),title_x=0.2,
                        height=500, width=850, xaxis=dict(title='District Code'),showlegend=False)
        st.plotly_chart(fig_15)


    if select=='Industries':

        # Top 10 Industries
        nic_name_counts = df['NIC Name'].value_counts().reset_index()
        nic_name_counts.columns = ['NIC Name', 'Counts']
        nic_name_counts = nic_name_counts.sort_values(by='Counts', ascending=False)

        top_10_nic_names = nic_name_counts.head(10)

        fig_16 = px.bar(top_10_nic_names, x='NIC Name', y='Counts', 
                                title='Top 10 Industries', 
                                labels={'NIC Name': 'NIC Name', 'Counts': 'Count'})

        fig_16.update_layout( height=530,width=800,title_font_color='orange',title_font=dict(size=18),title_x=0.4)
        fig_16.update_traces(textfont_size=12,marker_color=px.colors.diverging.PiYG)
        fig_16.update_layout(xaxis=dict(tickangle=18))
        st.plotly_chart(fig_16)

        # Least 10 Industries
        nic_name_counts = df['NIC Name'].value_counts().reset_index()
        nic_name_counts.columns = ['NIC Name', 'Counts']
        nic_name_counts = nic_name_counts.sort_values(by='Counts', ascending=False)

        top_10_nic_names = nic_name_counts.tail(10)
        fig_17 = px.bar(top_10_nic_names, x='NIC Name', y='Counts', 
                                title='Least 10 Industries', 
                                labels={'NIC Name': 'NIC Name', 'Counts': 'Count'})

        fig_17.update_layout( height=530,width=800,title_font_color='orange',title_font=dict(size=18),title_x=0.4)
        fig_17.update_traces(textfont_size=12,marker_color=px.colors.diverging.RdYlBu)
        fig_17.update_layout(xaxis=dict(tickangle=18))
        st.plotly_chart(fig_17)



        industrial_sector_counts = df['NIC Name'].value_counts().reset_index()
        industrial_sector_counts.columns = ['NIC Name', 'Count']

        # Convert the data to a dictionary for WordCloud
        industrial_sector_dict = {row['NIC Name']: row['Count'] for index, row in industrial_sector_counts.iterrows()}

        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='inferno').generate_from_frequencies(industrial_sector_dict)

        st.markdown(f'<center><h4 style="color:orange">Most Occurring Industrial Sectors</h3></center>', unsafe_allow_html=True)
        st.image(wordcloud.to_array(), use_column_width=True)


        word_freq = df.groupby('NIC Name').agg({
        'Main Workers - Total - Males': 'sum',
        'Main Workers - Total - Females': 'sum',
        'Main Workers - Rural - Males': 'sum',
        'Main Workers - Rural - Females': 'sum',
        'Main Workers - Urban - Males': 'sum',
        'Main Workers - Urban - Females': 'sum'
        }).reset_index()


        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_text(' '.join(word_freq['NIC Name']))
        st.markdown(f'<center><h4 style="color:orange">Most frequently occurring Industrial sectors by Gender</h3></center>', unsafe_allow_html=True)
        st.image(wordcloud.to_array(), use_column_width=True)

        # Top 10 Industries by Total Workers'
        workers_by_nic = df.groupby('NIC Name')[['Main Workers - Total -  Persons','Marginal Workers - Total -  Persons']].sum().reset_index()
        workers_by_nic['Total Workers'] = workers_by_nic['Main Workers - Total -  Persons'] + workers_by_nic['Marginal Workers - Total -  Persons']

        top_10_nic = workers_by_nic.nlargest(10, 'Total Workers')
        fig_18 = px.pie(top_10_nic ,values='Total Workers', names='NIC Name',
                    color_discrete_sequence=px.colors.sequential.Oryel_r,
                    title='Top 10 Industries by Total Workers')
        fig_18.update_layout( height=480,width=700,title_font_color='orange',title_font=dict(size=20),title_x=0.3,showlegend=False)
        st.plotly_chart(fig_18)
        

        # Top 10 India/States by NIC Name based on Main workers
        workers_by_nic_state = df.groupby(['NIC Name', 'India/States'])['Main Workers - Total -  Persons'].sum().reset_index()

        top_10_states_by_nic = workers_by_nic_state.groupby('NIC Name').apply(lambda x: x.nlargest(10, 'Main Workers - Total -  Persons')).reset_index(drop=True)
        fig_19 = px.bar(top_10_states_by_nic.head(35), x='India/States', y='Main Workers - Total -  Persons', color='NIC Name',
                    title='Top 10 States by NIC Name based on Main workers')
        fig_19.update_layout( height=600,width=900,title_font_color='orange',title_font=dict(size=18),title_x=0.2,
                        legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.6))
        fig_19.update_traces(textfont_size=12,marker_color=px.colors.diverging.RdYlGn)
        st.plotly_chart(fig_19)


        workers_by_nic_state = df.groupby(['NIC Name', 'India/States'])['Marginal Workers - Total -  Persons'].sum().reset_index()

        top_10_states_by_nic = workers_by_nic_state.groupby('NIC Name').apply(lambda x: x.nlargest(10, 'Marginal Workers - Total -  Persons')).reset_index(drop=True)
    
        fig_20 = px.bar(top_10_states_by_nic.head(35), x='India/States', y='Marginal Workers - Total -  Persons', color='NIC Name',
                    title='Top 10 States by NIC Name based on Marginal workers')
        fig_20.update_layout( height=650,width=900,title_font_color='orange',title_font=dict(size=20),
                        title_x=0.2,legend=dict(orientation='v', yanchor='top', y=1.1, xanchor='center', x=0.5))
        fig_20.update_layout(xaxis=dict(tickangle=45))
        fig_20.update_traces(textfont_size=12,marker_color=px.colors.diverging.Spectral_r)
        st.plotly_chart(fig_20)

if selected=='Insights':

    st.subheader(":orange[Gender:]")

    st.markdown(""" 
                - West Bengal,Rajasthan are the top two states with the highest number of workers, both male and female.
                
                - There's a significant gender distribution among main workers, with males constituting a larger proportion compared to females.
                
                - It's useful for understanding how gender dynamics vary among marginal workers, particularly in rural and urban areas.

                """)
    
    st.subheader(":orange[Groups:]")

    st.markdown(""" 
            
            - It helps identify the groups with the highest number of main workers, highlighting which sectors contribute the most to the workforce.It's essential for policymakers and businesses to understand where the majority of workers are employed.
            
            - Similar to main workers, agricultural and related workers also dominate the group of marginal workers, indicating the prevalence of seasonal or part-time agricultural employment.

            """)
    
    st.subheader(":orange[classes:]")

    st.markdown(""" 
            
            - By comparing the top and least 10 classes by the number of main workers, Policymakers can use this information to focus on uplifting underrepresented classes and improving opportunities for all.
            - Understanding the distribution of marginal workers can help address socioeconomic disparities and promote inclusive growth.
            
            """)
    
    st.subheader(" :orange[Division:]")

    st.markdown(""" 

            - Identifying whether main or marginal workers are increasing or decreasing in each division can inform labor policies and economic strategies.


            - Main workers are predominantly male across all divisions, reflecting gender disparities in formal employment.
            
            - The distribution of main workers differs significantly from that of marginal workers, as this could indicate distinct employment patterns or opportunities for men and women.

            """)
    st.subheader(":orange[Districts:]")

    st.markdown("""     
            - The top 10 districts with the highest number of main workers are predominantly urban and industrialized areas.There's a noticeable gender gap in main workforce participation across districts, with males outnumbering females.
                
            - By comparing main workers in rural and urban areas across districts, policymakers can understand urbanization trends and the distribution of employment opportunities.
            """)

    st.subheader(":orange[Industries:]")
    
    st.markdown(""" 

           - Industries related to agriculture, manufacturing, and construction dominate the top 10 industries in terms of workforce participation.
            
           - Word clouds highlight the most frequently occurring industrial sectors, providing insights into the industries with the highest workforce participation.

            """)
                    
