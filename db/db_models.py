from tortoise import fields, models


class CommonModel(models.Model):
    id: int = fields.IntField(pk=True)
    created_at: fields.DatetimeField = fields.DatetimeField(auto_now_add=True)


class UserModel(CommonModel):
    username: str = fields.CharField(max_length=50, unique=True)
    hashed_password: str = fields.CharField(max_length=128)


class MessageModel(CommonModel):
    user: "UserModel" = fields.ForeignKeyField("models.UserModel", related_name="messages")
    content: str = fields.TextField()
    role: str = fields.CharField(max_length=10)

