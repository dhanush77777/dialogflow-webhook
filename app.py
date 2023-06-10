from flask import Flask, render_template, request
from appwrite.client import Client
from appwrite.services.databases import Databases
from flask import Flask ,request , jsonify
from elasticsearch import Elasticsearch
from werkzeug.middleware.profiler import ProfilerMiddleware
import pickle
import pandas as pd
app=Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    request_data = request.get_json()
    intent = request_data['queryResult']['intent']['displayName']

    if intent == 'wismo':
        order_id = request_data['queryResult']['parameters']['awb_number']


        # Query the database to retrieve the order status based on the orderId
        order_status = query_order_status_from_database(order_id)

        # Format the response
        #order_status=list(order_status)
        # Send the response back to Dialogflow
        response = {
    "fulfillmentText": "your order status is {}".format(order_status),
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "your order status is {}".format(order_status)
          ]
        }
      }
    ],
    "source": "example.com",
    "payload": {
      "google": {
        "expectUserResponse": "true",
        "richResponse": {
          "items": [
            {
              "simpleResponse": {
                "textToSpeech": "this is a simple response"
              }
            }
          ]
        }
      },
      "facebook": {
        "text": "Hello, Facebook!"
      },
      "slack": {
        "text": "This is a text response for Slack."
      }
    }
  }
        return jsonify(response)

    return jsonify({})  # Return an empty response for other intents

# Function to query the order status from the database
def query_order_status_from_database(order_id):
    # Code to connect to your database and retrieve the order status based on the orderId
    # Replace this with your actual implementation
    # Example:
  
    client = Client()
    client.set_endpoint('https://cloud.appwrite.io/v1')  # Replace with your Appwrite endpoint
    client.set_project('646f96814ce0bd792d15')  # Replace with your Appwrite project ID
    client.set_key('6a759c9a8af2d7375898ab12267f78dd571da99ba41508369770c1617dde56198ad379536f31ab7691dc86d1aef7195e1a2469edbb0faf41a2d720bcbb397643bc783aee078310d2d581da685e9f61e784b7694bdb090b361033c5d53fc0e11249c58db5e2d0b138bc0b3e25ef9485d9dfd4102909f0ec09d84f2b400bfa6aa5')  
    database_id="646f96a60d5767f59620"
    database = Databases(client)
    # Fetch order details from the database
    collection_id = '648061a485127fc18474'  # Replace with your collection ID
    document = database.get_document(database_id,collection_id, order_id)

    if document:
        status = document['order_status']
        return status
    else:
        return None




product_dict = pickle.load(open('product_dict.pkl','rb'))
df=pd.DataFrame(product_dict)
df.head()
similarity = pickle.load(open('similarity.pkl','rb'))
def recommend(product):
    index = df[df['products'] == product].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    a=[]
    for i in distances[1:6]:
        a.append(df.iloc[i[0]].products)
    return a

@app.route("/recommend",methods=["POST"])
def rec():
    req=request.get_json()
    product=req["product_name"]
    return jsonify({"recommended list":recommend(product)})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int("3000"),debug=True)




