from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from walabotapi import db
from walabotapi.models import Device, Fall, Presence, Status, Fallback
from walabotapi.devices.forms import DeviceForm



devices = Blueprint('devices', __name__)


@devices.route('/device/manage', methods=['GET', 'POST'])
@login_required
def manage_devices():
    form = DeviceForm()
    devices = Device.query.filter_by(owner=current_user).all()
    if form.validate_on_submit():
        device = Device(device_id=form.device_id.data, patient_name=form.patient_name.data, location=form.location.data, owner=current_user)
        db.session.add(device)
        db.session.commit()
        flash('Your device has been successfully registered', 'success')
        return redirect(url_for('devices.manage_devices'))
    return render_template('manage_devices.html', title='Manage Devices', form=form, devices=devices)


@devices.route('/device/manage/<int:device_db_id>')
@login_required
def delete_device(device_db_id):
    device = Device.query.get_or_404(device_db_id)
    if device.owner != current_user:
        abort(403)
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('devices.manage_devices'))


@devices.route('/devices')
@login_required
def devices_view():
    devices_list = Device.query.filter_by(owner=current_user).all()
    return render_template('devices.html', title='Registered Devices', devices=devices_list)


@devices.route('/device/falls/<string:device_id>')
@login_required
def fall(device_id):
    device = Device.query.filter_by(device_id=device_id).first_or_404()
    if device.owner != current_user:
        abort(403)
    page = request.args.get('page', 1, type=int)
    falls = Fall.query.filter_by(device_id=device_id).order_by(Fall.id.desc()).paginate(page=page, per_page=5)
    return render_template('events_fall.html', title='Fall Events', falls=falls, device_id=device_id, device= device)


@devices.route('/device/falls/manage/<int:fall_db_id>')
@login_required
def delete_fall(fall_db_id):
    device_id = request.args.get('device_id')
    device = Device.query.filter_by(device_id=device_id).first_or_404()
    if device.owner != current_user:
        abort(403)
    fall = Fall.query.get_or_404(fall_db_id)
    db.session.delete(fall)
    db.session.commit()
    return redirect(url_for('devices.fall', device_id=device_id))


@devices.route('/device/presences/<string:device_id>')
@login_required
def presence(device_id):
    device = Device.query.filter_by(device_id=device_id).first_or_404()
    if device.owner != current_user:
        abort(403)
    page = request.args.get('page', 1, type=int)
    presences = Presence.query.filter_by(device_id=device_id).order_by(Presence.id.desc()).paginate(page=page, per_page=5)
    return render_template('events_presence.html', title='Presence Events', presences=presences, device_id=device_id, device= device)


@devices.route('/device/presences/manage/<int:presence_db_id>')
@login_required
def delete_presence(presence_db_id):
    device_id = request.args.get('device_id')
    device = Device.query.filter_by(device_id=device_id).first_or_404()
    if device.owner != current_user:
        abort(403)
    presence = Presence.query.get_or_404(presence_db_id)
    db.session.delete(presence)
    db.session.commit()
    return redirect(url_for('devices.presence', device_id=device_id))


@devices.route('/device/statuses/<string:device_id>')
@login_required
def status(device_id):
    device = Device.query.filter_by(device_id=device_id).first_or_404()
    if device.owner != current_user:
        abort(403)
    page = request.args.get('page', 1, type=int)
    statuses = Status.query.filter_by(device_id=device_id).order_by(Status.id.desc()).paginate(page=page, per_page=5)
    return render_template('events_status.html', title='Status Events', statuses=statuses, device_id=device_id, device= device)


@devices.route('/device/statuses/manage/<int:status_db_id>')
@login_required
def delete_status(status_db_id):
    device_id = request.args.get('device_id')
    device = Device.query.filter_by(device_id=device_id).first_or_404()
    if device.owner != current_user:
        abort(403)
    status = Status.query.get_or_404(status_db_id)
    db.session.delete(status)
    db.session.commit()
    return redirect(url_for('devices.status', device_id=device_id))


@devices.route('/device/fallback')
@login_required
def fallback():
    page = request.args.get('page', 1, type=int)
    fallbacks = Fallback.query.order_by(Fallback.id.desc()).paginate(page=page, per_page=5)
    return render_template('events_fallback.html', title='Fallback Data', fallbacks=fallbacks)


@devices.route('/device/fallback/manage/<int:fallback_db_id>')
@login_required
def delete_fallback(fallback_db_id):
    fallback = Fallback.query.get_or_404(fallback_db_id)
    db.session.delete(fallback)
    db.session.commit()
    return redirect(url_for('devices.fallback'))
