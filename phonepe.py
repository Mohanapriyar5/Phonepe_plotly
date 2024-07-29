import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector 
import plotly.express as px
import requests
import json
from PIL import Image

sqlconn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database = "phonepe_data")
cursor = sqlconn.cursor()

#Taking aggregated_insurance_df
cursor.execute("select * from aggregated_insurance")
table1 = cursor.fetchall()
sqlconn.commit()

Aggregated_insurance = pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type",
                                                    "Transaction_count","Transaction_amount"))

#Taking aggregated_transaction_df
cursor.execute("select * from aggregated_transaction")
table2 = cursor.fetchall()
sqlconn.commit()

Aggregated_transaction = pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type",
                                                    "Transaction_count","Transaction_amount"))

#Taking aggregated_user_df
cursor.execute("select * from aggregated_user")
table3 = cursor.fetchall()
sqlconn.commit()

Aggregated_user = pd.DataFrame(table3,columns=("States","Years","Quarter","Brands",
                                                    "Transaction_count","Percentage"))
#Taking map_insurance_df
cursor.execute("select * from map_insurance")
table4 = cursor.fetchall()
sqlconn.commit()

Map_insurance = pd.DataFrame(table4,columns=("States","Years","Quarter","District",
                                                    "Transaction_count","Transaction_amount"))

#Taking map_transaction_df
cursor.execute("select * from map_transaction")
table5 = cursor.fetchall()
sqlconn.commit()

Map_transaction = pd.DataFrame(table5,columns=("States","Years","Quarter","District",
                                                    "Transaction_count","Transaction_amount"))

#Taking map_user_df
cursor.execute("select * from map_insurance")
table6 = cursor.fetchall()
sqlconn.commit()

Map_user = pd.DataFrame(table6,columns=("States","Years","Quarter","District",
                                                    "RegisteredUser","AppOpens"))
#Taking top_insurance_df
cursor.execute("select * from top_insurance")
table7 = cursor.fetchall()
sqlconn.commit()

Top_insurance = pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes",
                                                    "Transaction_count","Transaction_amount"))

#Taking top_transaction_df
cursor.execute("select * from top_transaction")
table8 = cursor.fetchall()
sqlconn.commit()

Top_transaction = pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes",
                                                    "Transaction_count","Transaction_amount"))

#Taking top_user_df
cursor.execute("select * from top_user")
table9 = cursor.fetchall()
sqlconn.commit()

Top_user = pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes",
                                                    "RegisteredUser"))

def Transaction_amount_count_Y(df, year):
    trans = df[df["Years"] == year]
    trans.reset_index(drop = True,inplace = True)
    
    trans_group = trans.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    trans_group.reset_index(inplace = True)

    col1,col2= st.columns(2)
    with col1:
        fig_amount = px.bar(trans_group,x='States',y='Transaction_amount',title=f'{year} TRANSACTION AMOUNT',color_discrete_sequence=px.colors.sequential.Sunsetdark_r,height=500,width=450)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(trans_group,x='States',y='Transaction_count',title=f'{year} TRANSACTION COUNT',height=500,width=450)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        
        states_name.sort()
        fig_india_1 = px.choropleth(trans_group, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                color = "Transaction_amount", color_continuous_scale = "Rainbow",
                                range_color = (trans_group["Transaction_amount"].min(), trans_group["Transaction_amount"].max()),
                                hover_name = "States", title = f"{year} TRANSACTION AMOUNT", fitbounds = "locations",
                                height = 500, width = 500)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(trans_group, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                color = "Transaction_count", color_continuous_scale = "Rainbow",
                                range_color = (trans_group["Transaction_count"].min(), trans_group["Transaction_count"].max()),
                                hover_name = "States", title = f"{year} TRANSACTION COUNT", fitbounds = "locations",
                                height = 500, width = 500)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    return trans

