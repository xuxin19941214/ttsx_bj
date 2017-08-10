#coding=utf-8
#中间键
class UrlPathMiddleware:
    def process_view(self,request,view_func,view_args,view_kwargs):
        #如果当前请求的路径与用户登陆/注册有关，则不需要记录
        if request.path not in [
            '/user/register/',
            '/user/register_handle/',
            '/user/register_valid/',
            '/user/login/',
            '/user/login_handle/',
            '/user/logout/',
            '/user/islogin/',]:
            request.session['url_path']=request.get_full_path()





# http://www.itcast.cn/python?a=100
# 方法get_full_path():/python?a=100
# 属性path:/python
