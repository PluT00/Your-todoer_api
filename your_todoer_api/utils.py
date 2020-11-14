def custom_jwt_reponse_payload_handler(token, user=None, request=None):
    return {
        'user_id': user.id
    }
