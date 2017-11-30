import json


def get_user_devices(user):
    return [json.loads(x.device_data) for x in user.u2f_tokens.all()]
