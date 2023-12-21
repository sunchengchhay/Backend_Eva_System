from app.extensions import api
from flask_restx import fields

from app.customs.cambodia_datetime import current_time_cambodia

time_cambodia = current_time_cambodia()

# Define a model
login_model = api.model('Login', {
    "username": fields.String(default='admin', required=True, description='Username'),
    "password": fields.String(default='admin', required=True, description='Password')
})

# output_event_model = api.model(
#     'Output Event', {
#         "id": fields.Integer(),
#         "committee_id": fields.Integer()
#     }
# )

# output_login_model = api.model(
#     'Login Output', {
#         "access_token": fields.String(),
#         "user_id ":  fields.Integer(),
#         "events": fields.List(fields.Nested(output_event_model)),
#     }
# )
