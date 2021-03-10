from . import api


@api.route('/health', methods=['GET'])
def get_health_status():
    return ''
