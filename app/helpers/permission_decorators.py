from flask.ext import login
from functools import wraps
from flask import request
from flask.ext.restplus import abort

from app.models.session import Session
from app.models.microlocation import Microlocation
from app.models.track import Track
from app.models.speaker import Speaker
from app.models.sponsor import Sponsor


def is_super_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = login.current_user
        if not user.is_super_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = login.current_user
        if not user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def is_organizer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = login.current_user
        event_id = kwargs['event_id']
        if user.is_staff:
            return f(*args, **kwargs)
        if not user.is_organizer(event_id):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def is_coorganizer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = login.current_user
        event_id = kwargs['event_id']
        if user.is_staff:
            return f(*args, **kwargs)
        if not user.is_coorganizer(event_id):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def is_track_organizer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = login.current_user
        event_id = kwargs['event_id']
        if user.is_staff:
            return f(*args, **kwargs)
        if not user.is_track_organizer(event_id):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def is_moderator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = login.current_user
        event_id = kwargs['event_id']
        if user.is_staff:
            return f(*args, **kwargs)
        if not user.is_moderator(event_id):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def can_accept_and_reject(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = login.current_user
        event_id = kwargs['event_id']
        if user.is_staff:
            return f(*args, **kwargs)
        if user.is_organizer(event_id) or user.is_coorganizer(event_id):
            return f(*args, **kwargs)
        abort(403)

    return decorated_function


def can_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = login.current_user
        event_id = kwargs['event_id']
        url = request.url
        if user.is_staff:
            return f(*args, **kwargs)
        if 'events/' + event_id + '/' in url:
            if user.has_role(event_id):
                return f(*args, **kwargs)
            abort(403)
        if '/create/' in url or '/new/' in url:
            if '/events/create/' in url:
                return f(*args, **kwargs)
            if 'session' in url:
                if user.can_create(Session, event_id):
                    return f(*args, **kwargs)
            if 'track' in url:
                if user.can_create(Track, event_id):
                    return f(*args, **kwargs)
            if 'speaker' in url:
                if user.can_create(Speaker, event_id):
                    return f(*args, **kwargs)
            if 'sponsor' in url:
                if user.can_create(Sponsor, event_id):
                    return f(*args, **kwargs)
            if 'microlocation' in url:
                if user.can_create(Microlocation, event_id):
                    return f(*args, **kwargs)
            abort(403)
        if '/edit/' in url:
            if 'events/' + event_id + '/edit/' in url:
                if user.is_organizer(event_id) or user.is_coorganizer(
                        event_id):
                    return f(*args, **kwargs)
            if 'session' in url:
                if user.can_update(Session, event_id):
                    return f(*args, **kwargs)
            if 'track' in url:
                if user.can_update(Track, event_id):
                    return f(*args, **kwargs)
            if 'speaker' in url:
                if user.can_update(Speaker, event_id):
                    return f(*args, **kwargs)
            if 'sponsor' in url:
                if user.can_update(Sponsor, event_id):
                    return f(*args, **kwargs)
            if 'microlocation' in url:
                if user.can_update(Microlocation, event_id):
                    return f(*args, **kwargs)
            abort(403)
        if '/delete/' in url or '/trash/' in url:
            if 'events/' + event_id + '/delete/' in url:
                if user.is_organizer(event_id) or user.is_coorganizer(
                        event_id):
                    return f(*args, **kwargs)
            if 'events/' + event_id + '/trash/' in url:
                if user.is_organizer(event_id) or user.is_coorganizer(
                        event_id):
                    return f(*args, **kwargs)
            if 'session' in url:
                if user.can_delete(Session, event_id):
                    return f(*args, **kwargs)
            if 'track' in url:
                if user.can_delete(Track, event_id):
                    return f(*args, **kwargs)
            if 'speaker' in url:
                if user.can_delete(Speaker, event_id):
                    return f(*args, **kwargs)
            if 'sponsor' in url:
                if user.can_delete(Sponsor, event_id):
                    return f(*args, **kwargs)
            if 'microlocation' in url:
                if user.can_delete(Microlocation, event_id):
                    return f(*args, **kwargs)
            abort(403)

    return decorated_function
