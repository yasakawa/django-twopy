# -*- coding: utf-8 -*-
from .models import DtThread, DtComment
import twopy

import logging
logger = logging.getLogger('djtwopy')

def save_thread(thread):
    """ 指定されたスレッドとコメントを保存する
    thread: twopy.threadオブジェクト
    """
    # デバッグ用出力
    logger.debug('Start saving the thread.')
    logger.debug('  title: %s' % thread.title)
    logger.debug('  url  : %s' % thread.url)
    logger.debug('  res  : %s' % thread.getResponse())

    # スレッドを登録する
    dt_thread_prev_res = 0
    dt_thread, created = DtThread.objects.get_or_create(url = thread.url,
                                        defaults = dict(filename = thread.filename,
                                                        title = thread.title ))
    # スレッドの中で res だけは変更されるので都度更新する
    if dt_thread.res != thread.res:
        dt_thread_prev_res = dt_thread.res
        dt_thread.res = thread.res
        dt_thread.save()

    # レス数が更新されている場合は、Commentの取り込みを行う。
    if thread.res > dt_thread_prev_res:
        logger.debug("Retrieving thread : %s" % thread.title)
        thread.retrieve()

        # 該当スレッドについて、保存済みDtCommentオブジェクトのnumberの最大値を求める
        dt_comments = DtComment.objects.filter(thread__exact=dt_thread).order_by('-number')
        if dt_comments:
            max_number = dt_comments[0].number
        else:
            max_number = 0

        # コメントがDBに存在しないときは保存する
        for i in range(max_number+1, thread.res+1):
            comment = thread[i]
            try:
                dt_comment = DtComment.objects.get(thread__exact=dt_thread,
                                                   number__exact=comment.number)
            except DtComment.DoesNotExist:
                try:
                    dt_comment = DtComment()
                    dt_comment.setThread(dt_thread)
                    dt_comment.setComment(comment)
                    dt_comment.save()
                except Exception as e:
                    # コメントのフォーマットが通常と異なる場合は例外がスローされるため
                    # warningとしてハンドリングする（例：このスレッドは1000を超えました）
                    logger.warning(e)

def crawl(board_url, keywords):
    """ スレッドをクロールして、DtThread,DtComment にデータを取り込む。
    board_url : 板のURL (例:http://anago.2ch.net/stock/)
    keywords : 板からスレッドを検索する際のキーワードのリスト (例:['○○ってどうよ', '××ってどうよ'])
    """
    # 板の情報を取得する
    stock_board = twopy.Board(board_url)
    stock_board.retrieve()

    # 板のスレッド一覧から、キーワードを含むスレッドに対して処理を行う
    for thread in stock_board:
        for keyword in keywords:
            if thread.title.find(keyword) > -1:
                save_thread(thread)