def Transaction_amount_count_Y_Q(df, quarter):
    trans = df[df["Quarter"] == quarter]
    trans.reset_index(drop = True,inplace = True)
    
    trans_group = trans.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    trans_group.reset_index(inplace = True)

    col1,col2= st.columns(2)
    with col1:
        fig_amount = px.bar(trans_group,x='States',y='Transaction_amount',title=f'{trans["Years"].min()} QUARTER {quarter} TRANSACTION AMOUNT',color_discrete_sequence=px.colors.sequential.Sunsetdark_r,height=500,width=450)
        st.plotly_chart(fig_amount)
    
    with col2:
        fig_count = px.bar(trans_group,x='States',y='Transaction_count',title=f'{trans["Years"].min()} QUARTER {quarter} TRANSACTION COUNT',height=500,width=450)
        st.plotly_chart(fig_count)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    
    states_name.sort()

    col1,col2= st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(trans_group, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                color = "Transaction_amount", color_continuous_scale = "Rainbow",
                                range_color = (trans_group["Transaction_amount"].min(), trans_group["Transaction_amount"].max()),
                                hover_name = "States", title = f"{trans["Years"].min()} QUARTER {quarter} TRANSACTION AMOUNT", fitbounds = "locations",
                                height = 500, width = 500)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(trans_group, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                color = "Transaction_count", color_continuous_scale = "Rainbow",
                                range_color = (trans_group["Transaction_count"].min(), trans_group["Transaction_count"].max()),
                                hover_name = "States", title = f"{trans["Years"].min()} QUARTER {quarter} TRANSACTION COUNT", fitbounds = "locations",
                                height = 500, width = 500)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    
    return trans

def aggr_trans_Transaction_type(df,state):

    trans = df[df["States"] == state]
    trans.reset_index(drop = True,inplace = True)
    #trans
    trans_group = trans.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    trans_group.reset_index(inplace = True)
    #trans_group
    col1,col2= st.columns(2)
    with col1:
        fig_pie1 = px.pie(data_frame = trans_group, names="Transaction_type", values= "Transaction_amount",
                        width = 500, hole = 0.5, title= f"{state.upper()} TRANSACTION AMOUNT")
        st.plotly_chart(fig_pie1)
    
    with col2:
        fig_pie2 = px.pie(data_frame = trans_group, names="Transaction_type", values= "Transaction_count",
                        width = 500, hole = 0.5, title= f"{state.upper()} TRANSACTION COUNT")
        st.plotly_chart(fig_pie2)

#Aggregated user analysis 1
def Aggre_user_plot1(df,year):

    aguy = df[df["Years"] == year]
    aguy.reset_index(drop = True, inplace = True)
    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index( inplace = True)
    
    fig_bar_1 = px.bar(aguyg, x = "Brands", y = "Transaction_count", title = f"{year} BRANDS AND TRANSACTION COUNT",
                      width = 600, color_discrete_sequence=px.colors.sequential.haline_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggregated user analysis 2
def Aggre_user_plot2(df,quarter):
    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop = True, inplace = True)
    
    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index( inplace = True)
    
    fig_bar1 = px.bar(aguyqg, x = "Brands", y = "Transaction_count", title = f"Quarter- {quarter}, BRANDS AND TRANSACTION COUNT",
                          width = 600, color_discrete_sequence=px.colors.sequential.haline_r, hover_name = "Brands")
    st.plotly_chart(fig_bar1)

    return aguyq

#Aggregated user analysis 3
def Aggre_user_plot3(df,state):
    aguyqs = df[df["States"] == state]
    aguyqs.reset_index(drop= True, inplace = True)
    
    aguyqsg = aguyqs.groupby("Brands")[["Transaction_count", "Percentage"]].sum()
    aguyqsg.reset_index(inplace=True)
    
    fig_line_1 = px.line(aguyqsg, x ="Brands", y ="Transaction_count", hover_data = "Percentage",
                         title = f"{state.upper()}- BRANDS, TRANSACTION_COUNT, PERCENTAGE", width = 800, markers= True)
    st.plotly_chart(fig_line_1)

#Map Insurance Districts
def Map_insur_District(df,state):

    trans = df[df["States"] == state]
    trans.reset_index(drop = True,inplace = True)
    #trans
    trans_group = trans.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    trans_group.reset_index(inplace = True)
    #trans_group
    
    col1,col2= st.columns(2)
    with col1:
        fig_bar_1 = px.bar(trans_group, x= "Transaction_amount", y= "District", orientation = "h", title = f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",
                      color_discrete_sequence = px.colors.sequential.Mint_r,width = 500, height = 500)
        st.plotly_chart(fig_bar_1)
    
    with col2:
        fig_bar_2 = px.bar(trans_group, x= "Transaction_count", y= "District", orientation = "h", title = f"{state.upper()} DISTRICT AND TRANSACTION COUNT",
                      color_discrete_sequence = px.colors.sequential.Bluered_r,width = 500, height = 500)
        st.plotly_chart(fig_bar_2)

