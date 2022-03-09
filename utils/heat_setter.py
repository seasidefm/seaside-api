import json
from functools import wraps
from threading import Thread

from services.heat import HeatService
from services.mqtt import MqttService


def update_heat(func):
    mqtt = MqttService()
    heat_service = HeatService()

    # Wrap function
    @wraps(func)
    def wrapper(*args, **kwargs):
        return_val = func(*args, **kwargs)

        print('updating heat')

        def heat_setter():
            heat = heat_service.get_current_heat()
            mqtt.set_heat_level({
                "faveCount": heat.get('heat_level')
            })

        thread = Thread(target=heat_setter)
        thread.start()

        return return_val

    return wrapper
