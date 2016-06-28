#coding: utf-8
import datetime
import xadmin
import time
import commands
from xadmin import views
from models import Pj_host
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
from xadmin.util import User

from django.utils.encoding import force_unicode
from django.conf import settings
from xadmin.views.base import filter_hook, ModelAdminView, csrf_protect_m
from xadmin.plugins.actions import BaseActionView


class LoginSetting(object):
    title = u"Saltman"


class BaseSetting(object):
    use_bootswatch = True


class GlobalSetting(object):
    site_title = u'Saltman'
    site_footer = u'cyou-inc.com'
    apps_label_title = {'app': u'主机管理', 'auth': u'权限管理'}
    menu_style = 'accordion'


class MaintainInline(object):
    model = Pj_host
    extra = 1
    style = 'accordion'


class PreUpdateAction(BaseActionView):
    action_name = "preupdate"
    description = u'系统初始化'
    icon = 'fa fa-cog fa-spin fa-2x'

    @filter_hook
    def do_action(self, queryset):
        n = queryset.count()
        ipl = []
        for ip in queryset:
            ipl.append(ip.op_addr)
        if n >= 1:
            ipl = queryset[0].op_addr
            self.message_user(u'{0}台服务器初始化进行中，请耐心等待几分钟!'.format(n), 'success')



class SshCmdAction(BaseActionView):
    action_name = "sshcmd"
    description = u'执行命令'
    icon = 'fa fa-refresh fa-spin fa-2x'

    @filter_hook
    def do_action(self, queryset):
        n = queryset.count()
        if n >= 1:
            cmd = queryset[0].pj_cmd
            ret = commands.getoutput(cmd)
            dt = '<pre>' + ret + '</pre>'
            self.message_user(u'命令结果如下: \n  {0}'.format(dt), 'success')


class AutoFdiskAction(BaseActionView):
    action_name = "autofdisk"
    description = u'自动分区'
    icon = ' fa fa-spinner fa-spin fa-2x'

    @filter_hook
    def do_action(self, queryset):
        n = queryset.count()
        if n >= 1:
            dkl = queryset[0].pj_disk
            self.message_user(u'分区盘符:{0}'.format(dkl), 'warning')


class Pj_hostAdmin(object):
    fields = ('pj_name', 'idc_type', 'op_addr', 'pj_cmd', 'pj_disk', 'pj_status')
    list_display = ('pj_name', 'idc_type', 'op_addr', 
                    'pj_cmd', 'pj_disk', 'pj_status',
                    'pj_led')
    list_display_links = ('id', 'pj_name')
    list_filter = ['pj_name', 'idc_type', 'op_addr', 'pj_status', 'pj_led']
    search_fields = ['pj_name', 'idc_type', 'op_addr', 'pj_status', 'pj_led']
    list_per_page = 20
    grid_layouts = ('table', 'thumbnails')
    actions =[PreUpdateAction, SshCmdAction, AutoFdiskAction]
    list_editable = ('pj_cmd', 'pj_disk')

    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.pj_led = User.objects.get(username=request.user).first_name
        obj.save()


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(Pj_host, Pj_hostAdmin)
