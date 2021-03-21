from flask import Blueprint, render_template, request, url_for, redirect

staticpages = Blueprint('staticpages', __name__, template_folder='templates',static_folder='static')

@staticpages.route('/about')
def about():
    return render_template('about.html')

@staticpages.route('/faq')
def faq():
    return render_template('faq.html')