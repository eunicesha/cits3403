from datetime import datetime, timezone
from email.policy import default
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True) #so.Mapped to tell python what data type is used in the column 
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) # so.mapped_column to define additional settings 

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class GameResults(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index = True)
    user_id2: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index = True)
    user_choice: so.Mapped[str] = so.mapped_column(sa.String(8))
    user_choice2: so.Mapped[str] = so.mapped_column(sa.String(8))
    result: so.Mapped[str] = so.mapped_column(sa.String(20))
    

class Challenge(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    accepted: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                                index=True)
    challenger: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                                  index=True)
    status = db.Column(db.String(50), default='Open')


    
