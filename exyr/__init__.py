import jinja2
from flask import Flask, render_template
from flaskext import flatpages


app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined

pages = flatpages.FlatPages(app)


@app.route('/')
def index():
    articles = (p for p in pages
                if all(m in p.meta for m in ['published', 'title']))
    latest = sorted(articles, reverse=True, key=lambda p: p.meta['published'])
    return render_template('articles.html', articles=latest)


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    return render_template(template, page=page)
    

def run():
    app.before_request(pages.reset)
    app.run(debug=True)
