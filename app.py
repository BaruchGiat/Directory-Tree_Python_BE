from flask import Flask, make_response
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DB_USER:DB_PASS@DB_URL:PORT/DB_NAME'

db = SQLAlchemy(app)

class Nodes(db.Model):
    __tablename__ = 'Nodes'
    node_id = db.Column(db.Integer,primary_key = True)
    node_name = db.Column(db.String(50))


class Edges(db.Model):
        __tablename__ = 'Edges'
        id = db.Column(db.Integer,primary_key = True)
        parent_id = db.Column(db.Integer, db.ForeignKey('Nodes.node_id'))
        child_id = db.Column(db.Integer, db.ForeignKey('Nodes.node_id'))

@app.route('/get-sub-nodes/<tag>')
def get_sub_nodes(tag):
     node = Nodes.query.filter_by(node_name=tag).first()
     array = []
     for sub_node in db.session.query(Nodes.node_name).select_from(Nodes).join(Edges,Nodes.node_id == Edges.child_id).filter(Edges.parent_id == node.node_id).all():
        array.append(sub_node.node_name)

     return _corsify_actual_response(jsonify(array))

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response