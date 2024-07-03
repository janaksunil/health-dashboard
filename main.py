import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data
data = pd.read_excel('Final-GPT.xlsx')

# Function to create a line plot for each test
def plot_test(test_row):
    test_name = test_row['Test']
    results = {'December': test_row['Result December'], 'June 2024': test_row['Result June 2024']}
    reference_range = test_row['Reference Range (number)'].split('-') if '-' in test_row['Reference Range (number)'] else [0, 0]
    risk_score = test_row['Risk Score']
    description = test_row['What does this test mean?']

    # Determine color based on risk score
    if risk_score < 3:
        score_color = 'green'
    elif risk_score < 6:
        score_color = 'yellow'
    else:
        score_color = 'red'

    # Create figure
    fig = go.Figure()

    # Add trace for results
    fig.add_trace(go.Scatter(x=list(results.keys()), y=list(results.values()), mode='lines+markers', name='Results'))

    # Add reference range lines
    fig.add_trace(go.Scatter(x=list(results.keys()), y=[float(reference_range[0])]*2,
                             mode='lines', name='Reference Min', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=list(results.keys()), y=[float(reference_range[1])]*2,
                             mode='lines', name='Reference Max', fill='tonexty', line=dict(color='green', dash='dash')))

    for date, value in results.items():
        if float(value) < float(reference_range[0]) or float(value) > float(reference_range[1]):
            fig.add_annotation(x=date, y=value, text="Out of range", showarrow=True, arrowhead=1, arrowsize=2, arrowcolor="red", font=dict(color="red"))

    # Layout adjustments
    # Layout adjustments
    fig.update_layout(
    title={
        'text': f"<b>{test_name}</b> <br><span style='font-size: 12px;'>{description}</span>",
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    annotations=[
        dict(
            x=1,
            y=2,  # Adjust this as needed
            xref='paper',
            yref='paper',
            text=f"<b><span style='color:{score_color};'>Risk Score: {risk_score}</span></b>",
            showarrow=False,
            font=dict(size=12),  # Adjust font size as needed
            align='right'
        )
    ],
    
    xaxis_title='Date',
    yaxis_title='Value',
    font=dict(
        family="Helvetica, Arial, sans-serif",
        size=14,
        color="black"
    ),
    autosize=False,
    width=500,
    height=300,
    margin=dict(l=50, r=50, b=100, t=100, pad=0)
)


    return fig

# Display all plots in a grid layout
st.title('Blood Dashboard')
cols = st.columns(2)

for index, row in data.iterrows():
    fig = plot_test(row)
    st.plotly_chart(fig, use_container_width=True)
