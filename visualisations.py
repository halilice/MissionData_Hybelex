# Import the modules
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import regex as re
import folium
from streamlit_folium import st_folium
sns.set_style("whitegrid")
# Execute the following code to avoid displaying the numbers in scientific notation
pd.options.display.float_format = '{:.2f}'.format

# Execute the following code to avoid the 'SettingWithCopyWarning' warnings
pd.options.mode.chained_assignment = None

# Execute the following code to avoid the 'FutureWarning'
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def home():
    st.subheader('The first fifty rows of the dataset')

    df = pd.read_csv(r"Electric_Vehicle_Population_Data_clean.csv")
    st.write(df.head(50))

    st.subheader('Descriptive Statistics of dataset')
    df_desc = df.describe()
    st.write(df_desc)

    st.text("\n") 
    st.text("""
        There are 190989 vehicles in our database after cleaning and dropping the missing
        values. We can see from descriptive statistics that: 
            - The model year of the vehicles is in range of 1997 and 2025. We can say that
            the registration of the elecric and hybrid vehicules increased widely after 
            2019 by looking the first quantile (2019) and median (2022) values. 75 percent 
            of the registrations made after 2019 where the production and usage of these 
            type of vehicules increased.  
            - Electric range of the vehicles in dataset vary between 0 and 337 miles. So, 
            the vehicle which has the longest range can be driven for 337 miles maximum.
            - Base MSRP (Manufacturer’s Suggested Retail Price) of vehicles is 993 us 
            dollars in average and 845 thousand dollars at most. 
        We can see that there are zeros in columns 'Electric Range' and 'Base MSRP'. We 
        would like to know that percentage of zeros in total.""")
    st.text("\n") 

    per_zer_msrp = (len(df[df['Base MSRP'] == 0]) / len(df)) * 100
    per_zer_er =(len(df[df['Electric Range'] == 0]) / len(df)) * 100
    st.write('The percentage of zeros in column "Base MSRP" is:', per_zer_msrp)
    st.write('The percentage of zeros in column "Electric Range" is:', per_zer_er)
         
    st.text("""
        98 percent of the 'Base MSRP' values are zero which means that we can't make any 
        analysis on this column. Almost half of the 'Electric Range' values are zero and 
        we will make an analysis on this column at the end.""")

    st.subheader('Correlation coefficients between numeric variables')
    st.write(df.select_dtypes('number').corr())
    st.text("\n")
    st.text("""
        We can say that there is not a strong correlation between variables by looking at 
        the table above. We will now look the evolution of electric cars over time.""")

df = pd.read_csv(r"Electric_Vehicle_Population_Data_clean.csv")
def obj_to_lst(x):
    y = x[1:-1]
    y = re.sub(',', '', y)
    y = y.split()
    return y

df['Vehicle Location'] = df['Vehicle Location'].apply(obj_to_lst)

