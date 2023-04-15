
    def get_creador(self, obj):
        user_id = obj.creador_id
        username = get_username_by_id(user_id)
        return username