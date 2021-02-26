from flask import request

from . import api
from . import vehicles_model
from .. import db


@api.route('/vehicles', methods=['GET'])
def list_vehicles():
    result = db.session.query(vehicles_model.Vehicle).all()
    return {"items": [vehicle.to_dict() for vehicle in result]}


@api.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = db.session.query(vehicles_model.Vehicle).filter_by(id=vehicle_id).first()
    if vehicle is None:
        return 'Vehicle with id {} not found'.format(vehicle_id), 404
    else:
        return vehicle.to_dict()


@api.route('/vehicles', methods=['POST'])
def add_vehicle():
    body = request.json
    vehicle = vehicles_model.Vehicle(
        brand=body['brand'],
        model=body['model'],
        year=body['year']
    )
    db.session.add(vehicle)
    db.session.commit()

    return {'id': vehicle.id}, 201


@api.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle = db.session.query(vehicles_model.Vehicle).filter_by(id=vehicle_id).first()
    if vehicle is None:
        return 'Vehicle with id {} not found'.format(vehicle_id), 404

    body = request.json
    vehicle.brand = body['brand']
    vehicle.model = body['model']
    vehicle.year = body['year']

    db.session.commit()

    return {'id': vehicle.id}, 200


@api.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = db.session.query(vehicles_model.Vehicle).filter_by(id=vehicle_id).first()
    if vehicle is None:
        return 'Vehicle with id {} not found'.format(vehicle_id), 404
    else:
        db.session.delete(vehicle)
        db.session.commit()
        return {'id': vehicle.id}, 200

