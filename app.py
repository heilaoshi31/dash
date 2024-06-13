from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Updated connection string with URL-encoded password and increased timeout
client = MongoClient('mongodb+srv://heilaoshi31:Steven040506@cluster0.9fkg9lz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', tls=True, tlsAllowInvalidCertificates=True
)
db = client['financial_data']
collection = db['apple_stock_2023']

@app.route('/')
def home():
    return "<h1>Welcome to the Financial Data App</h1><p>Navigate to /fetch_data to query data.</p>"

@app.route('/test_mongo')
def test_mongo():
    try:
        document = collection.find_one()
        return jsonify({"status": "success", "document": document})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/fetch_data', methods=['GET', 'POST'])
def fetch_data():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Convert dates to ISO format for querying MongoDB
        try:
            start_date_iso = datetime.strptime(start_date, '%Y-%m-%d').isoformat()
            end_date_iso = datetime.strptime(end_date, '%Y-%m-%d').isoformat()
        except ValueError as e:
            logging.error(f"Invalid date format: {e}")
            return f"Invalid date format: {e}"

        query = {
            'Date': {
                '$gte': start_date_iso,
                '$lte': end_date_iso
            }
        }
        
        try:
            logging.info("Executing query...")
            data = list(collection.find(query))
            logging.info(f"Query executed successfully, retrieved {len(data)} records.")
            
            if data:
                df = pd.DataFrame(data)
                fig = px.line(df, x='Date', y='Close', title='Apple Stock Prices')
                graph_html = fig.to_html(full_html=False)
                return f"<h1>Apple Stock Prices</h1>{graph_html}"
            else:
                logging.info("No data found for the specified date range.")
                return "No data found for the specified date range."
        except Exception as e:
            logging.error(f"An error occurred while fetching data: {e}")
            return f"An error occurred while fetching data: {e}"
    return '''
        <form method="post">
            Start Date: <input type="date" name="start_date">
            End Date: <input type="date" name="end_date">
            <input type="submit">
        </form>
    '''

# Remove or update routes that reference missing templates and static files
@app.route('/table')
def table():
    return "<h1>Table View</h1><p>This route will be updated later.</p>"

@app.route('/graphs')
def graphs():
    return "<h1>Graphs</h1><p>This route will be updated later.</p>"

@app.route('/interactive_graphs')
def interactive_graphs():
    return "<h1>Interactive Graphs</h1><p>This route will be updated later.</p>"

@app.route('/yahoo_graphs')
def yahoo_graphs():
    return "<h1>Yahoo Graphs</h1><p>This route will be updated later.</p>"

# Comment out or remove routes serving static reports if they don't exist
# @app.route('/reports/<report_name>')
# def serve_report(report_name):
#     return send_from_directory('static', report_name)

if __name__ == '__main__':
    app.run(debug=True)
