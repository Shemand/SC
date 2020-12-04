import os
import sys

from flask import Flask, session, redirect, url_for

sys.path.append("/home/shemand/PycharmProjects/ff/sc_http")

app = Flask(__name__, static_folder='templates/static')
# app.config.from_object('config')

http_server = app
