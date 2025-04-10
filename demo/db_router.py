class UserDatabaseRouter:
    """
    A router to control all database operations on models in the 'user' app.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'user':
            return 'users'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'user':
            return 'users'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both models are from the same database
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'user':
            return db == 'users'
        return db == 'default'
