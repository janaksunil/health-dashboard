import streamlit as st
import pandas as pd
import plotly.graph_objects as go

data = pd.read_excel('Final-GPT.xlsx')

def plot_test(test_row):
    test_name = test_row['Test']
    results = {'December 2023': test_row['Result December'], 'June 2024': test_row['Result June 2024']}
    reference_range = test_row['Reference Range (number)'].split('-') if '-' in test_row['Reference Range (number)'] else [0, 0]
    risk_score = test_row['Risk Score']
    description = test_row['What does this test mean?']


    if risk_score < 3:
        score_color = 'green'
    elif risk_score < 6:
        score_color = 'orange'
    else:
        score_color = 'red'


    # Determine if the June 2024 result is out of the reference range
    out_of_range_june = not (float(reference_range[0]) <= test_row['Result June 2024'] <= float(reference_range[1]))
    ref_color = 'red' if out_of_range_june else 'green'


    # Create figure
    fig = go.Figure()

    # Add trace for results with markers colored based on condition
    marker_colors = ['red' if (key == 'June 2024' and out_of_range_june) else 'blue' for key in results.keys()]
    fig.add_trace(go.Scatter(
        x=list(results.keys()), 
        y=list(results.values()), 
        mode='lines+markers', 
        name='Results',
        line=dict(color='blue'),
        marker=dict(color=marker_colors, size=10)
    ))

    # Add reference range lines with dynamic coloring
    fig.add_trace(go.Scatter(
        x=list(results.keys()), 
        y=[float(reference_range[0])]*2,
        mode='lines', 
        name='Reference Min', 
        line=dict(color=ref_color, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=list(results.keys()), 
        y=[float(reference_range[1])]*2,
        mode='lines', 
        name='Reference Max', 
        fill='tonexty', 
        line=dict(color=ref_color, dash='dash')
    ))

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
                x=0,
                y=2,  
                xref='paper',
                yref='paper',
                text=f"<b><span style='color:{risk_score < 3 and 'green' or (risk_score < 6 and 'orange' or 'red')}';'>Risk Score: {risk_score}</span></b>",
                showarrow=False,
                font=dict(size=12),  
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
