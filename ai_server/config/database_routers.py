class EmbeddingRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'matching':
            return 'embedding'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'matching':
            return 'embedding'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name, **hints):
        if app_label == 'matching':
            return db == 'embedding'
        return db == 'default'
