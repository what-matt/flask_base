import os
import signal

from flask import Blueprint
from flask_restful import Api
from redis import exceptions

from app.api.menu import MenuResource
from app.api.menu import MenuListResource
from app.core.connections import get_redis_timeseries_connection
# from app.dao.redis import MenuDaoRedis
from app.dao.sqlite import MenuDaoRedis
from app.dao.redis.key_schema import KeySchema
from app.models import db


blueprint = Blueprint("api", __name__)
api = Api(blueprint)

def configure(app):
    key_schema = KeySchema(app.config['REDIS_KEY_PREFIX'])
    redis_client = get_redis_timeseries_connection(app.config['REDIS_HOST'],
                                        app.config['REDIS_PORT'])

    try:
        redis_client.ping()
    except exceptions.AuthenticationError:
        app.logger.error("Redis authentication failed. Make sure you set "
                         "$REDISOLAR_REDIS_PASSWORD to the correct password "
                         "for your Redis instance. Stopping server.")
        raise
    app.do_teardown_appcontext()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()


    # api.add_resource(MenuListResource,
    #                  '/menu',
    #                  resource_class_args=(MenuDaoRedis(
    #                      redis_client, key_schema), ))
    
    api.add_resource(MenuListResource,
                     '/menu',
                     resource_class_args=(MenuDaoRedis(
                         db, key_schema), ))

    # api.add_resource(MenuResource,
    #                  '/menu/<int:menu_id>',
    #                  resource_class_args=(MenuDaoRedis(
    #                      redis_client, key_schema), ))
