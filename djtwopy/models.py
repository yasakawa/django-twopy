# -*- coding: utf-8 -*-
import re
import pytz
import unicodedata
from django.db import models
from django.conf import settings
import twopy
from taggit.managers import TaggableManager

USE_TZ = getattr(settings, 'USE_TZ', True)

# DtComment.body_cleaned()でbodyから削除する文字列
REMOVE_TEXTS = ['(deleted an unsolicited ad)']


class DtThread(models.Model):
    url = models.CharField('URL', max_length=128, default='')
    filename = models.CharField('Filename', max_length=128)
    title = models.CharField('Title', max_length=128, blank=True)
    res = models.IntegerField('ResNumber', null=False, blank=False, default=0)
    tags = TaggableManager()

    """ for System Management """
    date_created = models.DateTimeField('Created Date', auto_now_add=True)
    date_updated = models.DateTimeField('Updated Date', auto_now=True)

    def thread_id(self):
        return self.filename.replace('.dat', '')

    def get_comment(self, number):
        return DtComment.objects.get(thread__exact=self, number__exact=number)


class DtComment(models.Model):
    """
    thread : コメントが保存されている親スレッドのインスタンス
    line   : 初期化に用いられる、datファイルの一行.
             この引数はunicode型でなければなりません.
    number : スレッドからの、コメント位置.
    """
    thread = models.ForeignKey('DtThread', related_name='comments')
    number = models.IntegerField('Number', null=True, blank=True)
    line = models.CharField('Line', max_length=4096, blank=True)
    name = models.CharField('Name', max_length=128, blank=True)
    mailaddr = models.CharField('Name', max_length=128, blank=True)
    datestr = models.CharField('Name', max_length=32, blank=True)
    # bodyを利用する際は、特定の文字列が除去されたbody_cleaned()の利用も検討ください
    body = models.TextField('Body', max_length=4096, blank=True)
    datetime = models.DateTimeField('Posted Date', blank=True)
    user_id = models.CharField('ID', max_length=64, blank=True)
    be = models.CharField('BE', max_length=64, null=True, blank=True)
    tags = TaggableManager()

    """ Custom Fields """
    body_html = models.TextField('Body(HTML)', max_length=8192, blank=True)

    """ for System Management """
    date_created = models.DateTimeField('Created Date', auto_now_add=True)
    date_updated = models.DateTimeField('Updated Date', auto_now=True)

    __urls = re.compile(r"(ttps?:\/\/[-_.!~*'()a-zA-Z0-9;/?:@&=+$,%#]+)")
    __response = re.compile((r"(>>\d{1,4}|＞＞[０-９]{1,4})"
                              "(-\d{1,4}|−[０-９]{1,4}|)"))

    def body_cleaned(self):
        """ bodyからREMOVE_TEXTSを削除した文字列を返す """
        retstr = self.body
        for remove_text in REMOVE_TEXTS:
            retstr = retstr.replace(remove_text, '')
        return retstr

    def setThread(self, thread):
        """ bbs2ch.Threadのインスタンスを引数で受けてメンバを初期化する """
        self.thread = thread

    def setComment(self, comment):
        """ twopy.Commentのインスタンスを引数で受けてメンバを初期化する """
        self.number = comment.number
        self.line = comment.line
        self.name = comment.getName()
        self.mailaddr = comment.getMailAddr()
        self.datestr = comment.getDate()
        self.body = comment.getBody()
        # Django 1.4からはTimeZoneの情報を付与する必要がある。
        # JSTの情報を付与するときは、replaceではなくlocalizeを使う必要がある。
        # http://nekoya.github.io/blog/2013/07/05/python-datetime-with-jst/
        if USE_TZ == True:
            jst = pytz.timezone('Asia/Tokyo')
            self.datetime = jst.localize(comment.getDatetime())
        else:
            self.datetime = comment.getDatetime()
        self.user_id = comment.getID()
        self.be = comment.getBe()
        self.body_html = ""

    def __extractResponses(self):
        """
        オリジナル版から __responses_cache の機能を除いている。
        """
        result = DtComment.__response.finditer(self.body_cleaned())
        l = [(r.group(1), r.group(2)) for r in result]
        return l

    def extractResponsesAsInteger(self):
        """
        コメントの内容からレスポンスの一覧を抽出し、整数のリストとして返します.
        """
        l = self.__extractResponses()
        rl = []
        for i in l:
            start = int(unicodedata.normalize("NFKC", i[0][2:]))
            if i[1] == "":
                rl.append(start)
            else:
                end = int(unicodedata.normalize("NFKC", i[1][1:]))
                rl += range(start, end + 1)
        return rl

    def extractResponsesAsComment(self):
        """
        コメントの内容からレスポンスの一覧を抽出し、コメントのリストとして返します.
        """
        rl = self.extractResponsesAsInteger()
        rl2 = []
        for i in rl:
            if type(i) == int:
                if 0 < i <= self.thread.res:
                    rl2.append(self.thread.get_comment(i))
                else:
                    pass
                    # rl2.append([self.thread.get_comment(i) for j in i if 0 < j <= self.thread.res])
                return rl2
            else:
                raise TypeError

    def render(self):
        """
        取得したコメントから、整形された文章を返します.
        """
        if self.be:
            header = "%i 名前:%s [%s]: %s ID:%s BE:%s" % \
                (self.number, self.name, self.mailaddr, self.date, self.ID, self.be)
        else:
            header = "%i 名前:%s [%s]: %s ID:%s" % \
                (self.number, self.name, self.mailaddr, self.date, self.ID)
        return "%s\n%s\n" % (header, self.body_cleaned())

    class Meta:
        index_together = (("thread", "number"),)

        unique_together = (("thread", "number"),)
