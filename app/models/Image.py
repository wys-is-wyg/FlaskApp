import pyrebase
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class Image():

    def __init__(self):

    def get_latest_images(self):
        self.get_user()
        return (self.user != None)
