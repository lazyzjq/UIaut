#coding=utf-8
from selenium import webdriver
from add_md5 import am5
from time import sleep,time,strftime
import unittest,os

'''
1、此文件用于测试第一阶段 充值    提现  资金转人  借款    发标    投标    1债权转让/债权购买    还款
2、usernames.txt是存放手机号码的，关于注册用帐号的处理，是先在setup中读取第一行帐号，然后在注册测试完成后，删除第一行的帐号，以后使用只管readline就OK了
self.username为充值人\投资人
3、测试前，先把D盘中的test.php导入到139.196.82.150的/data/www/yjdSite/yjdMobile/app/user/control路径中，用于跳过登录步骤
4、测试前，先发放10张满100-100的代金券，十张10%的加息券，1张100元10%年化的返现券
'''


class first(unittest.TestCase):
    def setUp(self):
        #创造md5登录密码
        self.password=am5('a123456')
        #登录的
        self.url='https://u.yjdtest.cn/test?mobile='
        #购买标的人
        self.username='15889725416'
        #借款人
        self.borrow='15896302548'
        #截图保存路径
        self.file_path='screen_shot/'
        #当前时间
        self.now_time = strftime("%Y-%m-%d")
        #信用卡
        self.credit='6217007482165930543'
        #创建截图文件
        if os.path.exists('screen_shot/%s'%self.now_time)==True:
            pass
        else:
            os.makedirs('screen_shot/%s'%self.now_time)
    def runTest(self):
        #供the_main调用
        pass
    def test_1(self):
        #充值
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)#打开主页
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()#点击我的账户
        driver.implicitly_wait(10)
        before_cash=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text#获取充值前金额
        before_cash=before_cash[:3]+before_cash[4:]#处理获取的金额，去除第四位的逗号
        before_cash=float(before_cash)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[1]/a[1]').click()#点击充值
        driver.implicitly_wait(10)
        #跳转充值页面
        driver.find_element_by_name('orderAmount').send_keys('100')#输入充值100块
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#点击提交
        sleep(5)
        driver.find_element_by_id('J_ajax_submit_btn').click()#点击立即支付
        sleep(8)
        #跳转华瑞
        driver.find_element_by_xpath('//*[@id="e_hr_getMsgCode"]').click()#点击获取验证码
        #打开验证码中心
        driver2=webdriver.Chrome()
        driver2.get('http://203.110.167.196:9082/usercenter/msgCode.html')
        driver2.implicitly_wait(10)
        driver2.find_element_by_xpath('//*[@id="verificationCode_txt"]').send_keys(self.username)
        driver2.find_element_by_xpath('//*[@id="verificationCode_btn"]').click()
        the_yanzhengma=driver2.find_element_by_xpath('//*[@id="verificactionCode"]/tbody/tr[1]/td[3]').text
        driver2.quit()
        driver.find_element_by_xpath('//*[@id="e_hr_msgCode"]').send_keys(the_yanzhengma)
        driver.find_element_by_xpath('//*[@id="hr_fake_pwd1"]').click()
        for i in range(6):
            driver.find_element_by_xpath('//*[@id="NumberKeyboard___100"]').click()#输入交易密码
        driver.find_element_by_xpath('//*[@id="hr_modal_footer"]/button[2]').click()#点击充值成功的确定键
        driver.implicitly_wait(10)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[1]/a').click()#点击账户总览
        driver.implicitly_wait(10)
        after_cash=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text#获取充值后金额
        after_cash=after_cash[:3]+after_cash[4:]
        after_cash=float(after_cash)
        self.assertEqual(before_cash+100,after_cash)
        driver.quit()
    def test_2(self):
        #充值费用小于1.00，大于5000000
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()  # 点击我的账户
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[1]/a[1]').click()  # 点击充值
        driver.implicitly_wait(5)
        # 跳转充值页面
        driver.find_element_by_name('orderAmount').send_keys('0.95')  # 输入充值100块
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()  # 点击提交
        the_message=driver.find_element_by_xpath('//*[@id="priceTip"]').text
        self.assertEqual(the_message,u'单次充值金额最少为1.00元，最多为500万元。')
        driver.find_element_by_name('orderAmount').click()
        driver.find_element_by_name('orderAmount').clear()
        driver.find_element_by_name('orderAmount').send_keys('5000000.01')
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()  # 点击提交
        the_message = driver.find_element_by_xpath('//*[@id="priceTip"]').text
        self.assertEqual(the_message, u'单次充值金额最少为1.00元，最多为500万元。')
        driver.quit()
    def test_3(self):
        #投资人提现
        driver = webdriver.Chrome()
        driver.get(self.url + self.username)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()  # 点击我的账户
        driver.implicitly_wait(10)
        before_cash = driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text  # 获取充值前金额
        if len(before_cash)>=8:
            before_cash=float(str(before_cash).replace(',',''))
        else:
            before_cash=float(before_cash)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[1]/a[2]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="price"]').send_keys('100')#提款100
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#点击提交
        sleep(5)
        driver.find_element_by_xpath('//*[@id="e_hr_getMsgCode"]').click()
        driver2=webdriver.Chrome()
        driver2.get('http://203.110.167.196:9082/usercenter/msgCode.html')
        driver2.implicitly_wait(5)
        driver2.find_element_by_xpath('//*[@id="verificationCode_txt"]').send_keys(self.username)
        driver2.find_element_by_xpath('//*[@id="verificationCode_btn"]').click()
        yanzhengma=driver2.find_element_by_xpath('//*[@id="verificactionCode"]/tbody/tr[1]/td[3]').text#获取验证码
        driver2.quit()
        driver.find_element_by_xpath('//*[@id="e_hr_msgCode"]').send_keys(yanzhengma)
        driver.find_element_by_xpath('//*[@id="hr_fake_pwd1"]').click()
        for i in range(6):
            driver.find_element_by_xpath('//*[@id="NumberKeyboard___100"]').click()
        driver.find_element_by_xpath('//*[@id="hr_modal_footer"]/button[2]').click()  # 点击充值成功的确定键
        sleep(3)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[1]/a').click()  # 点击账户总览
        driver.implicitly_wait(10)
        after_cash = driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text  # 获取充值后金额
        if len(after_cash)>=8:
            after_cash=float(str(after_cash).replace(',',''))
        else:
            after_cash=float(after_cash)
        self.assertEqual(before_cash-100,after_cash)
        driver.quit()
    def test_4(self):
        #企业借款
        print u'借款'
        jiekuan='10000'
        title='uiauto'+str(int(time()))
        driver=webdriver.Chrome()
        driver.get(self.url+'18011236985')
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[4]/a').click()#点击首页上方的借款
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/a').click()#点击企业借款
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="title"]').send_keys(title)#输入标题
        driver.find_element_by_xpath('//*[@id="price"]').send_keys(jiekuan)#输入借款金额
        driver.find_element_by_xpath('//*[@id="myform"]/table/tbody/tr[6]/td/div/ul/span').click()#点击借款期限
        driver.find_element_by_xpath('//*[@id="myform"]/table/tbody/tr[6]/td/div/div/div/ul/li[4]').click()#选择借款期限
        driver.find_element_by_xpath('//*[@id="myform"]/table/tbody/tr[12]/td/div/ul/span').click()#点击还款方式
        driver.find_element_by_xpath('//*[@id="myform"]/table/tbody/tr[12]/td/div/div/div/ul/li[1]').click()#每月付息，到期还本
        #driver.find_element_by_class_name('length_6').send_keys(u'测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试测试')
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#点击下一步，跳转至下个页面            sleep(5)
        driver.find_element_by_xpath('//*[@id="myform"]/div/div[1]/div/div[2]/table/tbody/tr[5]/td/div[1]/ul/span').click()#点击企业所在地1
        driver.find_element_by_xpath('//*[@id="myform"]/div/div[1]/div/div[2]/table/tbody/tr[5]/td/div[1]/div/div/ul/li[1]').click()#选择省市
        driver.find_element_by_xpath('//*[@id="myform"]/div/div[1]/div/div[2]/table/tbody/tr[5]/td/div[2]/ul/span').click()#点击企业所在地2
        driver.find_element_by_xpath('//*[@id="myform"]/div/div[1]/div/div[2]/table/tbody/tr[5]/td/div[2]/div/div/ul/li').click()#选择市
        driver.find_element_by_xpath('//*[@id="myform"]/div/div[1]/div/div[2]/table/tbody/tr[5]/td/div[3]/ul/span').click()#点击企业所在地3
        driver.find_element_by_xpath('//*[@id="myform"]/div/div[1]/div/div[2]/table/tbody/tr[5]/td/div[3]/div/div/ul/li[1]').click()#选择区县
        driver.find_element_by_xpath('//*[@id="myform"]/div/div[1]/div/div[2]/table/tbody/tr[24]/td/div/ul/span').click()#点击职工人数
        driver.find_element_by_xpath('//*[@id="myform"]/div/div[1]/div/div[2]/table/tbody/tr[24]/td/div/div/div/ul/li[1]').click()#选择人数
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#点击确认提交,跳转借款管理页面
        sleep(15)
        c_jiekuan=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[4]/font').text#获取借款管理中的借款金额
        c_jiekuan=float(c_jiekuan[:2]+c_jiekuan[3:])
        c_status=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[6]').text#获取借款管理中的标的状态
        c_times=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[3]').text
        self.assertEqual(c_jiekuan,10000.00)
        self.assertEqual(c_status,u'正在初审')
        self.assertEqual(c_times,u'12个月')
        driver.quit()
    def test_5(self):
        #发标
        print u'发标'
        driver = webdriver.Chrome()
        # 登录
        driver.get('http://admina.yjdtest.cn/')
        sleep(2)
        driver.find_element_by_xpath("//input[@id='username']").send_keys('admin')
        sleep(2)
        driver.find_element_by_xpath("//input[@id='password']").send_keys('123456')
        sleep(2)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        sleep(4)
        driver.find_element_by_xpath("//a[@data-id='nav_5']").click()
        # 初审
        sleep(3)
        driver.find_element_by_xpath("//a[@data-id='VerifyNo1_80']").click()
        sleep(2)
        driver.switch_to.frame("iframe_VerifyNo1_80")
        title=driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[1]/td[3]').text#获取标的标题
        driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[1]/td[10]/a').click()
        sleep(2)
        driver.find_element_by_xpath("/html/body/div/div[2]/ul/li[9]/a").click()
        sleep(2)
        driver.find_element_by_xpath('/html/body/div/div[2]/ul/li[9]/a').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div/form/div[2]/table/tbody/tr[5]/td/ul/li[1]/label/input').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div/form/div[2]/table/tbody/tr[8]/td/ul/li[1]/label/input').click()
        driver.find_element_by_xpath('/html/body/div/form/div[2]/table/tbody/tr[9]/td/textarea').send_keys(
            'sssssssssssssssssssssssssssssssssssssssssssssssssssssss')
        driver.find_element_by_xpath('/html/body/div/form/div[4]/table/tbody/tr[1]/td/input').send_keys('100')
        driver.find_element_by_xpath('/html/body/div/form/div[4]/table/tbody/tr[2]/td/input').send_keys('100')
        driver.find_element_by_xpath('/html/body/div/form/div[4]/table/tbody/tr[3]/td/input').send_keys('100')
        driver.find_element_by_xpath('/html/body/div/form/div[6]/table/tbody/tr[3]/td/textarea').send_keys('okokok')
        driver.find_element_by_xpath('/html/body/div/form/div[7]/div/button').click()
        print u'初审成功'
        sleep(3)
        driver.switch_to.default_content()
        # 复审
        driver.find_element_by_xpath('//*[@id="B_menubar"]/dt[17]/a').click()
        sleep(2)
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="iframe_VerifyNo2_81"]'))
        driver.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[1]/td[9]/a').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div/div[2]/ul/li[7]/a').click()
        sleep(1)
        # driver.find_element_by_xpath('/html/body/div/form/div[2]/table/tbody/tr/td/input').send_keys('15882475913')
        driver.find_element_by_xpath('/html/body/div/form/div[4]/table/tbody/tr[1]/td/input').send_keys('100')
        driver.find_element_by_xpath('/html/body/div/form/div[4]/table/tbody/tr[2]/td/input').send_keys('100')
        driver.find_element_by_xpath('/html/body/div/form/div[4]/table/tbody/tr[3]/td/input').send_keys('100')
        driver.find_element_by_xpath('/html/body/div/form/div[8]/table/tbody/tr[3]/td/textarea').send_keys('ok')
        driver.find_element_by_xpath('/html/body/div/form/div[8]/table/tbody/tr[4]/td/textarea').send_keys('ok')
        driver.find_element_by_xpath('/html/body/div/form/div[9]/div/button').click()
        print u'复审成功'
        sleep(3)
        driver.switch_to.default_content()
        # 发标
        driver.find_element_by_xpath('//*[@id="B_menubar"]/dt[18]/a').click()
        sleep(1)
        driver.switch_to.frame("iframe_VerifyNo3_94")
        driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[9]/a').click()
        sleep(2)
        driver.find_element_by_xpath('/html/body/div/div[2]/ul/li[7]/a').click()
        sleep(2)
        jjs = "$('input:radio').eq(7).attr('checked', 'checked').click()"
        driver.execute_script(jjs)
        driver.find_element_by_xpath('/html/body/div[1]/form/div[4]/table/tbody/tr[3]/td/textarea').send_keys('ok')
        driver.find_element_by_xpath('/html/body/div[1]/form/div[5]/div/button').click()
        print u'发标成功'
        sleep(1)
        #发标完之后，上出借页面查看是否有该标的
        driver2=webdriver.Chrome()
        driver2.get(self.url+'18011236985')
        driver2.implicitly_wait(10)
        driver2.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[2]/a').click()
        driver2.implicitly_wait(10)
        c_title=driver2.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/a/div[1]/h4').text
        self.assertEqual(title,c_title)
        driver.quit()
    def test_6(self):
        #投标
        print u'投标'
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.implicitly_wait(10)
        before_cash=driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/ul/li[1]/span').text#首页获取金额字符串
        before_cash=float(before_cash[:3]+before_cash[4:10])#处理金额字符
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[2]/a').click()#点击出借
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/a').click()#点击标的
        driver.implicitly_wait(10)
        before_baifenbi=driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul[2]/li[4]/span/em').text#获取标的进度百分比
        #数字为两位和三位，去除百分比符号
        if len(before_baifenbi)==2:
            before_baifenbi = int(before_baifenbi[0])
        elif len(before_baifenbi)==3:
            before_baifenbi=int(before_baifenbi[:2])
        before_highest=driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul[2]/li[6]/span/font').text#获取当前最高可投资额
        #数字为五位和四位时，对逗号做处理
        if len(before_highest)>=8:
            before_highest=float(str(before_highest).replace(',',''))
        else:
            before_highest=float(before_highest)
        driver.find_element_by_xpath('//*[@id="price"]').send_keys('100')#投资金额输入100元
        driver.find_element_by_xpath('//*[@id="xuanze"]').click()#点击代金券
        driver.find_element_by_xpath('//*[@id="vol"]/li[1]').click()#点击不选择
        driver.find_element_by_xpath('//*[@id="checkbox"]').click()#打勾协议
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#投标
        sleep(15)
        after_baifenbi=driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul[2]/li[4]/span/em').text#获取投标后的百分比
        if len(after_baifenbi)==2:
            after_baifenbi = int(after_baifenbi[0])
        elif len(after_baifenbi)==3:
            after_baifenbi=int(after_baifenbi[:2])
        after_highest=driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul[2]/li[6]/span/font').text#获取投标后的最高可投资金额
        # 数字为五位和四位时，对逗号做处理
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()#点击I我的账户
        print 'wait 40s'
        sleep(40)  # 等待40S，等待总交易金额刷新
        driver.refresh()#刷新
        after_cash = driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text  # 获取投标后总金额
        after_cash = float(str(after_cash).replace(',', ''))  # 处理金额
        if len(after_highest) >= 8:
            after_highest=float(str(after_highest).replace(',',''))
        else:
            after_highest=float(after_highest)
        sleep(10)
        #获取返现券的返现金额
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[2]/a').click()#点击交易记录
        jiangli=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[3]/font').text
        if len(jiangli)>=8:
            jiangli=float(str(jiangli))
        else:
            jiangli=float(jiangli)
        print before_cash
        print jiangli
        print after_cash
        #计算投标后的总金额加上投标金额减去返现券的奖励金
        the_after_cash=after_cash+100-jiangli
        print the_after_cash
        self.assertEqual(before_cash,the_after_cash)#判断金额
        self.assertEqual(before_baifenbi,after_baifenbi-1)
        self.assertEqual(before_highest,after_highest+100)
        driver.quit()
    def test_7(self):
        #用和满减券,返现券投资
        print u'满减券和返现券投资'
        trancash=100.00
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)#暂时用购买债权人投标
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()#点击我的账户
        before_djq=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[2]/ul/li[3]/font').text
        before_djq=int(before_djq)#获取代金券数量
        before_jxq=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[2]/ul/li[4]/font').text
        before_jxq=int(before_jxq)#获取加息券数量
        before_cash = driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text
        before_cash = float(str(before_cash).replace(',', ''))  # 交易前的总金额
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[2]/a').click()#点击出借
        sleep(2)
        driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/a').click()#点击标的
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="price"]').send_keys(str(int(trancash)))#输入金额
        driver.find_element_by_xpath('//*[@id="xuanze"]').click()#点击代金券
        driver.find_element_by_xpath('//*[@id="vol"]/li[3]').click()#选择满减券
        driver.find_element_by_xpath('//*[@id="jiaxi"]').click()#点击加息券
        driver.find_element_by_xpath('//*[@id="rai"]/li[2]').click()#选择加息券
        driver.find_element_by_xpath('//*[@id="checkbox"]').click()#勾选协议
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#点击立即投标
        sleep(10)
        #点击我的账户
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        after_djq=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[2]/ul/li[3]/font').text
        after_djq=int(after_djq)#获取代金券数量
        after_jxq=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[2]/ul/li[4]/font').text
        after_jxq=int(after_jxq)#获取加息券数量
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[2]/a').click()
        sleep(50)#等待50s，等返现记录刷新
        driver.refresh()
        #buytype=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[2]').text#交易类型
        #buytype=str(buytype)
        money=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[3]/font').text#交易金额
        money=float(money)
        after_cash=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[4]/font').text#实时可用金额
        after_cash=float(str(after_cash).replace(',',''))

        #tip=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[13]/td[6]').text
        #判断代金券数量
        self.assertEqual(before_djq-1,after_djq)
        #判断满减券
        self.assertEqual(before_jxq-1,after_jxq)
        #判断交易类型
        #self.assertEqual(buytype,u'奖励')
        #判断交易金额
        #self.assertEqual(money,trancash*0.1)
        #判断实时可用金额
        self.assertEqual(before_cash,after_cash-money)
        #判断备注
        #self.assertEqual(tip,u'返现券返现')
        driver.quit()
    def test_8(self):
        #投满标
        print u'投满标并终审'
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[2]/a').click()#点击出借
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/a').click()#点击标的
        go_cash=driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/ul[2]/li[6]/span/font').text
        if len(go_cash)>=8:
            go_cash=str(int(float(str(go_cash).replace(',',''))))#处理投资金额
        else:
            go_cash=str(int(float(go_cash)))
        driver.find_element_by_xpath('//*[@id="price"]').send_keys(go_cash)#输入金额
        driver.find_element_by_xpath('//*[@id="xuanze"]').click()  # 点击代金券
        driver.find_element_by_xpath('//*[@id="vol"]/li[1]').click()  # 点击不选择
        driver.find_element_by_xpath('//*[@id="checkbox"]').click()  # 勾选协议
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()  # 点击立即投标
        driver.quit()
        driver2 = webdriver.Chrome()
        # 登录
        driver2.get('http://admina.yjdtest.cn/')
        sleep(2)
        driver2.find_element_by_xpath("//input[@id='username']").send_keys('admin')
        sleep(2)
        driver2.find_element_by_xpath("//input[@id='password']").send_keys('123456')
        sleep(2)
        driver2.find_element_by_xpath("//input[@type='submit']").click()
        sleep(4)
        driver2.find_element_by_xpath("//a[@data-id='nav_5']").click()
        sleep(2)
        driver2.find_element_by_xpath('//*[@id="B_menubar"]/dt[19]/a').click()
        sleep(2)
        driver2.switch_to.frame('iframe_VerifyNo4_82')
        driver2.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[9]/a').click()
        sleep(2)
        driver2.find_element_by_xpath('/html/body/div/div[2]/ul/li[7]/a').click()
        sleep(2)
        driver2.find_element_by_xpath('/html/body/div/form/div[8]/table/tbody/tr[2]/td/textarea').send_keys('okokok')
        driver2.find_element_by_xpath('/html/body/div/form/div[9]/div/button').click()
        print u'终审成功'
        driver2.quit()
    def test_9(self):
        #债权转让
        print u'债权转让'
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()#点击账户详情
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[3]/a').click()#点击我的出借
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[8]/a').click()#点击转出
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="discount_per_partion"]').clear()
        driver.find_element_by_xpath('//*[@id="discount_per_partion"]').send_keys('1')
        sleep(2)
        js1='document.getElementById("J_ajax_submit_btn").click();'
        driver.execute_script(js1)
        # driver.find_element_by_id('J_ajax_submit_btn').click()#确认债转//*[@id="J_ajax_submit_btn"]
        sleep(10)
        zq_name1=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[2]/p[1]/a').text#获取债权名称
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[3]/a').click()#点击债权
        driver.implicitly_wait(10)
        zq_name2=driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/a/div/h4').text#在购买债权页面中获取债权名称
        #判断债权名称
        self.assertEqual(zq_name1,zq_name2)
        driver.quit()
    def test_10(self):
        #购买债权
        print u'购买债权'
        driver=webdriver.Chrome()
        driver.get(self.url+'18386249157')
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[3]/a').click()#点击债权按钮
        driver.implicitly_wait(10)
        driver.find_element_by_css_selector('body > div.ui-row.mt20 > div:nth-child(1) > div:nth-child(1) > a > div > div.borrow-box.mb20 > div.borrow-price > div').click()#点击购买债权
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="number"]').send_keys('1')#输入购买份数
        sleep(2)
        zqprice = driver.find_element_by_xpath('//*[@id="buyprice"]').text
        zqprice = float(zqprice)  # 债权价格
        before_cash=driver.find_element_by_xpath('//*[@id="myform"]/table/tbody/tr[6]/td/div/ul/span/font').text
        before_cash=float(str(before_cash[1:-4]).replace(',',''))
        driver.find_element_by_xpath('//*[@id="checkbox"]').click()#点击协议
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#点击立即购买
        sleep(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()#点击我的账户
        after_cash=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text
        after_cash=float(str(after_cash).replace(',',''))#处理金额
        self.assertNotEqual(after_cash,before_cash)
        driver.quit()
    def test_11(self):
        #还款
        print u'还款'
        driver=webdriver.Chrome()
        #先获取出借人的金额
        driver.get(self.url+self.username)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()#点击我的账户
        driver.implicitly_wait(10)
        chujieren_cash=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text
        if len(chujieren_cash)>=8:
            chujieren_cash=float(str(chujieren_cash).replace(',',''))#获取出借人总金额
            chujieren_cash=round(chujieren_cash,2)
        else:
            chujieren_cash=float(chujieren_cash)
            chujieren_cash=round(chujieren_cash,2)
        driver.get(self.url+'18011236985')#登录借款人
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()#点击我的账户
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[4]/a').click()#点击借款管理
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="J_box_nav"]/ul/a[2]').click()#点击我要还款
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[2]').click()#点击翻页
        driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[6]/td[8]/a').click()#点击还款
        total_cash=driver.find_element_by_xpath('//*[@id="myform"]/table[1]/tbody/tr[11]/td/span').text#账户总金额
        if len(total_cash)>=8:
            total_cash=float(str(total_cash).replace(',',''))
            total_cash=round(total_cash,2)
        else:
            total_cash=float(total_cash)
        re_cash=driver.find_element_by_xpath('//*[@id="myform"]/table[1]/tbody/tr[9]/td/span').text#应还总额
        if len(re_cash)>=8:
            re_cash=float(str(re_cash).replace(',',''))
            re_cash=round(re_cash,2)
        else:
            re_cash=float(re_cash)
            re_cash = round(re_cash, 2)
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#点击执行还款
        sleep(10)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[1]/a').click()#点击账户总览
        after_total_cash=driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text
        if len(after_total_cash)>=8:
            after_total_cash=float(str(after_total_cash).replace(',',''))
            after_total_cash=round(after_total_cash,2)
        else:
            after_total_cash=float(after_total_cash)
            after_total_cash = round(after_total_cash, 2)
        driver.get(self.url+self.username)#登录出借人
        print u'等待出借人的交易记录刷新90S'
        sleep(90)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()  # 点击我的账户
        driver.implicitly_wait(10)
        after_chujieren_cash = driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[1]/div/div[2]/font').text
        if len(after_chujieren_cash) >= 8:
            after_chujieren_cash = float(str(after_chujieren_cash).replace(',', ''))  # 获取出借人总金额
        else:
            after_chujieren_cash = float(after_chujieren_cash)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[2]/a').click()#点击交易记录
        jiangli=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[1]/td[3]/font').text
        jiangli=float(jiangli)#获取加息券奖励的金额
        re_cash2=driver.find_element_by_xpath('//*[@id="user-right"]/table/tbody/tr[2]/td[3]/font').text
        if len(re_cash2)>=8:
            re_cash2=float(str(re_cash2).replace(',',''))
            re_cash2=round(re_cash2,2)
        else:
            re_cash2=float(re_cash2)
            re_cash2 = round(re_cash2, 2)
        print u'出借人收到还款后的总金额：'+str(after_chujieren_cash)
        print u'还款：'+str(re_cash2)
        print u'返现券返现金额：'+str(jiangli)
        print u'出借人没收到还款时的总金额'+str(chujieren_cash)
        #计算借款人扣款是否正确，出借人收入是否正确，第一期都是有加息券加成的
        #借款人还款前金额total_cash，借款人应扣金额recash，借款人还款后金额after_total_cash
        self.assertEqual(total_cash-re_cash,after_total_cash)#判断借款人金额是否正确
        self.assertEqual(after_chujieren_cash,re_cash2+jiangli+chujieren_cash)
        driver.quit()
    def test_12(self):
        #验证点击首页个人信息的出借，是否能跳转至出借页面

        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/a[1]').click()
        driver.get_screenshot_as_file(self.file_path+self.now_time+'/test_12.png')
    def test_13(self):
        #验证点击首页个人信息的充值，是否能跳转至充值页面
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/a[2]').click()
        driver.implicitly_wait(10)
        driver.get_screenshot_as_file(self.file_path+self.now_time+'test_13.png')
    def test_14(self):
        #点击首页个人信息的眼睛，是否能屏蔽金额
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/ul/li[1]/i').click()
        price=driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/ul/li[1]/span').text
        self.assertEqual(price,'****')
    def test_15(self):
        #点击左上角医界贷图片，返回首页
        driver=webdriver.Chrome()
        driver.get(self.url+self.borrow)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()#点击我的账户
        driver.find_element_by_xpath('/html/body/div[2]/div/a/div/img').click()#点击左上角医界贷图片，返回首页
        driver.implicitly_wait(10)
        try:
            the_text=driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/a[1]').text
            print the_text
        except:
            print u'15失败，截图'
            driver.get_screenshot_as_file(u'screen_shot/%s/点击左上角医界贷图片返回首页.png'%self.now_time)
        finally:
            driver.quit()
    def test_16(self):
        #点击账户总览-回款查询
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()  # 点击我的账户
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[2]/ul/li[1]/div/a').click()#点击回款查询
        try:
            the_text=driver.find_element_by_xpath('//*[@id="user-right"]/table/thead/tr/th[5]').text
            print the_text
        except:
            print u'16失败，截图'
            driver.get_screenshot_as_file(u'screen_shot/%s/点击账户总览-回款查询.png'%self.now_time)
        finally:
            driver.quit()
    def test_17(self):
        #账户总览-代金券查看
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[2]/ul/li[3]/div/a').click()#点击代金券查看
        try:
            the_text=driver.find_element_by_xpath('//*[@id="J_box_nav"]/h3').text
            print str(the_text)
        except:
            print u'17失败，截图'
            driver.get_screenshot_as_file(u'screen_shot/%s/账户总览-代金券查看.png'%self.now_time)
        finally:
            driver.quit()
    def test_18(self):
        #账户总览-加息券查看
        driver=webdriver.Chrome()
        driver.get(self.url+self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[4]/div/div[2]/ul/li[4]/div/a').click()
        try:
            the_text=driver.find_element_by_xpath('//*[@id="J_box_nav"]/h3').text
            print the_text
        except:
            print u'18失败，截图'
            driver.get_screenshot_as_file(u'screen_shot/%s/账户总览-加息券查看.png'%self.now_time)
        finally:
            driver.quit()
    def test_19(self):
        #借款人-账户总览-我要还款
        driver=webdriver.Chrome()
        driver.get(self.url+self.borrow)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[6]/div/div/a').click()#点击我要还款
        try:
            the_text=driver.find_element_by_xpath('//*[@id="user-right"]/table/thead/tr/th[8]').text
            print the_text
        except:
            print u'19失败，截图'
            driver.get_screenshot_as_file(u'screen_shot/%s/借款人-账户总览-我要还款.png'%self.now_time)
        finally:
            driver.quit()
    def test_20(self):
        #投资人-账户总览-上月账单
        driver = webdriver.Chrome()
        driver.get(self.url + self.borrow)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[6]/div/div/a').click()
        try:
            the_text=driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/div/div[1]').text
            print the_text
        except:
            print u'20失败，截图'
            driver.get_screenshot_as_file(u'screen_shot/%s/投资人-账户总览-上月账单.png'%self.now_time)
        finally:
            driver.quit()
    def test_21(self):
        #投资人-交易记录-各个模块截图
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url + self.borrow)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[6]/div/div/a').click()
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[2]/a').click()#点击交易记录
        #截取全部
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-全部截图.png'%self.now_time)
        #截取充值
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[2]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-充值截图.png'%self.now_time)
        #截取出借
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[3]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-出借截图.png'%self.now_time)
        #截取提现
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[4]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-提现截图.png'%self.now_time)
        #截取奖励
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[5]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-奖励截图.png'%self.now_time)
        #截取借款
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[6]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-借款截图.png'%self.now_time)
        #截取其他
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[7]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-其他截图.png'%self.now_time)
        #交易记录-普通账户-全部
        driver.find_element_by_xpath('//*[@id="J_box_nav"]/ul/a[2]').click()#点击普通账户
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-普通账户-全部截图.png'%self.now_time)
        #交易记录-普通账户-充值
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[2]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-普通账户-充值截图.png' % self.now_time)
        #交易记录-普通账户-出借
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[3]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-普通账户-出借截图.png' % self.now_time)
        #交易记录-普通账户-提现
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[4]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-普通账户-提现截图.png' % self.now_time)
        #交易记录-普通账户-奖励
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[5]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-普通账户-奖励截图.png' % self.now_time)
        #交易记录-普通账户-借款
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[6]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-普通账户-借款截图.png' % self.now_time)
        #交易记录-普通账户-其他
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[7]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/投资人-交易记录-普通账户-其他截图.png' % self.now_time)
    def test_22(self):
        #我的出借
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url + self.borrow)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[6]/div/div/a').click()
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[3]/a').click()  # 点击我的出借
        #我的出借-我的债权-有效债权
        driver.get_screenshot_as_file(u'screen_shot/%s/我的出借-我的债权-有效债权.png'%self.now_time)
        #我的出借-我的债权-有效债权-回款报表查看按钮
        driver.find_element_by_xpath('//*[@id="9848"]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/我的出借-我的债权-有效债权-查看.png'%self.now_time)
        #我的出借-我的债权-过期债权
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[2]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/我的出借-我的债权-过期债权.png'%self.now_time)
        #我的出借-我的债权-过期债权-回款报表查看按钮
        driver.find_element_by_xpath('//*[@id="9847"]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/我的出借-我的债权-过期债权-回款报表查看按钮.png'%self.now_time)
        #我的出借-回款查询-代收回款
        driver.find_element_by_xpath('//*[@id="J_box_nav"]/ul/a[2]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/我的出借-回款查询-代收回款.png'%self.now_time)
        #我的出借-汇款查询-已收回款
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[2]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/我的出借-回款查询-已收回款.png'%self.now_time)
        #我的出借-上月账单
        driver.find_element_by_xpath('//*[@id="J_box_nav"]/ul/a[3]').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/我的出借-上月账单.png'%self.now_time)
        #我的出借-上月账单-查看明细按钮
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/div/div[2]/a').click()
        driver.get_screenshot_as_file(u'screen_shot/%s/我的出借-上月账单-查看明细按钮.png'%self.now_time)
    def test_23(self):
        #我的奖励
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url + self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-right"]/div[6]/div/div/a').click()
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[4]/a').click()  # 点击我的奖励
        #我的奖励-全部-代金券-可使用
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-代金券-可使用.png'%self.now_time)
        #我的奖励-全部-代金券-已使用
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-代金券-已使用.png'%self.now_time)
        #我的奖励-全部-代金券-已过期
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[3]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-代金券-已过期.png'%self.now_time)
        #我的奖励-全部-加息券-可使用

        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-加息券-可使用.png'%self.now_time)
        #我的奖励-全部-加息券-已使用

        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-加息券-已使用.png'%self.now_time)
        #我的奖励-全部-加息券-已过期

        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[3]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-加息券-已过期.png' % self.now_time)
        #我的奖励-全部-返现券-可使用

        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[3]').click()
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-返现券-可使用.png' % self.now_time)
        #我的奖励-全部-返现券-已使用

        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-返现券-已使用.png' % self.now_time)
        #我的奖励-全部-返现券-已过期

        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[3]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-返现券-已过期.png' % self.now_time)
        #我的奖励-全部-理财金-可使用
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[4]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-理财金-可使用.png'%self.now_time)
        #我的奖励-全部-理财金-已使用
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-理财金-已使用.png' % self.now_time)
        #我的奖励-全部-理财金-已过期
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[3]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-理财金-已过期.png' % self.now_time)
        #我的奖励-全部-预约券-可使用
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[5]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-预约券-可使用.png'%self.now_time)
        #我的奖励-全部-预约券-已使用
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-预约券-已使用.png' % self.now_time)
        #我的奖励-全部-预约券-已过期
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[3]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-预约券-已过期.png' % self.now_time)
        #我的奖励-全部-提额券-可使用
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[6]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-提额券-可使用.png'%self.now_time)
        #我的奖励-全部-提额券-已过期
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-全部-提额券-已过期.png' % self.now_time)
        #我的奖励-兑换奖励
        driver.find_element_by_xpath('//*[@id="J_box_nav"]/ul/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-兑换奖励.png'%self.now_time)
        #我的奖励-使用说明
        driver.find_element_by_xpath('//*[@id="J_box_nav"]/ul/a[3]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的奖励-使用说明.png'%self.now_time)
    def test_24(self):
        #我的推广
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url + self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[5]/a').click()#点击我的推广
        #邀请好友
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的推广-邀请好友.png'%self.now_time)
        #邀请明细
        driver.find_element_by_xpath('//*[@id="J_box_nav"]/ul/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的推广-邀请明细.png'%self.now_time)
        #领取收益-待领取
        driver.find_element_by_xpath('//*[@id="J_box_nav"]/ul/a[3]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的推广-领取收益-待领取.png'%self.now_time)
        #领取收益-已领取
        driver.find_element_by_xpath('//*[@id="user-right"]/div[2]/a[2]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/我的推广-领取收益-已领取.png'%self.now_time)
    def test_25(self):
        #账户设置-绑定邮箱
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url + self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[6]/a').click()#点击账户设置
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/table/tbody/tr[4]/td[4]/div/a').click()#点击绑定邮箱
        driver.implicitly_wait(10)
        driver.find_element_by_name('bindemail').send_keys('asdsadsaddasd@qq.com')
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()
        sleep(3)
        driver.get_screenshot_as_file(u'screen_shot/%s/绑定邮箱截图.png'%self.now_time)
        driver.quit()
    def test_26(self):
        #账户设置-修改密码
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url + self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[6]/a').click()  # 点击账户设置
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/table/tbody/tr[5]/td[4]/div/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_name('old').send_keys('a123456')
        driver.find_element_by_name('password').send_keys('a123456')
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()
        sleep(1)
        driver.get_screenshot_as_file(u'screen_shot/%s/账户设置-修改密码.png'%self.now_time)
        sleep(1)
        driver.quit()
    def test_27(self):
        #账户设置-修改交易密码
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url + self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[6]/a').click()  # 点击账户设置
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/table/tbody/tr[6]/td[4]/div/a').click()#点击修改交易密码
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="bkAccountId"]').send_keys(self.credit)
        driver.find_element_by_xpath('//*[@id="telephoneNo"]').send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="e_hr_getMsgCode"]').click()#点击获取验证码
        driver2=webdriver.Chrome()#打开第二个浏览器验证码
        driver2.get('http://203.110.167.196:9082/usercenter/msgCode.html')
        driver2.implicitly_wait(10)
        driver2.find_element_by_xpath('//*[@id="verificationCode_txt"]').send_keys(self.username)#输入号码
        driver2.find_element_by_xpath('//*[@id="verificationCode_btn"]').click()#查询
        yzm=driver2.find_element_by_xpath('//*[@id="verificactionCode"]/tbody/tr[1]/td[3]').text
        driver.find_element_by_xpath('//*[@id="e_hr_msgCode"]').send_keys(yzm)#输入验证码
        driver.find_element_by_xpath('//*[@id="hr_fake2_pwd1"]').click()
        for i in range(6):
            driver.find_element_by_xpath('//*[@id="NumberKeyboard2___100"]').click()
        driver.find_element_by_xpath('//*[@id="hr_fake3_pwd1"]').click()
        for i in range(6):
            driver.find_element_by_xpath('//*[@id="NumberKeyboard3___100"]').click()
        sleep(3)
        driver.get_screenshot_as_file(u'screen_shot/%s/修改交易密码.png'%self.now_time)
        driver.quit()
        driver2.quit()
    def test_28(self):
        #账户设置-免密设置
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self.url + self.username)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/a').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@id="user-left"]/ul/li[6]/a').click()  # 点击账户设置
        driver.find_element_by_xpath('//*[@id="user-right"]/div[3]/table/tbody/tr[7]/td[4]/div/a').click()
        driver.find_element_by_name('pwd_limit').send_keys('1095')
        driver.find_element_by_name('pwd_price').send_keys('500000')
        driver.find_element_by_xpath('//*[@id="J_ajax_submit_btn"]').click()#点击提交
        sleep(10)
        driver.find_element_by_xpath('//*[@id="e_hr_getMsgCode"]').click()#获取验证码
        driver2 = webdriver.Chrome()  # 打开第二个浏览器验证码
        driver2.get('http://203.110.167.196:9082/usercenter/msgCode.html')
        driver2.implicitly_wait(10)
        driver2.find_element_by_xpath('//*[@id="verificationCode_txt"]').send_keys(self.username)  # 输入号码
        driver2.find_element_by_xpath('//*[@id="verificationCode_btn"]').click()  # 查询
        yzm = driver2.find_element_by_xpath('//*[@id="verificactionCode"]/tbody/tr[1]/td[3]').text
        driver.find_element_by_xpath('//*[@id="e_hr_msgCode"]').send_keys(yzm)  # 输入验证码
        driver.find_element_by_xpath('//*[@id="hr_fake_pwd1"]').click()
        for i in range(6):
            driver.find_element_by_xpath('//*[@id="NumberKeyboard___100"]').click()
        sleep(3)
        driver.get_screenshot_as_file(u'screen_shot/%s/免密设置.png'%self.now_time)
        driver.quit()
        driver2.quit()
if __name__ == '__main__':
        unittest.main()
