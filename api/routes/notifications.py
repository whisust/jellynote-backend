from flask import request, make_response, Blueprint

from models.errors import BaseError
from models.jellynote import MinifiedNotifications
from persist import RangeQuery, PaginatedQuery, notifications
from routes.utils import json_response, format_content_range

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    try:
        is_page_range = True
        if 'date-range' in request.args:
            is_page_range = False
            query = RangeQuery.from_query_string(request.args['date-range'])
        elif 'range' in request.args:
            query = PaginatedQuery.from_query_string(request.args['range'])
        else:
            query = PaginatedQuery(0, 20)
        notif_count = notifications.count(user_id)
        notifs = MinifiedNotifications([n.to_minified() for n in notifications.list_all(user_id, query)])
        resp = json_response(notifs, 200)
        if is_page_range:
            content_range = format_content_range(query.offset, query.offset + len(notifs.notifications), notif_count)
        else:
            content_range = format_content_range(None, None, notif_count)
        resp.headers['Content-Range'] = content_range
        return resp
    except Exception as e:
        return json_response(BaseError(e.args), 500)