# Map user plot 1
def map_user_plot1(df,year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop = True, inplace = True)
    #muy
    muyg = muy.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyg.reset_index( inplace = True)
    
    fig_line_2 = px.line(muyg, x ="States", y =["RegisteredUser", "AppOpens"], 
                             title = f"{year} REGISTERED_USER AND APP_OPENS", width = 800,height = 600, markers = True)
    st.plotly_chart(fig_line_2)

    return muy

# Map user plot 2
def map_user_plot2(df,quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True, inplace = True)
    #muyq
    muyqg = muyq.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyqg.reset_index( inplace = True)
    
    fig_line_3 = px.line(muyqg, x ="States", y =["RegisteredUser", "AppOpens"], 
                             title = f"QUARTER-{quarter} REGISTERED_USER AND APP_OPENS", width = 800,height = 600, markers = True)
    st.plotly_chart(fig_line_3)

    return muyq

# Map user plot 3
def map_user_plot3(df,states):
    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop = True, inplace = True)
    #muyqs
    col1,col2 = st.columns(2)
    with col1:
        fig_map_user_bar1 = px.bar(muyqs, x= "RegisteredUser", y = "District", orientation = "h",
                                title = f"{states.upper()} REGISTERED USER")
        st.plotly_chart(fig_map_user_bar1)

    with col2:
        fig_map_user_bar2 = px.bar(muyqs, x= "AppOpens", y = "District", orientation = "h",
                                title = f"{states.upper()} APP OPENS")
        st.plotly_chart(fig_map_user_bar2)

# Top Insurance plot 1
def top_insurance_plot1(df,state):
    tiy = df[df["States"] == state]
    tiy.reset_index(drop = True, inplace = True)

    col1,col2 = st.columns(2)
    with col1:   
        fig_top_insur_bar1 = px.bar(tiy, x= "Quarter", y = "Transaction_amount", hover_data = "Pincodes", 
                                    title = "TRANSACTION AMOUNT",height = 600,width= 500)
        st.plotly_chart(fig_top_insur_bar1)

    with col2:
        fig_top_insur_bar2 = px.bar(tiy, x= "Quarter", y = "Transaction_count", hover_data = "Pincodes", 
                                    title = "TRANSACTION COUNT",height = 600,width = 500,color_discrete_sequence = px.colors.sequential.Rainbow)
        st.plotly_chart(fig_top_insur_bar2)

# Top User plot1
def top_user_plot1(df,year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop = True, inplace = True)
    
    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index( inplace = True)
    
    
    fig_top_plot1 = px.bar(tuyg, x = "States", y= "RegisteredUser", color = "Quarter", width = 800, height = 800,
                           color_discrete_sequence= px.colors.sequential.Burgyl, hover_name = "States", title = f"{year} REGISTERED USER")
    st.plotly_chart(fig_top_plot1)

    return tuy

#Top user plot 2
def top_user_plot2(df,state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop = True, inplace = True)
    
    fig_top_plot2 = px.bar(tuys, x = "Quarter", y = "RegisteredUser", title = f"{state.upper()} REGISTERED USER , PINCODE & QUARTER",
                           width = 800, height = 1000, color = "RegisteredUser", hover_data = "Pincodes",
                           color_continuous_scale = px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot2)