def basic_indic():
    st.subheader('Evolution of Electric Car Numbers over Time')
    st.text("""
        I will start with drawing a time-series line graphic in order to analyse the
        evolution of electric car registrations in Washington State over time. This 
        will give us a good idea about the progress of electic vehicles.""")
    number_by_year = df.groupby('Year').agg(**{'Frequency': ('Car_Mark', lambda x: x.count())}).reset_index()
    evol_num_veh = sns.lineplot(data=number_by_year, x='Year', y='Frequency')
    plt.title('Evolution of Electric Car Numbers over Time', pad=15, fontsize=15, loc='left')
    st.pyplot(evol_num_veh.figure)
    st.text("""
        We can intrepret that the number of registration of electric cars until 2010 
        follows a steady trend. After that year, it begins to increase little by little 
        until 2017 where it sees a slight decline. After it made its peak in 2023 with 
        a number of 60 thousand registers it sees a sharp decline.
        We will now look into the distribution of brands, models, type of vehicules etc...""")

    st.subheader('Distribution of Electric Vehicle Types')
    st.text("""
        Now, we will investigate the proprotion of Electric and Hybrid vehicles
        in total number of the vehicles in this dataset.""")
    type_vehicule_count = df['Type_Vehicle'].value_counts()
    st.write('\nThe numbers of each vehicle type are: ', type_vehicule_count)
    st.text('\n')
    fig, ax = plt.subplots(figsize=(10,7))
    sns.countplot(data=df, y='Type_Vehicle', palette='Blues')
    plt.title('The Distribution of Electric Vehicle Types', pad=15, fontsize=15, loc='left')
    plt.ylabel('Vehicle Type')
    st.pyplot(fig)
    st.text("""
        There are two types of vehicle in this dataset and almost 80 percent of them 
        are Battery Electric Vehicles.""")

    st.subheader('The distribution of Vehicle Brands')
    st.text("""
        A visual showing the distribution of vehicle brand in terms of numbers will 
        give us a good idea which brand people choice and the decisions that we will make 
        on the future.""")
    car_brands_count = df.groupby('Car_Mark').agg(**{'count': ('Car_Mark', lambda x: x.count())}).reset_index()
    top_10_brand = car_brands_count.sort_values(by='count', ascending=False).head(10)
    st.write('\nThe number of vehicle brands:', len(car_brands_count), '\n')
    fig, ax = plt.subplots(figsize=(10,7))
    sns.barplot(data=top_10_brand, x='count', y='Car_Mark',  palette='rocket', errorbar=None)
    plt.title('The Distribution of Vehicle Brands', pad=15, fontsize=15, loc='left')
    plt.ylabel('Vehicle Brands')
    st.pyplot(fig)  
    st.text("""
        There are 42 different vehicle brands in dataset in total. Tesla is in 
        first place with a number of around 80 thousand vehicles. Chevrolet and 
        Nissan follows Tesla in second and third places with around 12 thousand 
        vehicles.""")
    
    st.subheader('The distribution of Vehicle Brands by Vehicle Type')
    st.text("""
        We will now differentiate the car brands between Battery Electric Vehicles 
        and Plug-in Hybrid Electric Vehicles.""")
    car_brands_count_bev = df[df['Type_Vehicle'] == 'Battery Electric Vehicle (BEV)']\
                        .groupby('Car_Mark').agg(**{'count': ('Car_Mark', lambda x: x.count())}).reset_index()
    car_brands_count_phev = df[df['Type_Vehicle'] == 'Plug-in Hybrid Electric Vehicle (PHEV)']\
                        .groupby('Car_Mark').agg(**{'count': ('Car_Mark', lambda x: x.count())}).reset_index()

    # Take top 10 brands for each type
    top_10_bev = car_brands_count_bev.sort_values(by='count', ascending=False).head(10)
    top_10_phev = car_brands_count_phev.sort_values(by='count', ascending=False).head(10)

    # Plot the graphs
    fig, ax = plt.subplots(1,2, figsize=(20,10))
    ax1 = plt.subplot(1,2,1)
    sns.barplot(data=top_10_bev, x='count', y='Car_Mark', palette='rocket')
    ax1.set_title('Battery Electric Vehicles', pad=15, fontsize=15, loc='left')
    ax1.set_ylabel('Vehicle Brands')

    ax2 = plt.subplot(1,2,2)
    sns.barplot(data=top_10_phev, x='count', y='Car_Mark', palette='rocket')
    ax2.set_title('Plug-in Hybrid Electric Vehicles', pad=15, fontsize=15, loc='left')
    ax2.set_ylabel('Vehicle Brands')    

    st.pyplot(fig)

    st.text("""
        The distribution of car brands for Battery Electric Vehicles is similar 
        to general distribution where Tesla, Nissan and Chevrolet are in top 3 
        places. But, the distribution of car brands for Plug-in Hybrid Electric 
        Vehicles is more balanced and we see different brands than the other type. 
        Toyota is in first place with a number of 7 thousand vehicles, BMW and 
        Jeep follow it in second and third places.""")

    st.subheader('The distribution of Models')
    st.text("""
        We will now dig into the distribution of models.""")
    car_models_count = df.groupby(['Type_Vehicle', 'Car_Mark', 'Model']).agg(**{'count': ('Model', lambda x: x.count())}).reset_index()
    top_10_models = car_models_count.sort_values(by='count', ascending=False).head(10)
    st.write('\nThe number of vehicle models:', len(car_models_count), '\n')
    st.write('\nThe numbers of each top 10 vehicle models are: \n', top_10_models, "\n")

    fig, ax = plt.subplots()
    sns.barplot(data=top_10_models, x='count', y='Model', palette="mako")
    plt.title('The Distribution of Vehicle Models', pad=15, fontsize=15, loc='left')
    plt.ylabel('Vehicle Models')
    st.pyplot(fig)

    st.text("""
        We can clearly see from table and the graph that the most registered electric
        car models are Tesla with the models Model Y, Model 3, Model S and Model X. 
        There are two model of Chevrolet in top 10 model which are 'Bolt EV' and 'Volt'
        whereas Nissan, Volkswagen, Ford and Jeep have only one model each. In addition
        to these, there are two models of type Plug-in Hybrid Electric Vehicle in top
        10 models.""")

    st.subheader('The distribution of Models by Vehicle Type')
    st.text("""
        We will now look at the distribution of models by type of the vehicle.""")
    N = 10
    df1 = car_models_count.sort_values(by=['Type_Vehicle', 'count'], ascending=[True, False])
    df1 = df1.groupby('Type_Vehicle', as_index=False).nth[:N]
    st.write('\nThe numbers of each top 10 vehicle models by type are: \n', df1, "\n")

    # Take top 10 models for each type
    top_10_mod_bev = df1[df1['Type_Vehicle'] == 'Battery Electric Vehicle (BEV)']
    top_10_mod_phev = df1[df1['Type_Vehicle'] == 'Plug-in Hybrid Electric Vehicle (PHEV)']

    # Plot the graphs
    fig, ax = plt.subplots(1,2, figsize=(20,10))
    ax1 = plt.subplot(1,2,1)
    sns.barplot(data=top_10_mod_bev, x='count', y='Model', palette='mako')
    ax1.set_title('Battery Electric Vehicles', pad=15, fontsize=15, loc='left')
    ax1.set_ylabel('Vehicle Models')

    ax2 = plt.subplot(1,2,2)
    sns.barplot(data=top_10_mod_phev, x='count', y='Model', palette='mako')
    ax2.set_title('Plug-in Hybrid Electric Vehicles', pad=15, fontsize=15, loc='left')
    ax2.set_ylabel('Vehicle Models')
    st.pyplot(fig)

