import django.dispatch

channel_updated = django.dispatch.Signal(providing_args=[
    "sender", "channel"
])

changed_tree = django.dispatch.Signal(providing_args=[
    "sender", "updated_instance", "original_instance"
])
