django-twopy - twopy wrapper for Django
============

このモジュールは、Pythonistaのための2chライブラリであるのtwopyのDjangoラッパーです。
2chのスレッドやコメントをDjangoモデルとして保存・利用することができます。

動作環境
============

以下の環境での動作を確認済みです。

* Django >= 1.4
* twopy >= 0.4.0
* django-taggit >= 0.1.0

インストール
============

1 `django-twopy`のインストール

```
$ cd <downloaded dir>
$ python setup.py install
```

2 settings.pyの`INSTALLED_APPS`に`django_twopy`を追加する

```
INSTALLED_APPS = (
    ...
    'djtwopy',
)
```

3 url.pyにURLconfをインクルードする

```
url(r'^djtwopy/', include('djtwopy.urls')),
```

4 データベースにModelを登録する

```
$ python manage.py migrate djtwopy
```

著者
============
twopyについては以下を参照ください。
django_twopyではshogo82148氏によるコードの利用を想定しています。

* オリジナルのコード(rezoo氏): [CodeRepos](http://coderepos.org/share/browser/lang/python/twopy)
* 改修版(shogo82148氏): [github](https://github.com/shogo82148/twopy)
