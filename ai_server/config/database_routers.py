class EmbeddingRouter:
    route_app_labels = {'auth', 'admin', 'contenttypes', 'sessions', 'messages', 'staticfiles'}

    def db_for_read(self, model, **hints):
        # 모델의 앱 라벨을 체크하여 읽기 데이터베이스를 결정합니다.
        if model._meta.app_label == 'matching':
            # UserEmbedding 모델은 embedding 데이터베이스에서 읽습니다.
            if model.__name__ == 'UserEmbedding':
                return 'embedding'
            # UserInfo 모델은 default 데이터베이스에서 읽습니다.
            elif model.__name__ == 'UserInfo':
                return 'default'
        return None

    def db_for_write(self, model, **hints):
        # 모델의 앱 라벨을 체크하여 쓰기 데이터베이스를 결정합니다.
        if model._meta.app_label == 'matching':
            # UserEmbedding 모델은 embedding 데이터베이스에 쓰기 작업을 합니다.
            if model.__name__ == 'UserEmbedding':
                return 'embedding'
            # UserInfo 모델은 default 데이터베이스에 쓰기 작업을 합니다.
            elif model.__name__ == 'UserInfo':
                return 'default'
        return None

    def allow_migrate(self, db, app_label, model_name, **hints):
        # 마이그레이션 권한을 결정합니다.
        if app_label == 'matching':
            # UserEmbedding 모델은 embedding 데이터베이스에만 마이그레이션 합니다.
            if model_name == 'userembedding':
                return db == 'embedding'
            # UserInfo 모델은 default 데이터베이스에만 마이그레이션 합니다.
            elif model_name == 'userinfo':
                return db == 'default'
        elif app_label in self.route_app_labels:
            # 기타 기본 앱들은 모두 default 데이터베이스에 마이그레이션 합니다.
            return db == 'default'
        return None
