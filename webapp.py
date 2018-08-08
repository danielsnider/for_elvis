

@app.route('/')
def hello():
    html == """<form action="/request" method="post">
        <input type="text" name="projectFilepath">
        <input type="submit">
    </form>"""
    return html

@app.route('/request', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
