
# This is the api for the project integrated with another external api from the amazon services 
# required packages for the products Flask web api framework

# import flask library
from flask import Flask, redirect, render_template, request
import requests

# creating an instance from the Flask class
server_api = Flask(__name__)

server_api.config['DEBUG'] = True
server_api.config['FLASK_APP'] = 'wsgi.py'

# route that redirects to the home or main page
@server_api.route('/')
@server_api.route('/amazon_price_api/home', methods = ["POST", "GET"])
def home_pag():
    if request.method == "POST":
        product_name = request.form['product_name']
        return redirect("/amazon_price_api/products?product_name={0}".format(product_name))
    return render_template('home.html')


@server_api.route('/amazon_price_api/products')
def products_page():
    product_name = request.args.get('product_name')

    # connecting to the external api from rapid_Apis
    url = "https://pricejson-amazon.p.rapidapi.com/pricejson/search"

    # query string in the url fetches the details of the product from the amazon server
    # e.g: http://127.0.0.1:5000/amazon_price_api/products?product_name=airpod/
    querystring = {"q":"{0}".format(product_name)}

    headers = {
	    "x-rapidapi-key": "acaa9ea20emsh0d4ad91ab123d9ap1974e2jsnaf847876441b",
	    "x-rapidapi-host": "pricejson-amazon.p.rapidapi.com"
    }

    ## -> gets response from the server and displays response
    response = requests.get(url, headers=headers, params=querystring)

    context = {"product_name": product_name,
               "products": response.json()["products"]}

    return render_template('product_page.html', context=context)

# using this file as the running point of the server
if __name__ == "__main__":
    server_api.run()