#Top chart Transaction Amount
def top_chart_transaction_amount(table_name):
    sqlconn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database = "phonepe_data")
    cursor = sqlconn.cursor()
    
    
    # Top 10
    query1 = f'''select States,sum(Transaction_amount) as Transaction_amount from {table_name} 
                group by States
                order by Transaction_amount desc
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    sqlconn.commit()
    
    df_1 = pd.DataFrame(table_1, columns = ("States", "Transaction_amount"))
    
    col1,col2 = st.columns(2)
    with col1:

        fig_pie_1 = px.pie(data_frame = df_1, names="States", values= "Transaction_amount",
                      width = 425, title= " TOP 10 TRANSACTION AMOUNT",hole=0.3, hover_name= "States")
        st.plotly_chart(fig_pie_1)   
    
    # Bottom 10
    query2 = f'''select States,sum(Transaction_amount) as Transaction_amount from {table_name} 
                group by States
                order by Transaction_amount 
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    sqlconn.commit()
    
    df_2 = pd.DataFrame(table_2, columns = ("States", "Transaction_amount"))
    
    with col2:

        fig_pie_2 = px.pie(data_frame = df_2, names="States", values= "Transaction_amount",
                      width = 500, title= " LEAST 10 TRANSACTION AMOUNT",hole=0.3, hover_name= "States")
        st.plotly_chart(fig_pie_2)

    
    # Average
    query3 = f'''select States,avg(Transaction_amount) as Transaction_amount from {table_name} 
                group by States
                order by Transaction_amount;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    sqlconn.commit()
    
    df_3 = pd.DataFrame(table_3, columns = ("States", "Transaction_amount"))
    
    fig_amount_3 = px.bar(df_3,x='Transaction_amount',y='States',title=" AVERAGE TRANSACTION AMOUNT", orientation = "h",
                          hover_name = "States", color_discrete_sequence=px.colors.sequential.Magenta,height=800, width = 800)
    st.plotly_chart(fig_amount_3)

#Top chart Transaction count
def top_chart_transaction_count(table_name):
    sqlconn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database = "phonepe_data")
    cursor = sqlconn.cursor()
    
    
    # Top 10
    query1 = f'''select States,sum(Transaction_count) as Transaction_count from {table_name} 
                group by States
                order by Transaction_count desc
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    sqlconn.commit()
    
    df_1 = pd.DataFrame(table_1, columns = ("States", "Transaction_count"))

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_3 = px.pie(data_frame = df_1, names="States", values= "Transaction_count",
                        width = 425, title= "TOP 10 TRANSACTION COUNT",hole=0.3)
        st.plotly_chart(fig_pie_3)
    
    # Bottom 10
    query2 = f'''select States,sum(Transaction_count) as Transaction_count from {table_name} 
                group by States
                order by Transaction_count 
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    sqlconn.commit()
    
    df_2 = pd.DataFrame(table_2, columns = ("States", "Transaction_count"))

    with col2:
        fig_pie_4 = px.pie(data_frame = df_2, names="States", values= "Transaction_count",
                        width = 500, title= "LEAST 10 TRANSACTION COUNT",hole=0.3)
        st.plotly_chart(fig_pie_4)
      
    # Average
    query3 = f'''select States,avg(Transaction_count) as Transaction_count from {table_name} 
                group by States
                order by Transaction_count;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    sqlconn.commit()
    
    df_3 = pd.DataFrame(table_3, columns = ("States", "Transaction_count"))
  
    fig_amount_3 = px.bar(df_3,x='Transaction_count',y='States',title="AVERAGE TRANSACTION COUNT", orientation = "h",
                          hover_name = "States", color_discrete_sequence=px.colors.sequential.Magenta,height=800, width = 800)
    st.plotly_chart(fig_amount_3)

