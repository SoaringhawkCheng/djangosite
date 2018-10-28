## 项目结构
```
├── biz # 业务逻辑代码
├── common # 公共代码
│.. ├── constant # 常量
│.. ├── db # db相关
│.. │.. ├── model # model定义
│.. │.. ├── session # db session相关
│.. ├── middleware # 中间件
│.. ├── request # 请求处理
│.. ├── response # 响应处理
│.. └── utils # 工具类
│.. ├── mail.py # 邮件
│.. ├── sms.py # 短信
│.. └── string.py # 字符串处理
├── conf # 配置
├── dals # 数据库读写
├── doc # 文档
├── forms # 表单，如webargs参数schema声明
├── templates # 模板，只存放nginx需要的，前端代码推荐前后分离
│.. ├── 404.html
│.. └── 500.html
├── views # 视图
│.. ├── hello.py
├── bootstrap.py # 启动文件
├── settings.py # 配置文件
└── urls.py # 路由配置
├── libs # 依赖库
├── tasks # 定时任务
├── tmpscripts # 临时脚本
├── validate # 校验器
├── .editorconfig # editorconfig
├── .gitignore # git不跟踪的文件
└── README.md # 项目说明
```

## 代码分层

decorator: 权限校验
view层: 编写请求参数处理、业务逻辑处理、响应的返回等等
dal层: 数据库读写
constant：常量定义

util：常见工具，string util md5

异常定义:

## 依赖说明

views 依赖biz, biz依赖 validate和dals
validate和dals可能相互依赖, 比如说校验数据库里是否存在
validata和dals再依赖common和constant
common依赖constant
constant不能依赖其他的

## 代码demo

```
# view最薄，只负责获取请求数据，调用biz处理业务逻辑, 返回response三个事情 biz里调用validate做业务逻辑处理
# function based views
@permission_check_decorator
def view_handler(request):
    # get request data
    request_data = webargs.djangoparser.parse(form_data_schema, request)

    # business logic
    biz_logic()

    # validate
    for validate in validates:
        validate(request_data)

    # dals
    create_model(request_data)
    session.commit()

    # return response
    return json_response(request)


# class based views
class BaseView(View):
    __metaclass__ = BaseViewMeta

    decorators = []   # 装饰器配置
    methods = []    # 允许方法配置
    params = {}   # 请求参数配置
    resp_type = ResponseType.Json  # 返回参数配置，大部分是json

    def __init__(self, **kwargs):
        super(BaseView, self).__init__(**kwargs)
        for decorator in self.decorators:
            self.handle = decorator(self.handle)
        self.allowed_methods = [method.lower() for method in self.methods]

    def dispatch(self, request, *args, **kwargs):
        """
            dispatch请求的过程，判断请求方法是否满足，不满足返回403
        """
        self.request = request
        method = request.method.lower()
        if method in self.allowed_methods:
            return self.handle(request, *args, **kwargs)
        else:
            self.http_method_not_allowed(request, *args, **kwargs)

    def build_context(self, args):
        pass

    def handle(self, request, *args, **kwargs):
        """
            首先利用webargs解析参数，然后是逻辑处理，最好处理返回结果，暂时只定义了两种返回结果
        """
        parsed_args = parser.parse(self.params, self.request)
        new_args = args + (parsed_args,)
        self.build_context(parsed_args)
        output = dict()
        self.pre_process(parsed_args)
        data = self.process(parsed_args, output)
        self.post_process(parsed_args, output)
        if self.resp_type == ResponseType.Json:
            return get_json_success_response(data)
        else:
            return data

    def pre_process(self, args):
        """
        一些预处理的位置 TODO: 更好的形式
        """
        for func_name, func in self._pre_processers.iteritems():
            func(self, args)

    def post_process(self, args, output):
        for func_name, func in self._post_processers.iteritems():
            func(self, args, output)

    def process(self, args, output):
        """
            业务逻辑实现位置
        """
        raise NotImplementedError()
```