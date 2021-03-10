import os

from . import api

INSTANCE_ID = os.getenv('INSTANCE_ID')


@api.route('/instance_id', methods=['GET'])
def get_instance_id():
    return INSTANCE_ID



