# 状态码

OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}
DATABASE_ERROR = {'code': 900, 'msg': '数据库访问失败'}
PARAMS_ERROR = {'code': 901, 'msg': '参数错误'}


USER_REGISTER_PARAMS_ERROR = {'code': 1000, 'msg': '注册信息不能为空'}
USER_REGISTE_MOBILE_ERROR = {'code': 1001, 'msg': '注册手机号码不符合规则'}
USER_REGISTE_MOBILE_IS_EXISTS = { 'code': 1002, 'msg': '该手机号码已注册'}
USER_REGISTER_PASSWORD_IS_ERROR = {'code': 1003, 'msg': '两次输入的密码不一样'}

USER_LOGIN_IS_NOT_EXSITS = {'code': 1004, 'msg': '用户不存在'}
USER_LOGIN_PASSWORD_IS_ERROR = {'code': 1005, 'msg': '用户登录密码错误'}


USER_UPLOAD_IMAGE_IS_ERROR = {'code': 1006, 'msg': '上传图片不符合标准'}

USER_UPDATE_USERNAME_IS_EXISTS = {'code': 1007, 'msg': '用户名已存在'}

USER_AUTH_IDCARD_IS_ERROR = {'code': 1008, 'msg': '用户身份证信息有误'}

MYHOUSE_USER_IS_NOT_AUTH = {'code': 2000, 'msg': '用户没有实名认证'}