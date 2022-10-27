from model import put_post

def test_put_post():
	assert put_post(('hello world', 'description', 'sohan')) == 1
