from flask import Flask, render_template, request, redirect, flash, url_for, session

import model

app = Flask(__name__)


app.config['SECRET_KEY'] ="adsflahsfdlkasdfh"

@app.route('/')
def index():
	posts = model.fetch_post()
	
	return render_template('index.html', title='Home', active=session.get('loged_in', None), uname=session.get('username', None), posts=posts)
	
	
@app.route('/login')
def login():
	if session.get('loged_in', None):
		return redirect(url_for('dashboard'))
	else:
		return render_template('login.html', title='Login')
	
@app.route('/login_check', methods=['POST'])
def login_check():
	usr = request.form.get('usrname')
	pas = request.form.get('pass')
	
	
	
	if (usr is None) or (len(usr)<3) and (pas is None) or (len(pas)<6):
		flash('Invalid usrname and password!')
		return redirect(url_for('login'))
	
		
	user_data = model.fetch_usr(usr)
	
	if user_data == None:
		flash('Username does not exists.')
		return redirect(url_for('login'))
	
	if user_data[3]!=usr or user_data[4] !=pas:
		flash('Username and password not matched!')
		return redirect(url_for('login'))
	
	else:
		session['loged_in']=True
		session['username'] = user_data[3]
		session['usr_data']=user_data
		session['first_name']= user_data[1]
		session['last_name']= user_data[2]
		return redirect(url_for('change', to=0))


curr=0
up={}
@app.route('/dashboard')
def dashboard():
	usr_post_info={}
	if curr==1:
		usr_post_info = model.fetch_usr_post(session.get('username'))
	return render_template('dashboard.html', title="Dashboard", u=session.get('usr_data', None), curr=curr, posts=usr_post_info, up=up)
	

	
@app.route('/change/<int:to>')
def change(to):
	global curr
	curr=to
	return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('loged_in', None)
	curr=0
	return redirect(url_for('index'))



@app.route('/register', methods=['POST','GET'])
def register():
	
	if request.method == 'GET':
		return render_template('registraton.html')
	else:
		uf_name = request.form.get('first_name', None)
		ul_name = request.form.get('last_name', None)
		username = request.form.get('username', None)
		password = request.form.get('password', None)
		password_re = request.form.get('password_re', None)
		
		
		if len(uf_name)==0:
			flash('Invalid First Name.')
			return redirect(url_for('register'))
		
		if len(ul_name)==0:
			flash('Invalid Last Name.')
			return redirect(url_for('register'))
		if len(username) < 3:
			flash('Invalid Username.')
			return redirect(url_for('register'))
		if len(password) < 6:
			flash('Password length at least 6.')
			return redirect(url_for('register'))
		if password != password_re:
			flash('Password does not match.')
			return redirect(url_for('register'))
			
		status = model.insert_usr_data('users', (uf_name, ul_name, username, password))
		
		if status:
			return redirect(url_for('dashboard'))
		flash('Error, Try again later!')
		return redirect(url_for('register'))


@app.route('/publish', methods=['POST'])
def publish():
	title = request.form.get('post-text', None)
	description = request.form.get('post-content')
	author = session['username']
	

	
	if len(title) == 0:
		flash("You can't post without a title!")
		return redirect('dashboard')
	
	res = model.put_post((title, description, author))
	if res:
		flash("Post publish successfully!")
		return redirect('dashboard')
	flash("Some error occurred, please try again later!")
	return redirect('dashboard')

@app.route('/delete', methods=['POST'])
def delete():
	id = request.form.get('delete')
	model.delete_post(id)
	return redirect(url_for('change', to=1))
	
@app.route('/update', methods=['POST'])
def update():
	id = request.form.get('update')
	posts = model.fetch_post()
	
	global up
	for post in posts:
		#return str(type(id))
		if str(post['id'])==id:
			up['id']=post['id']
			up['title'] = post['title']
			up['des'] = post['description']
	return redirect(url_for('change', to=3))



@app.route('/update_profile', methods=['POST'])
def profile_update():
	new_f_name = request.form.get('f_name')
	new_l_name = request.form.get('l_name')
	
	curr_pass = request.form.get('cur_pass', None)
	new_pass = request.form.get('new_pass', None)
	new_pass_aga = request.form.get('new_pass_aga', None)
	
	if len(curr_pass)==0:
		curr_pass=None
	
	if new_f_name != session['first_name'] or new_l_name != session['last_name']:

		if curr_pass == None:
			k=	model.update_profile(new_f_name, new_l_name, session['usr_data'][4], session['username'])
		else:
			k=model.update_profile(new_f_name, new_l_name, new_pass, session['username'])
	elif curr_pass != None:
		if session['usr_data'][4] == curr_pass and new_pass==new_pass_aga:
			k=model.update_profile(new_f_name, new_l_name, new_pass, session['username'])
		else:
			pass
		
	update_session()
	return redirect(url_for('change', to=2))


def update_session():
	user_data = model.fetch_usr(session['username'])
	
	session['usr_data']=user_data
	session['first_name']= user_data[1]
	session['last_name']= user_data[2]


@app.route('/up_date', methods=['POST'])
def up_date():
	title = request.form.get('post-text', None)
	description = request.form.get('post-content')
	id =  request.form.get('sub')
	
	if len(title) == 0:
		#flash("You can't post without a title!")
		return redirect('dashboard')
	
	res = model.up_post((title, description, int(id)))
	return redirect(url_for('change', to=1))
	
if __name__=='__main__':
	app.run(debug=True)

