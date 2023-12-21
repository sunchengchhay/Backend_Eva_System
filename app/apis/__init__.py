from .resources import (
    auth_ns,
    event_ns,
    eform_ns
)
from app.extensions import api

# register namespace
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(event_ns)
api.add_namespace(eform_ns)
