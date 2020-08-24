from functools import wraps
 
class A():
    def a_new_decorator(a_func, *args, **kwargs):
        def wrapTheFunction(self):
            print("I am doing some boring work before executing a_func()")
            a_func()
            print("I am doing some boring work after executing a_func()")
        return wrapTheFunction
    
    @a_new_decorator
    def a_function_requiring_decoration(self):
        """Hey yo! Decorate me!"""
        print("I am the function which needs some decoration to "
            "remove my foul smell")
 
a = A()
a.a_function_requiring_decoration()
exit()
# Output: a_function_requiring_decoration
# class Buy(object):
#     def __init__(self):
#         self.reset = True        # 定义一个类属性，稍后在装饰器里更改
#         self.func = True         

#     # 在类里定义一个装饰器
#     def clothes( func):    # func接收body
#         def ware(self, *args, **kwargs):    # self,接收body里的self,也就是类实例
#             print('This is a decrator!')
#             if self.reset == True:        # 判断类属性
#                 print('Reset is Ture, change Func..')
#                 self.func = False        # 修改类属性
#             else:
#                 print('reset is False.')

#             return func(self, *args, **kwargs)

#         return ware

#     @clothes
#     def body(self):
#         print('The body feels could!')

# b = Buy()    # 实例化类
# b.body()     # 运行body
# print(b.func)    # 查看更改后的self.func值，是False，说明修改完成