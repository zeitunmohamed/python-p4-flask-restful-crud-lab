import json
import pytest
from server.app import app
from server.models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        with app.app_context():
            plant = Plant(name="Aloe", image="https://img.jpg", price=100.0)
            db.session.add(plant)
            db.session.commit()

            response = app.test_client().get(f'/plants/{plant.id}')
            assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        with app.app_context():
            plant = Plant(name="Cactus", image="https://cactus.jpg", price=50.0)
            db.session.add(plant)
            db.session.commit()

            response = app.test_client().get(f'/plants/{plant.id}')
            data = json.loads(response.data.decode())

            assert isinstance(data, dict)
            assert data["id"] == plant.id
            assert data["name"] == "Cactus"

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        with app.app_context():
            plant = Plant(name="Fern", image="fern.png", price=20.0, is_in_stock=True)
            db.session.add(plant)
            db.session.commit()

            response = app.test_client().patch(
                f'/plants/{plant.id}',
                json={"is_in_stock": False}
            )
            data = json.loads(response.data.decode())

            assert response.status_code == 200
            assert isinstance(data, dict)
            assert data["id"] == plant.id
            assert data["is_in_stock"] == False

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''returns empty body with 204 at "/plants/<int:id>" after deletion.'''
        with app.app_context():
            plant = Plant(name="Palm", image="palm.jpg", price=120.0)
            db.session.add(plant)
            db.session.commit()

            response = app.test_client().delete(f'/plants/{plant.id}')
            assert response.status_code == 204
            assert response.data == b''
