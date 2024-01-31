import os
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load sample data for demonstration
monthly_data = pd.read_csv('monthly_average.csv')
five_day_data = pd.read_csv('five_day_average.csv')
one_day_data = pd.read_csv('one_day_average.csv')
weekly_data = pd.read_csv('weekly_average.csv')


@app.route('/plot', methods=['GET'])
def plot():
    chart_type = request.args.get('chart_type')
    print(chart_type)

    if chart_type == 'whole':
        plot_data = monthly_data
        title = 'Monthly Average Plot'
    elif chart_type == 'yearly':
        year = request.args.get('year')
        five_day_data['Timestamp'] = pd.to_datetime(five_day_data['Timestamp'])
        plot_data = five_day_data[five_day_data['Timestamp'].dt.year == int(year)]
        title = f'Five Day Average Plot for {year}'
    elif chart_type == 'monthly':
        year = request.args.get('year')
        month = request.args.get('month')
        one_day_data['Timestamp'] = pd.to_datetime(one_day_data['Timestamp'])
        plot_data = one_day_data[(one_day_data['Timestamp'].dt.year == int(year)) & (one_day_data['Timestamp'].dt.month == int(month))]
        title = f'One Day Average Plot for {year}-{month}'
    elif chart_type == 'period':
        start_year = request.args.get('start_year')
        start_month = request.args.get('start_month')
        end_year = request.args.get('end_year')
        end_month = request.args.get('end_month')
        plot_data = weekly_data[(weekly_data['Timestamp'].dt.year >= int(start_year)) & (weekly_data['Timestamp'].dt.year <= int(end_year)) & 
                                (weekly_data['Timestamp'].dt.month >= int(start_month)) & (weekly_data['Timestamp'].dt.month <= int(end_month))]
        title = f'Weekly Average Plot for {start_year}-{start_month} to {end_year}-{end_month}'

    # Create an interactive plot with hover information
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=plot_data['Timestamp'], y=plot_data['Profit Percentage'], mode='lines+markers', name='Profit Percentage'))

    fig.update_layout(title=title, xaxis_title='Timestamp', yaxis_title='Profit Percentage')

    # Get the HTML div containing the Plotly figure
    plot_html = pio.to_html(fig, full_html=False)

    # Return the response as JSON
    response = {'plot_html': plot_html}
    fig.show()
    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=6000)
