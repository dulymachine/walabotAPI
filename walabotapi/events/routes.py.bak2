import json
from flask import request, Response, Blueprint, current_app
from walabotapi import db
from walabotapi.models import User, Device, Fall, Presence, Status, Fallback
from datetime import datetime



events = Blueprint('events', __name__)



@events.route('/fall', methods=['POST', 'PUT'])
def respond_fall():
    auth = request.authorization
    if auth.username == current_app.config['POST_USERNAME'] and auth.password == current_app.config['POST_PASSWORD']:
        payload = request.json 
        try:
            device_id = payload['uid']
            end_timestamp = payload['endTimestamp']
            is_silent = payload['isSilent']
            is_learning = payload['isLearning']
            is_simulated = payload['isSimulated']
            status = payload['status']
            status_update_timestamp = payload['statusUpdateTimestamp']
            timestamp = payload['timestamp']
            type_ = payload['type']
            timestamp_str = payload['timestampStr']
            event_id = payload['eventId']
            new_fall = Fall(device_id=device_id, end_timestamp=end_timestamp, is_silent=is_silent, is_learning=is_learning, is_simulated=is_simulated, status=status, status_update_timestamp=status_update_timestamp, timestamp=timestamp, type_=type_, timestamp_str=timestamp_str, event_id=event_id)
            db.session.add(new_fall)
            db.session.commit()
        except:
            payload_string = json.dumps(payload)
            new_fallback = Fallback(payload_string = payload_string, origin = "fall")
            db.session.add(new_fallback)
            db.session.commit()

        return Response(status=200)
    else:
        return Response(status=401)


@events.route('/presence', methods=['POST', 'PUT'])
def respond_presence():
    auth = request.authorization
    if auth.username == current_app.config['POST_USERNAME'] and auth.password == current_app.config['POST_PASSWORD']:
        payload = request.json
        try:
            device_id = payload['uid']
            timestamp = payload['timestamp']
            presence_detected = payload['presenceDetected']
            presence_region_map = json.dumps(payload['presenceRegionMap'])
            new_presence = Presence(device_id=device_id, timestamp=timestamp, presence_detected=presence_detected, presence_region_map=presence_region_map)
            db.session.add(new_presence)
            db.session.commit()
        except:
            payload_string = json.dumps(payload)
            new_fallback = Fallback(payload_string = payload_string, origin = "presence")
            db.session.add(new_fallback)
            db.session.commit()
        return Response(status=200)
    else:
        return Response(status=401)



@events.route('/status', methods=['POST', 'PUT'])
def respond_status():
    auth = request.authorization
    if auth.username == current_app.config['POST_USERNAME'] and auth.password == current_app.config['POST_PASSWORD']:
        payload = request.json
        try:
            device_id = payload['uid']
            timestamp = payload['timestamp']
            temperature = payload['temperature']
            humidity = payload['humidity']
            status = payload['status']
            battery_temperature = payload['batteryTemperature']
            battery_level = payload['batteryLevel']
            up_time = payload['upTime']
            wifi_state = json.dumps(payload['wifiState'])
            storage_state = json.dumps(payload['storageState'])
            new_status = Status(device_id=device_id, timestamp=timestamp, temperature=temperature, humidity=humidity, status=status, battery_temperature=battery_temperature, battery_level=battery_level, up_time=up_time, wifi_state=wifi_state, storage_state=storage_state)
            db.session.add(new_status)
            db.session.commit()
        except:
            payload_string = json.dumps(payload)
            new_fallback = Fallback(payload_string = payload_string, origin = "status")
            db.session.add(new_fallback)
            db.session.commit()
        return Response(status=200)
    else:
        return Response(status=401)
