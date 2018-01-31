#blogs.html?    
#<a href="/ind_post?id={{user.id}}">Written by:{{user.email}}</a>

# @app.route('/allusers', methods=['POST', 'GET'])
# def all_users():
#     owner = User.query.filter_by(email=session['email']).first()
#     blogid = request.args.get('id')
#     if blogid:
#         blogid = int(blogid)
#         blogs = Blog.query.get(blogid)
#         return render_template('index.html', blogs=blogs)

#     blogs = Blog.query.filter_by(owner=owner).all()
#     return render_template('index.html',title="All Users", 
#         blogs=blogs)