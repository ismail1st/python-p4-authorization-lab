#!/usr/bin/env python3

import pytest
from app import app
from models import db, User, Article

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture
def setup_database():
    """Create tables and seed database before each test."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Seed data if not exists
        if not User.query.first():
            from random import randint
            from faker import Faker
            fake = Faker()
            
            # Create users
            users = []
            usernames = []
            for i in range(25):
                username = fake.first_name()
                while username in usernames:
                    username = fake.first_name()
                usernames.append(username)
                user = User(username=username)
                users.append(user)
            db.session.add_all(users)
            
            # Create articles
            articles = []
            for i in range(100):
                content = fake.paragraph(nb_sentences=8)
                preview = content[:25] + '...'
                article = Article(
                    author=fake.name(),
                    title=fake.sentence(),
                    content=content,
                    preview=preview,
                    minutes_to_read=randint(1,20),
                    is_member_only=bool(randint(0, 2))  # 1 True, 2 False
                )
                articles.append(article)
            db.session.add_all(articles)
            
            db.session.commit()
        
        yield
        
        # Cleanup after test
        db.session.remove()
