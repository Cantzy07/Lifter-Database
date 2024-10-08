from flask import request, jsonify
from config import app, db
from models import Lifter
from models import PositionalPoints
from models import Resource
from models import Link
from positionalPointsFactory import PositionalPointsFactory
from io import BytesIO
import numpy as np
from PIL import Image
from KNNTransform import KNNTransform

# http methods for lifters
@app.route("/lifters", methods=["GET"])
def get_lifters():
    # get all lifter data
    lifters = Lifter.query.all()
    json_lifters = list(map(lambda x: x.to_json(), lifters))
    return jsonify({"lifters": json_lifters})

@app.route("/find_matching", methods=["POST"])
def find_matching():
    if 'file' not in request.files:
        return "no file part", 400
    
    file = request.files['file']
    weight = request.form['weight']

    if file.filename == '':
        return "No selected file", 400
    
    frame = Image.open(BytesIO(file.read()))
    frame = np.array(frame)

    lifter_metrics = PositionalPointsFactory.getMetrics(frame, weight)

    data = []
    # get all lifter data
    allLifters = Lifter.query.all()
    # get all metrics data from all lifters and put into a list
    for lifter in allLifters:
        tempArr = KNNTransform.transformData(lifter)
        for metrics in tempArr:
            data.append(metrics)

    most_similar = KNNTransform.findKNN(lifter_metrics, data)

    return jsonify(allLifters[data.index(most_similar)].name)

@app.route("/create_lifter", methods=["POST"])
def create_lifter():
    # get info from the request made
    name = request.form.get("name")
    weight = request.form.get("weight")
    file = request.files["positionalPoints"]

    # if request doesn't have necessary fields return error message
    if not name or not weight or not file:
        return (
            jsonify({"message": "You must include a name, weight, and body metrics"}),
            400,
        )
    if file.filename == '':
        return (
            jsonify({"message": "No selected file"}), 
            400,
        )

    frame = Image.open(BytesIO(file.read()))
    frame = np.array(frame)

    # instantiate new lifter with fields from request
    new_lifter = Lifter(name=name, weight=weight)

    # try catch to add new lifter to database and return error if unsuccessful; add and commit are similar to git commands
    try:
        db.session.add(new_lifter)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Must input a unique name, weight, and a picture"}), 400

    # create metrics from picture
    point = PositionalPointsFactory.create_positional_point(new_lifter.id, frame)
    db.session.add(point)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    # return successful operation code
    return jsonify({"message": "Lifter created!"}), 201


@app.route("/update_lifter/<int:user_id>", methods=["PATCH"])
def update_lifter(user_id):
    # get the user from the db based on user id
    lifter = Lifter.query.get(user_id)

    # if lifter isn't found then return error
    if not lifter:
        return jsonify({"message": "Lifter not found"}), 404

    # update any existing data from the lifter with the new data
    data = request.form.to_dict()
    lifter.name = data.get("name", lifter.name)
    lifter.weight = data.get("weight", lifter.weight)

    # update positional points if provided
    if "positionalPoints" in request.files:
        file = request.files['positionalPoints']

        if file.filename != '':
            # Read the image file directly from memory
            img = Image.open(BytesIO(file.read()))
            img = np.array(img)
            
            # Create and add new positional points
            point = PositionalPointsFactory.create_positional_point(user_id, img)
            db.session.add(point)

    # commit changes
    db.session.commit()
    # return successful update response
    return jsonify({"message": "Lifter updated."}), 200


@app.route("/delete_lifter/<int:user_id>", methods=["DELETE"])
def delete_lifter(user_id):
    # get the user from the db based on user id
    lifter = Lifter.query.get(user_id)

    # if lifter isn't found then return error
    if not lifter:
        return jsonify({"message": "Lifter not found"}), 404

    # delete lifter and commit changes
    db.session.delete(lifter)
    db.session.commit()

    # return successful deletion message
    return jsonify({"message": "Lifter deleted!"}), 200

@app.route("/delete_metrics/<int:user_id>", methods=["DELETE"])
def delete_metrics(user_id):
    # get the user from the db based on user id
    lifter = Lifter.query.get(user_id)

    # if lifter isn't found then return error
    if not lifter:
        return jsonify({"message": "Lifter not found"}), 404

    # Clear existing positional points
    PositionalPoints.query.filter_by(lifter_id=lifter.id).delete()
    db.session.commit()

    # return successful deletion message
    return jsonify({"message": "Lifter deleted!"}), 200

# http methods for resources
@app.route("/resources", methods=["GET"])
def get_resources():
    # get all lifter data
    resources = Resource.query.all()
    json_resources = list(map(lambda x: x.to_json(), resources))
    return jsonify({"resources": json_resources})

@app.route("/create_resource", methods=["POST"])
def create_resource():
    # get info from the request made
    name = request.form.get("name")
    program = request.form.get("program")
    links = request.form.getlist("links")

    # if request doesn't have necessary fields return error message
    if not name:
        return (
            jsonify({"message": "You must include a name, program, and video link"}),
            400,
        )

    # instantiate new lifter with fields from request
    new_resource = Resource(name=name, program=program)

    # try catch to add new lifter to database and return error if unsuccessful; add and commit are similar to git commands
    try:
        db.session.add(new_resource)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Must input a unique name, program, and video link"}), 400
    
    if links:
        for link_url in links:
            if link_url:
                link = Link(link=link_url, resource_id=new_resource.id)
                db.session.add(link)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    # return successful operation code
    return jsonify({"message": "Resource created!"}), 201

@app.route("/update_resource/<int:resource_id>", methods=["PATCH"])
def update_resource(resource_id):
    # get the user from the db based on user id
    resource = Resource.query.get(resource_id)

    # if lifter isn't found then return error
    if not resource:
        return jsonify({"message": "Resource not found"}), 404

    # update any existing data from the lifter with the new data
    data = request.form.to_dict()
    resource.name = data.get("name", resource.name)
    resource.program = data.get("program", resource.program)

    # Check if the new link is different from the existing one
    new_link_value = data.get("link", None)
    if new_link_value:
        # Check if a link already exists for this resource
        existing_link = Link.query.filter_by(resource_id=resource.id).first()

        if existing_link:
            # If the new link is different from the existing one, update it
            if existing_link.link != new_link_value:
                new_link = Link(link=new_link_value, resource_id=resource_id)
                db.session.add(new_link)
        else:
            # If no link exists, create a new one
            new_link = Link(link=new_link_value, resource_id=resource_id)
            db.session.add(new_link)

    # commit changes
    db.session.commit()
    # return successful update response
    return jsonify({"message": "Resource updated."}), 200

@app.route("/delete_resource/<int:resource_id>", methods=["DELETE"])
def delete_resource(resource_id):
    # get the user from the db based on user id
    resource = Resource.query.get(resource_id)

    # if resource isn't found then return error
    if not resource:
        return jsonify({"message": "Resource not found"}), 404

    # delete resource and commit changes
    db.session.delete(resource)
    db.session.commit()

    # return successful deletion message
    return jsonify({"message": "Resource deleted!"}), 200

@app.route("/delete_links/<int:resource_id>", methods=["DELETE"])
def delete_links(resource_id):
    # get the user from the db based on user id
    resource = Resource.query.get(resource_id)

    # if lifter isn't found then return error
    if not resource:
        return jsonify({"message": "Resource not found"}), 404

    # Clear existing positional points
    Link.query.filter_by(resource_id=resource.id).delete()
    db.session.commit()

    # return successful deletion message
    return jsonify({"message": "Links deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
