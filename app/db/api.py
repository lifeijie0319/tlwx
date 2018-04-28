from .model import *


class OP_Base:
    def __init__(self, session):
        self.db = session


class OP_User(OP_Base):
    def get(self, openid):
        user = self.db.query(User).filter(User.openid==openid).one_or_none()
        return user

    def create(self, data):
        user = User(**data)
        self.db.add(user)

    def check_bind(self, openid):
        user = self.db.query(User).filter(User.openid==openid).one_or_none()
        if not user:
            return False
        else:
            return user.binded


class OP_CredentialType(OP_Base):
    def get(self, code=None):
        query = self.db.query(CredentialType)
        if code:
            ret = query.filter(CredentialType.code==code).one_or_none()
        else:
            ret = query.all()
        return ret


class OP_CCRDOnlineApply(OP_Base):
    def get(self, openid, product_cd=None):
        query = self.db.query(CCRDOnlineApply).filter(CCRDOnlineApply.openid==openid)\
            .filter(~CCRDOnlineApply.status.in_(['成功', '失败', '取消']))
        if product_cd:
            ret = query.filter(CCRDOnlineApply.product_cd==product_cd).one()
        else:
            ret = query.all()
        return ret

    def create(self, data):
        item = CCRDOnlineApply(**data)
        self.db.add(item)

    def update(self, openid, product_cd, data):
        self.db.query(CCRDOnlineApply).filter(CCRDOnlineApply.openid==openid)\
            .filter(CCRDOnlineApply.product_cd==product_cd).update(data)
