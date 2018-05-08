from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from .base import Base


class CCRDOnlineApply(Base):
    __tablename__ = 'CCRD_ONLINE_APPLY'

    #基本信息
    id = Column(Integer, primary_key=True)
    openid = Column(String(36), nullable=False)
    product_cd = Column(String(36), nullable=False)
    status = Column(String(18), default='申请中')
    step = Column(String(18), default='base_info')
    name = Column(String(80))
    id_no = Column(String(30))
    id_type = Column(String(1))
    cellphone = Column(String(20))
    id_card_img_no = Column(String(40))#身份证正反面影像批次号
    #概述
    id_issuer_address = Column(String(200))#发证机关所在地址
    if_serve_ever = Column(String(1))#证件是否永久有效
    id_start_date = Column(String(8))#证件起始日
    id_last_date = Column(String(8))#证件到期日
    ref_no = Column(String(20))#推荐人编号
    profile_img_no = Column(String(40))#常用证件影像批次号（驾驶证、工作证、房产证、其它证件）
    #工作信息
    corp_name = Column(String(80))#公司名称
    emp_province = Column(String(40))#公司所在省
    emp_city = Column(String(40))#公司所在市
    emp_zone = Column(String(40))#公司所在区/县
    emp_add = Column(String(40))#公司地址
    emp_structure = Column(String(1))#公司性质
    emp_type = Column(String(1))#公司行业类别
    emp_phone = Column(String(20))#公司电话
    emp_post = Column(String(1))#职务
    title_of_technical = Column(String(1))#职称
    emp_department = Column(String(80))#任职部门
    emp_workyears = Column(Numeric(precision=4, scale=2))#本单位工作年限
    year_income = Column(Numeric(precision=13))#年收入
    #住宅信息
    home_state = Column(String(40))#家庭所在省
    home_city = Column(String(40))#家庭所在市
    home_zone = Column(String(40))#家庭所在区县
    home_add = Column(String(200))#家庭地址
    home_phone = Column(String(20))#家庭电话
    house_ownership = Column(String(1))#住宅状况\住宅持有类型
    contact_name = Column(String(40))#联系人中文姓名
    contact_relation = Column(String(1))#联系人与申请人关系
    contact_mobile = Column(String(11))#联系人移动电话
    contact_oname = Column(String(40))#其他联系人中文姓名
    contact_orelation = Column(String(1))#其他联系人与申请人关系
    contact_omobile = Column(String(11))#其他联系人移动电话
    #其他信息
    marital_status = Column(String(1))#婚姻状况
    qualification = Column(String(1))#教育状况
    email = Column(String(80))#电子邮箱
    stmt_media_type = Column(String(1))#账单介质类型
    card_fetch_method = Column(String(1))#介质卡领取方式
    card_mailer_ind = Column(String(1))#卡片寄送地址标志
    sm_amt_verify_ind = Column(String(1))#小额免密


class CredentialType(Base):
    __tablename__ = 'CREDENTIAL_TYPE'

    code = Column(String(1), nullable=False, primary_key=True)
    name = Column(String(36), nullable=False)
