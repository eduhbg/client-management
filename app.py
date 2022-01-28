from crypt import methods
from datetime import datetime

from flask import Flask
from flask import render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Client {self.id}>'

@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        client_name = request.form['name']
        client_address = request.form['address']  
        client_phone = request.form['phone']
        new_client = Client(name=client_name, address=client_address, phone=client_phone)

        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding your client.'

    else:
        clients = Client.query.order_by(Client.date_created).all()
        return render_template('index.html', clients=clients)


@app.route('/delete/<int:id>')
def delete(id):
    client_to_delete = Client.query.get_or_404(id)

    try:
        db.session.delete(client_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this client.'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    client = Client.query.get_or_404(id)

    if request.method == 'POST':
        client.name = request.form['name']
        client.address = request.form['address']
        client.phone = request.form['phone']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating this client.'

    else:
        return render_template('update.html', client=client)

if __name__ == '__main__':
    app.run(debug=True)