# Top chart Registered user
def top_chart_registered_user(table_name, state):
    sqlconn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database = "phonepe_data")
    cursor = sqlconn.cursor()
    
    
    # Top 10
    query1 = f'''select Districts, sum(RegisteredUser) as RegisteredUser from {table_name}
                where States= '{state}'
                group by Districts
                order by Registereduser desc
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    sqlconn.commit()
    
    df_1 = pd.DataFrame(table_1, columns = ("Districts", "RegisteredUser"))
    
    col1,col2 = st.columns(2)
    with col1: 
        fig_amount_1 = px.bar(df_1,x='Districts',y='RegisteredUser',title="TOP 10 REGISTERED USER", hover_name = "Districts",
                            color_discrete_sequence=px.colors.sequential.Sunsetdark_r,height=500, width = 500)
        st.plotly_chart(fig_amount_1)
        
    # Bottom 10
    query2 = f'''select Districts, sum(RegisteredUser) as RegisteredUser from {table_name}
                where States= '{state}'
                group by Districts
                order by Registereduser
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    sqlconn.commit()
    
    df_2 = pd.DataFrame(table_2, columns = ("Districts", "RegisteredUser"))
    
    with col2:
        fig_amount_2 = px.bar(df_2,x='Districts',y='RegisteredUser',title="LEAST 10 REGISTERED USER", hover_name = "Districts",
                            color_discrete_sequence=px.colors.sequential.Sunsetdark,height=500, width = 500)
        st.plotly_chart(fig_amount_2)
    
        # Average
    query3 = f'''select Districts, avg(RegisteredUser) as RegisteredUser from {table_name}
                where States= '{state}'
                group by Districts
                order by Registereduser;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    sqlconn.commit()
    
    df_3 = pd.DataFrame(table_3, columns = ("Districts", "RegisteredUser"))
    
    fig_amount_3 = px.bar(df_3,x='RegisteredUser',y='Districts',title="AVERAGE REGISTERED USER", orientation = "h",
                          hover_name = "Districts", color_discrete_sequence=px.colors.sequential.Magenta,height=500, width = 800)
    st.plotly_chart(fig_amount_3)

#Top Chart App Opens
def top_chart_app_opens(table_name, state):
    sqlconn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database = "phonepe_data")
    cursor = sqlconn.cursor()
    
    
    # Top 10
    query1 = f'''select Districts, sum(AppOpens) as AppOpens from {table_name}
                where States= '{state}'
                group by Districts
                order by AppOpens desc
                limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    sqlconn.commit()
    
    df_1 = pd.DataFrame(table_1, columns = ("Districts", "AppOpens"))

    col1,col2 = st.columns(2)
    with col1:  
        fig_amount_1 = px.bar(df_1,x='Districts',y='AppOpens',title="TOP 10 APP OPENS", hover_name = "Districts",
                            color_discrete_sequence=px.colors.sequential.Sunsetdark_r,height=500, width = 500)
        st.plotly_chart(fig_amount_1)
    
    
    # Bottom 10
    query2 = f'''select Districts, sum(AppOpens) as AppOpens from {table_name}
                where States= '{state}'
                group by Districts
                order by AppOpens
                limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    sqlconn.commit()
    
    df_2 = pd.DataFrame(table_2, columns = ("Districts", "AppOpens"))
    
    with col2:
        fig_amount_2 = px.bar(df_2,x='Districts',y='AppOpens',title="LEAST 10 APP OPENS", hover_name = "Districts",
                            color_discrete_sequence=px.colors.sequential.Sunsetdark,height=500, width = 500)
        st.plotly_chart(fig_amount_2)
    
    
    # Average
    query3 = f'''select Districts, avg(AppOpens) as AppOpens from {table_name}
                where States= '{state}'
                group by Districts
                order by AppOpens;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    sqlconn.commit()
    
    df_3 = pd.DataFrame(table_3, columns = ("Districts", "AppOpens"))
    
    fig_amount_3 = px.bar(df_3,x='AppOpens',y='Districts',title="AVERAGE APP OPENS", orientation = "h",
                          hover_name = "Districts", color_discrete_sequence=px.colors.sequential.Magenta,height=500, width = 800)
    st.plotly_chart(fig_amount_3)