def geog_dist():
    st.subheader('Top 5 counties in terms of registered electric cars')
    st.text("""
        I want to start the geographical distribution analysis of vehicles with visualising
        the county level. I can't visualise all of the counties because there are 39 of them 
        in total in database. I choose top five Counties in terms of vehicle numbers and 
        draw a treemap.""")
    geo_count = df.groupby(['County']).agg(**{'count': ('Model', lambda x: x.count())}).reset_index()

    geo_count1 = geo_count.sort_values(by='count', ascending=False).head(5)
    t5 = geo_count1['count'].sum()
    st.write('\nThe total number of electric cars in top 5 country are: ', t5)
    st.write('\nThe ratio of The total number of electric cars in top 5 county to total cars is', round(t5/len(df), 2)*100,'percent\n')

    fig = px.treemap(geo_count1, path=[px.Constant("County"), 'County',
                  ], values='count',
                  color='count',
                  color_continuous_scale='RdBu')
    fig.update_layout(margin = dict(t=25, l=25, r=25, b=25))
    st.plotly_chart(fig)
    st.text("""
        We can clearly see that the ratio of electric car numbers in top five County to
        total electric car numbers in database is 0.80 that is 80 percent of total.
        The King County alone represents more than half of electric car registrations in 
        State with almost 100 thousand cars.""")

    st.subheader('Top 5 counties and their top 3 Cities in terms of the numbers of registered electric cars')
    st.text("""
        I want to dig a bit deeper and and go on City level. I will show the three first
        Cities in each County in terms of the vehicle numbers.""")

    first5 = df['County'].value_counts().head(5).index.to_list()
    df_first5_county = df[df['County'].isin(first5)]

    df_first5_county = df_first5_county.groupby(['County', 'City']).agg(**{'count': ('City', lambda x: x.count())}).reset_index()

    N = 3
    df_first5_county1 = df_first5_county.sort_values(by=['County', 'count'], ascending=[True, False])
    df_first5_county1 = df_first5_county1.groupby('County', as_index=False).nth[:N]

    fig = px.treemap(df_first5_county1, path=[px.Constant("County"), 'County',
                  'City'], values='count',
                  color='City',
                  color_continuous_scale='RdBu')
    fig.update_layout(margin = dict(t=25, l=25, r=25, b=25))
    st.plotly_chart(fig)


