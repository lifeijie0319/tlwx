#-*- coding:utf-8 -*-
import os

tornado_settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'tpl'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'static_url_prefix': '/tlwx/static/',
    'cookie_secret': 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
    'xsrf_cookies': True,
    'debug': True,
}
BASE_URL = 'https://hz.wx.yinsho.com/tlwx'
URL_PREFIX = '/tlwx'
TOKEN = 'yinshowxtoken'
APPID = 'wx6290daffb81416ac'
APPSECRET = 'f3bc7bb9c6dca40dd1bbe9b69fdf6ea0'
ACCESS_TOKEN_KEY = 'tl_access_token'
JSAPI_TICKET_KEY = 'tl_jsapi_ticket'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = BASE_URL + '/media'
MEDIA_PATH = os.path.join(os.path.dirname(__file__), 'media')
REDIS = {
    'HOST': 'localhost',
    'PORT': '6379',
}
TL_HOST = '127.0.0.1'
TL_PORT = '8001'
BILL_TPL_ID = 'z4QouwVQpchy1tNSe-SCk4J2BoAa0y8NXR3HcWp8kmE'
TRADE_TPL_ID = 'dIKccSFgM7gi7zwzd2t960_4Akm-JORICZNwZCAoS1s'
REPAY_TPL_ID = '5xk75tSL9ghjMC3-EijPbB3e_mI6QEFmqLlGm_78sHY'
ID_TYPE = {
    'A': '军官证',
    'C': '警官证',
    'F': '外国人居留证',
    'G': '澳门身份证',
    'H': '港澳居民来往内地通行证',
    'I': '身份证',
    'J': '台湾身份证',
    'L': '香港身份证',
    'O': '其他有效证件',
    'P': '护照',
    'R': '户口薄',
    'S': '士兵证',
    'T': '临时身份证',
    'W': '台湾同胞来往内地通行证',
}
EMP_STRUCTURE = {
    'A': '党政机关',
    'B': '事业单位',
    'C': '军队',
    'D': '社会团体',
    'E': '内资企业',
    'F': '国有企业',
    'G': '集体企业',
    'H': '股份合作企业',
    'I': '联营企业',
    'J': '有限责任公司',
    'K': '股份有限公司',
    'L': '私营企业',
    'M': '外商投资企业(含港、澳、台)',
    'N': '中外合资经营企业(含港、澳、台)',
    'O': '中外合作经营企业(含港、澳、台)',
    'P': '外资企业(含港、澳、台)',
    'Q': '外商投资股份有限公司(含港、澳、台)',
    'R': '个体经营',
    'Z': '其他',
}
EMP_TYPE = {
    'A': '农、林、牧、渔业',
    'B': '采掘业',
    'C': '制造业',
    'D': '电力、燃气及水的生产和供应业',
    'E': '建筑业',
    'F': '交通运输、仓储和邮政业',
    'G': '信息传输、计算机服务和软件业',
    'H': '批发和零售业',
    'I': '住宿和餐饮业',
    'J': '金融业',
    'K': '房地产业',
    'L': '租赁和商务服务业',
    'M': '科学研究、技术服务业和地质勘察业',
    'N': '水利、环境和公共设施管理业',
    'O': '居民服务和其他服务业',
    'P': '教育',
    'Q': '卫生、社会保障和社会福利业',
    'R': '文化、体育和娱乐业',
    'S': '公共管理和社会组织',
    'T': '国际组织',
    'Z': '其他',
}
EMP_POST = {
    'A': '高级管理人员/厅局级及以上',
    'B': '中层管理人员/县处级',
    'C': '低层管理人员/科级',
    'D': '一般员工/科员',
    'E': '内勤',
    'F': '后勤',
    'G': '工人',
    'H': '销售/中介/业务代表',
    'I': '营业员/服务员',
    'J': '正部级',
    'K': '副部级',
    'L': '正厅级',
    'M': '副厅级',
    'N': '正处级',
    'O': '副处级',
    'P': '正科级',
    'Q': '副科级',
    'R': '正股级',
    'S': '副股级',
    'Z': '其他',
}
TITLE_OF_TECHNICAL = {
    'A': '高级及以上',
    'B': '中级',
    'C': '初级',
    'D': '初级以下',
}
HOUSE_OWNERSHIP = {
    'A': '自有住房(无贷款)',
    'B': '贷款购房',
    'C': '租房',
    'D': '与亲属合住',
    'E': '集体宿舍',
    'Z': '其他',
}
CONTACT_RELATION = {
    'B': '兄弟',
    'C': '配偶',
    'D': '父母',
    'F': '父亲',
    'H': '子女',
    'L': '亲属',
    'M': '母亲',
    'O': '其他',
    'S': '姐妹',
    'T': '同学',
    'W': '同事',
    'X': '兄弟姐妹',
    'Y': '朋友',
}
MARITAL_STATUS = {
    'C': '已婚有子女',
    'D': '离异',
    'M': '已婚无子女',
    'O': '其他',
    'S': '未婚',
    'W': '丧偶',
}
QUALIFICATION = {
    'A': '博士及以上',
    'B': '硕士',
    'C': '本科',
    'D': '大专',
    'E': '中专及技校',
    'F': '高中',
    'G': '初中及以下',
}
STMT_MEDIA_TYPE = {
    'B': '纸质+电子账单',
    'E': '电子账单',
    'P': '纸质账单',
}
CARD_FETCH_METHOD = {
    'A': '邮件寄送 ',
    'B': '分支行领卡 ',
    'E': '快递寄送',
}
CARD_MAILER_IND = {
    'C': '公司地址',
    'H': '家庭地址',
}
class G:pass
