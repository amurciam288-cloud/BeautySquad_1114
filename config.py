import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def values():
        return {
            "SECRET_KEY": os.environ.get(
                "SECRET_KEY",
                "development-change-me"
            ),
            "SQLALCHEMY_DATABASE_URI": os.environ.get(
                "DATABASE_URL",
                "sqlite:///beautysquad.db"
            ),
            "SQLALCHEMY_TRACK_MODIFICATIONS": Config.SQLALCHEMY_TRACK_MODIFICATIONS,
        }
