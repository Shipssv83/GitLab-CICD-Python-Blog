import pytest
from app import app, db
from models import User, Post

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используйте in-memory базу для тестов
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Создайте таблицы
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Удалите таблицы после тестов

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_register(client):
    response = client.post('/register', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful!' in response.data

def test_login(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login successful!' in response.data

def test_logout(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out.' in response.data

def test_new_post(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    response = client.post('/new', data={'title': 'Test Post', 'content': 'This is a test post'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Post created successfully!' in response.data