def tesla_map():
    st.subheader('Geographic Distribution of Tesla Electric Cars on Map')
    df_tesla = df[df['Car_Mark'] == 'TESLA'].head(1000)
    position_wash = [47.62, -117.4]
    t = folium.Map(location = position_wash, zoom_start=7)

    for i in range(len(df_tesla)):
        folium.Marker(location=df_tesla.iloc[i,8],
                popup=df_tesla.iloc[i,0],
                icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(t)
    return st_folium(t, width=1300)

def nissan_map():
    st.subheader('Geographic Distribution of Nissan Electric Cars on Map')
    df_nissan = df[df['Car_Mark'] == 'NISSAN'].head(1000)
    position_wash = [47.751076, -120.740135]
    n = folium.Map(location = position_wash, zoom_start=7)

    for i in range(len(df_nissan)):
        folium.Marker(location=df_nissan.iloc[i,8],
                popup=df_nissan.iloc[i,0],
                icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(n)
    return st_folium(n, width=1300)

def chevrolet_map():
    st.subheader('Geographic Distribution of Chevrolet Electric Cars on Map')
    df_chev = df[df['Car_Mark'] == 'CHEVROLET'].head(1000)
    position_wash = [47.751076, -120.740135]
    c = folium.Map(location = position_wash, zoom_start=7)

    for i in range(len(df_chev)):
        folium.Marker(location=df_chev.iloc[i,8],
                popup=df_chev.iloc[i,0],
                icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(c)
    return st_folium(c, width=1300)

def ford_map():
    st.subheader('Geographic Distribution of Ford Electric Cars on Map')
    df_ford = df[df['Car_Mark'] == 'FORD'].head(1000)
    position_wash = [47.751076, -120.740135]
    f = folium.Map(location = position_wash, zoom_start=7)

    for i in range(len(df_ford)):
        folium.Marker(location=df_ford.iloc[i,8],
                popup=df_ford.iloc[i,0],
                icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(f)
    return st_folium(f, width=1300)

def kia_map():
    st.subheader('Geographic Distribution of Kia Electric Cars on Map')
    df_kia = df[df['Car_Mark'] == 'KIA'].head(1000)
    position_wash = [47.751076, -120.740135]
    f = folium.Map(location = position_wash, zoom_start=7)

    for i in range(len(df_kia)):
        folium.Marker(location=df_kia.iloc[i,8],
                popup=df_kia.iloc[i,0],
                icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(f)
    return st_folium(f, width=1300)

def range_veh():
    st.subheader('Analysis of Electric Vehicle Ranges')

    st.text("""
        First of all i will plot a time series graphic in order to visualise the 
        evolution of the ranges of electric vehicles over time. For this, i will
        insert the years on x axis and the electric range on y axis.""")
    fig, ax = plt.subplots(figsize=(10,7))
    sns.lineplot(data=df, x='Year', y='Electric Range')
    plt.title('Evolution of Electric Car Range over Time', pad=15, loc='left', fontsize=15)
    plt.ylabel('Range(km)')
    st.pyplot(fig)

    st.text("""
        We can clearly see from the graphic that the range of electric cars had
        increased until 2010 and after that it sharply declined until 2012. We
        see a constant rise after that point up until 2020. It has been weirdly
        decreasing after 2020 although the technology on this area has been 
        improving constantly. We will investigate that, it maybe come from the
        zeros (unknown) values in this column. We will filter the dataframe by
        year to be after 2020 for investigating the reasons.""")
    st.text('\n')

    df_filter = df[df['Year']>=2020]
    st.write('\nThe percentage of zeros in column "Electric Range" is: ', 
          (len(df_filter[df_filter['Electric Range'] == 0]) / len(df_filter)) * 100)
    st.text('\n')
    st.text("""
        We see that almost three fourths of the 'Electric range' values are
        zero.""")

    # st.subheader('Distribution of vehicles ranges')
    # st.write('\nAverage range of electtric vehicles is: ', df['Electric Range'].mean(), 'miles\n')
    # fig, ax = plt.subplots(figsize=(10,7))
    # sns.histplot(data=df, x='Electric Range')
    # plt.axvline(df['Electric Range'].mean(), color='r',  linestyle='dashed',linewidth=1)
    # plt.title("Distribution of Electic Vehicles' Ranges", pad=15, loc='left', fontsize=15)
    # st.pyplot(fig)

    # st.text("""
        # There are more than 100 thousand vehicles that we don't know their ranges.
        # It is too hard to make comment by looking at this graph so that we will 
        # filter the vehicles with missing values and draw a new graph.""")

    st.subheader('The distribution of vehicles ranges without missing values')
    df_filter_zero = df[df['Electric Range'] != 0]
    st.write('\nAverage range of electtric vehicles after filtering is: ', df_filter_zero['Electric Range'].mean(), 'miles\n')
    fig, ax = plt.subplots(figsize=(10,7))
    sns.histplot(data=df_filter_zero, x='Electric Range')
    plt.axvline(df_filter_zero['Electric Range'].mean(), color='r', linestyle='dashed', linewidth=1)
    plt.title("Distribution of Electic Vehicles' Ranges after Filtering", pad=15, loc='left', fontsize=15)
    st.pyplot(fig)
    st.text("""
        As can be seen from the graphic, the average range of electric cars in 
        dataset is almost 120 miles. We can see a clustering around 20 and 40 
        miles and at on the other side aorund 200 miles.""")
    
    st.subheader('10 models with longest electric range')
    st.text("""
        I want to show the top ten models with longest range in order to 
        have a complete understanding of the dataset and electric vehicles. """)
    model_longest = df.groupby('Model').agg(**{'max_range': ('Electric Range', lambda x: x.max())}).reset_index()
    ten_model_longest = model_longest.sort_values(by='max_range', ascending=False).head(10)

    #Plot the graph
    fig,ax = plt.subplots(figsize=(10,7))
    sns.barplot(data=ten_model_longest, x='max_range', y='Model', palette="viridis")
    plt.title('Top 10 Electric Vehicles with Longest Range', pad=15, fontsize=15, loc='left')
    plt.ylabel('Vehicle Models')
    st.pyplot(fig)
    st.text("""
        As it can be seen from the graph, the models of Tesla Model S, 3, X and Y 
        in top 4 in terms of range.""")