#Top chart top_user
def top_chart_registered_user1(table_name):
    sqlconn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database = "phonepe_data")
    cursor = sqlconn.cursor()
    
    
    # Top 10
    query1 = f'''select States, sum(RegisteredUser) as RegisteredUser from {table_name}
                    group by States
                    order by RegisteredUser desc
                    limit 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    sqlconn.commit()
    
    df_1 = pd.DataFrame(table_1, columns = ("States", "RegisteredUser"))

    col1,col2 = st.columns(2) 
    with col1:   
        fig_amount_1 = px.bar(df_1,x='States',y='RegisteredUser',title="TOP 10 REGISTERED USER", hover_name = "States",
                            color_discrete_sequence=px.colors.sequential.Sunsetdark_r,height=500, width = 500)
        st.plotly_chart(fig_amount_1)
    
    
    # Bottom 10
    query2 = f'''select States, sum(RegisteredUser) as RegisteredUser from {table_name}
                    group by States
                    order by RegisteredUser 
                    limit 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    sqlconn.commit()
    
    df_2 = pd.DataFrame(table_2, columns = ("States", "RegisteredUser"))

    with col2:
        fig_amount_2 = px.bar(df_2,x='States',y='RegisteredUser',title="LEAST 10 REGISTERED USER", hover_name = "States",
                            color_discrete_sequence=px.colors.sequential.Sunsetdark,height=500, width = 500)
        st.plotly_chart(fig_amount_2)
    
    
    # Average
    query3 = f'''select States, avg(RegisteredUser) as RegisteredUser from {table_name}
                    group by States
                    order by RegisteredUser;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    sqlconn.commit()
    
    df_3 = pd.DataFrame(table_3, columns = ("States", "RegisteredUser"))
    
    fig_amount_3 = px.bar(df_3,x='RegisteredUser',y='States',title="AVERAGE REGISTERED USER", orientation = "h",
                          hover_name = "States", color_discrete_sequence=px.colors.sequential.Magenta,height=500, width = 800)
    st.plotly_chart(fig_amount_3)



#streamlit part
st.set_page_config(layout="wide")
st.title(":blue[PHONEPE DATA VISUALIZATION]")

with st.sidebar:
    select = option_menu("Main Menu",["Home","Data Exploration","Top Transactions"])

if select == "Home":
    st.subheader("Phonepe")
    col1,col2 = st.columns(2)
    with col1:
        st.write("""
                PhonePe is a digital payment platform in India that allows users to make seamless 
                 mobile payments, money transfers, and utility bill payments.
                 Launched in December 2015, PhonePe has grown to become one of the leading digital payment apps in the country.
                 PhonePe is a digital wallet payment method used by consumers to pay for mobile recharges, e-commerce orders, utility bill payments, travel, and more.
                 Customers can use it to recharge prepaid and postpaid mobile phones, pay bills online, and even book movie tickets.
                """)
    with col2:
        st.image(Image.open(r"C:\Users\Mohana Priya\Desktop\Phonepe\phonepe1.jpg"))
    
    st.markdown(" ")
    col3,col4 = st.columns(2)
    with col3:
        st.image(Image.open(r"C:\Users\Mohana Priya\Desktop\Phonepe\Phonepe2.png"))

    with col4:
        st.subheader("Key Features")
        st.write("""
                - **Mobile Recharge**: Users can recharge their mobile phones, DTH connections, and data cards.
                - **Bill Payments**: PhonePe supports payments for various utility bills, including electricity, water, gas, and more.
                - **Money Transfer**: Send and receive money directly from your bank account to anyone else’s bank account in India.
                - **Insurance**: PhonePe offers options to buy and manage insurance policies for health, car, and more.
                """)
       
    st.video(r"C:\Users\Mohana Priya\Desktop\Phonepe\Phonepe_Ad.mp4")
    st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

elif select == "Data Exploration":
    tab1,tab2,tab3 = st.tabs(["Aggregated","Map","Top"])
    
    with tab1:
        method = st.radio("Select the method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])
        if method == "Insurance Analysis":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Aggregated_insurance["Years"].min(),Aggregated_insurance["Years"].max(),Aggregated_insurance["Years"].min())
            trans_y = Transaction_amount_count_Y(Aggregated_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter",trans_y["Quarter"].min(),trans_y["Quarter"].max(),trans_y["Quarter"].min())
            Transaction_amount_count_Y_Q(trans_y, quarters)
        
        elif method == "Transaction Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Aggregated_transaction["Years"].min(),Aggregated_transaction["Years"].max(),Aggregated_transaction["Years"].min())
            aggre_trans_trans_y = Transaction_amount_count_Y(Aggregated_transaction, years)


            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", aggre_trans_trans_y["States"].unique())
            aggr_trans_Transaction_type(aggre_trans_trans_y,states)  

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter",aggre_trans_trans_y["Quarter"].min(),aggre_trans_trans_y["Quarter"].max(),aggre_trans_trans_y["Quarter"].min())
            Aggr_trans_trans_y_Q = Transaction_amount_count_Y_Q(aggre_trans_trans_y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State ", Aggr_trans_trans_y_Q["States"].unique())

            aggr_trans_Transaction_type(Aggr_trans_trans_y_Q,states)  

        elif method == "User Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year ",Aggregated_user["Years"].min(),Aggregated_user["Years"].max(),Aggregated_user["Years"].min())
            Aggre_user_y = Aggre_user_plot1(Aggregated_user, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter",Aggre_user_y["Quarter"].min(),Aggre_user_y["Quarter"].max(),Aggre_user_y["Quarter"].min())
            Aggre_user_y_q = Aggre_user_plot2(Aggre_user_y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", Aggre_user_y_q["States"].unique())
            Aggre_user_plot3(Aggre_user_y_q,states)

    with tab2:
        method1 = st.radio("Select the method",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])
        
        if method1 == "Map Insurance Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Map_insurance["Years"].min(),
                                  Map_insurance["Years"].max(),Map_insurance["Years"].min(),
                                  key="unique_year_slider")
            map_insur_tac_y = Transaction_amount_count_Y(Map_insurance, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", map_insur_tac_y["States"].unique(),key="unique_state_slider")
            Map_insur_District(map_insur_tac_y,states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter ",map_insur_tac_y["Quarter"].min(),map_insur_tac_y["Quarter"].max(),map_insur_tac_y["Quarter"].min())
            map_insur_tac_y_Q = Transaction_amount_count_Y_Q(map_insur_tac_y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State  ", map_insur_tac_y_Q["States"].unique())
            Map_insur_District(map_insur_tac_y_Q,states)

        elif method1 == "Map Transaction Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year ",Map_transaction["Years"].min(),
                                  Map_transaction["Years"].max(),Map_transaction["Years"].min())
            map_trans_tac_y = Transaction_amount_count_Y(Map_transaction, years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State  ", map_trans_tac_y["States"].unique())
            Map_insur_District(map_trans_tac_y,states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter ",map_trans_tac_y["Quarter"].min(),map_trans_tac_y["Quarter"].max(),map_trans_tac_y["Quarter"].min())
            map_trans_tac_y_Q = Transaction_amount_count_Y_Q(map_trans_tac_y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox(" Select the State ", map_trans_tac_y_Q["States"].unique())
            Map_insur_District(map_trans_tac_y_Q,states)

        elif method1 == "Map User Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year. ",Map_user["Years"].min(),
                                  Map_user["Years"].max(),Map_user["Years"].min())
            map_user_Y = map_user_plot1(Map_user, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter. ",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot2(map_user_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State..", map_user_Y_Q["States"].unique())
            map_user_plot3(map_user_Y_Q,states)


    with tab3:
        method3 = st.radio("Select the method",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])
        if method3 == "Top Insurance Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Top_insurance["Years"].min(),
                                  Top_insurance["Years"].max(),Top_insurance["Years"].min(),
                                  key="unique_year1_slider")
            top_insur_tac_y = Transaction_amount_count_Y(Top_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State...", top_insur_tac_y["States"].unique())
            top_insurance_plot1(top_insur_tac_y,states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter.",top_insur_tac_y["Quarter"].min(),top_insur_tac_y["Quarter"].max(),top_insur_tac_y["Quarter"].min())
            top_insur_tac_y_Q = Transaction_amount_count_Y_Q(top_insur_tac_y, quarters)

        elif method3 == "Top Transaction Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Top_transaction["Years"].min(),
                                  Top_transaction["Years"].max(),Top_transaction["Years"].min(),
                                  key="unique_year2_slider")
            top_tran_tac_y = Transaction_amount_count_Y(Top_transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State...", top_tran_tac_y["States"].unique())
            top_insurance_plot1(top_tran_tac_y,states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter ",top_tran_tac_y["Quarter"].min(),top_tran_tac_y["Quarter"].max(),top_tran_tac_y["Quarter"].min())
            top_tran_tac_y_Q = Transaction_amount_count_Y_Q(top_tran_tac_y, quarters)


        elif method3 == "Top User Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Top_user["Years"].min(),
                                  Top_user["Years"].max(),Top_user["Years"].min(),
                                  key="unique_year3_slider")
            top_user_y = top_user_plot1(Top_user, years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State...", top_user_y["States"].unique())
            top_user_plot2(top_user_y,states)

elif select == "Top Transactions":
    question = st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users 0f Top User"])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":
         
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
 
    elif question == "6. Transaction Amount and Count of Top Transaction":
         
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered users of Map User":
        
        col1,col2 = st.columns(2)
        with col1:
            states = st.selectbox("Select the State",Map_user["States"].unique()) 
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_user", states)  

    elif question == "9. App opens of Map User":
        
        col1,col2 = st.columns(2)
        with col1:
            states = st.selectbox("Select the State",Map_user["States"].unique()) 
        st.subheader("APP OPENS")
        top_chart_app_opens("map_user", states)

    elif question == "10. Registered users 0f Top User":
        
        st.subheader("REGISTERED USER")
        top_chart_registered_user1("top_user")