@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')
    else:
        return redirect('/blogs')

    

#blogs.html?    
<a href="/ind_post?id={{user.id}}">Written by:{{user.email}}</a>