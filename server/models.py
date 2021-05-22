import os 
import random
import string
import base64
import onetimepass
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.String(100), primary_key=True)
    display_name = db.Column(db.String(100))
    last_online = db.Column(db.DateTime())
    operating_system = db.Column(db.String(100))
    remote_ip = db.Column(db.String(100))
    geolocation = db.Column(db.String(100))
    output = db.Column(db.Text(), default="")
    hostname = db.Column(db.String(100))
    username = db.Column(db.String(100))
  
    def __init__(self, uid):
        self.id = uid
        self.display_name = self.id

    def push_command(self, cmdline):
        cmd = Command()
        cmd.agent = self
        cmd.cmdline = cmdline
        cmd.timestamp = datetime.now()
        db.session.add(cmd)
        db.session.commit()

    def rename(self, new_name):
        self.display_name = new_name
        db.session.commit()

    def is_online(self):
        return (datetime.now() - self.last_online).seconds < 30


class Command(db.Model):
    __tablename__ = 'commands'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agent_id = db.Column(db.Integer(), db.ForeignKey('agents.id'))
    agent = db.relationship('Agent', backref=db.backref('commands', lazy='dynamic'))
    cmdline = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime(), default=datetime.now)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    salt = db.Column(db.String(100))
    last_login_time = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))

    otp_secret = db.Column(db.String(16))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    # ...

    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=2FA-Demo' \
            .format(self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)
