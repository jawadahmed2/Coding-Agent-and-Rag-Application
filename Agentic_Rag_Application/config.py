class AppConfig:

    @staticmethod
    def EMBEDDING_MODEL():
        MODEL = "BAAI/bge-small-en"
        KWARGS = {"device":"cuda"}

        NORMALIZE = {"normalize_embeddings": True}

        return MODEL, KWARGS, NORMALIZE