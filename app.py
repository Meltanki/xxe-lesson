from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from lxml import etree

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'

# Initialize db
db = SQLAlchemy(app)


# Create db model
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())

    # Create a function to return a string
    @property
    def __repr__(self):
        return f"Item('{self.title}', '{self.description}')"


@app.route("/", methods=['GET', 'POST'])
@app.route("/items", methods=['GET', 'POST'])
def items():
    if request.method == "POST":
        try:
            f = request.files['file']
            doc = etree.parse(f, etree.XMLParser())
            root = doc.getroot()
            item_title, item_description = root.getchildren()[0].text, root.getchildren()[1].text
            new_item = Items(title=item_title, description=item_description)

            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except Exception as error:
            return error
    else: # method == "GET"
        item_list = Items.query.order_by(Items.created)
        return render_template('items.html', item_list=item_list)


if __name__ == "__main__":
    print("Starting XXE App")

    # Initialize a new db and populate with some Items
    db.drop_all()
    db.create_all()
    first_item = Items(title='Title1', description='Description number One!')
    second_item = Items(title='Title2', description='Description number Two!')
    db.session.add(first_item)
    db.session.add(second_item)
    db.session.commit()

    app.run(debug=True)
