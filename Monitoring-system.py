import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('./predictions.csv')

disease_color_palette = px.colors.qualitative.Plotly
disease_to_color = {disease: color for disease, color in zip(df['Prediction'].unique(), disease_color_palette)}

st.sidebar.title("Monitoring System")

selected_page = st.sidebar.selectbox("Select a Page", ["Request Time Graph", "Diseases by Pincode", "Confidence Line Chart of Predictions"])

st.title("Monitoring System Visualization")

if selected_page == "Request Time Graph":
    st.write('\n\n')
    st.header("Request Time Graph")
    df = pd.read_csv('./predictions.csv')
    fig_time_line = px.line(df, x=df.index, y='Total Time (ms)', title='Request Time Line Plot')
    fig_time_line.update_traces(line=dict(color='blue'))
    fig_time_line.update_layout(
        xaxis_title='Index',
        yaxis_title='Total Time (ms)',
        template='plotly_dark',
    )
    st.plotly_chart(fig_time_line)

    fig_time = px.histogram(df, x='Total Time (ms)', nbins=20, title='Request Time Histogram')
    fig_time.update_traces(marker=dict(color='green'))
    fig_time.update_layout(
        xaxis_title='Total Time (ms)',
        yaxis_title='Count',
        template='plotly_dark',
    )
    st.plotly_chart(fig_time)

elif selected_page == "Diseases by Pincode":
    st.write('\n\n')
    st.header("Diseases by Pincode")
    df = pd.read_csv('./predictions.csv')
    pincode = st.text_input("Enter Pincode", "")
    pincode = int(pincode) if pincode.isdigit() and len(pincode) == 6 else None

    if pincode is not None:
        filtered_data = df[df['Pincode'] == pincode]
        if not filtered_data.empty:
            fig_histogram = px.histogram(filtered_data, x='Prediction', title=f'Diseases for Pincode: {pincode}')
            fig_histogram.update_traces(marker_color='purple')
            fig_histogram.update_layout(
                xaxis_title='Prediction',
                yaxis_title='Count',
                template='plotly_dark',
            )
            st.plotly_chart(fig_histogram)
        else:
            st.info("No data available for the entered pincode.")
    else:
        st.info("Please enter a valid 6-digit numeric pincode.")

elif selected_page == "Confidence Line Chart of Predictions":
    st.write('\n\n')
    st.header("Confidence Line Chart of Predictions")
    df = pd.read_csv('./predictions.csv')
    confidence_fig = px.line(df, x=df.index,y='Confidence', title='Confidence Line Chart')
    confidence_fig.update_traces(marker_color='cyan')
    confidence_fig.update_layout(
        xaxis_title='Index',
        yaxis_title='Confidence',
        template='plotly_dark',
    )
    st.plotly_chart(confidence_fig)
