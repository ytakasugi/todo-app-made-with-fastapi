from controllers import app, index, admin

app.add_api_route('/', index)
app.add_api_route('/admin', admin)