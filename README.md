# Docker勉強会用Djangoサンプル

## 概要

DB上に数値を格納し、インクリメントしていく機能のみを持つdjangoのプロジェクト

## リポジトリ

| 名称 | URL | 備考 |
| :-- | :-- | :-- |
| ソースコードリポジトリ | https://github.com/northtorch/django-docker | ソースコードを管理するリポジトリ |


## 開発環境

| 項目 | 値 | 備考 |
| :-- | :-- | :-- |
| 開発言語 | python | バージョン3.10（annotationの都合上） |
| パッケージ管理 | poetry | |
| 開発環境 | vscode | リポジトリ上のcode-workspaceにて開発を行うこと | 
| フォーマッタ | black | https://github.com/psf/black |
| 型チェック | mypy | https://github.com/python/mypy |
| DocString | Googleスタイル | vscodeの拡張機能autoDocstringで生成する |
| Unit Test | PyTest | vscode統合済み |

# 開発環境の構築

## 前提条件

- poetryインストール済み（ https://python-poetry.org/docs/#installation ）
- pyenv等で開発用のpythonバージョンが使用可能になっている
- Windows WSL2 ( Ubuntu 20.04LTS )上での環境構築を想定  
  それ以外の環境の場合、セットアップ手順のコマンド等を適宜読みかえること
- vscodeインストール済み

## セットアップ手順

1. 必要なバージョンの Python をインストール

    pyenvを使用して Python 3.10系をインストールする

    ```
    pyenv install 3.10.8
    ```

1. ソースコードをクローンし、クローンしたディレクトリに降りる

    ```
    git clone https://github.com/northtorch/django-docker.git
    cd django-docker
    ```

1. Python仮想環境を構築する

    poetryで、pyenvでインストールしたPythonを指定する
    
    ```
    poetry env use 3.10.8
    ```

    仮想環境をプロジェクト配下に作成するようにpoetryを設定

    ```
    poetry config virtualenvs.in-project true
    ```

    必要なパッケージをインストール

    ```
    poetry install
    ```

1. djangoの設定ファイルをコピー

    ```
    cp core/local_settings.py.org core/local_settings.py
    ```

1. djangoのSECRET_KEYを作成

    ```
    poetry run python get_random_secret_key.py
    ```

    生成された SECRET_KEY を local_settings.py 内の SECRET_KEY に上書き

    ```
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = ''
    ```

1. vscodeのワークスペースファイルをコピー

    ```
    cp django-docker.code-workspace.org django-docker.code-workspace
    ```

1. vscodeでワークスペースを開く

    ```
    code django-docker.code-workspace
    ```

    以降、vscodeのコマンドパレットで実行する

1. migrationの実行

    ```
    poetry run python manage.py migrate
    ```

# 機能

## djangoコマンド

djangoのコマンドとして内部の数値をインクリメントするコマンドを実装済み

```
python manage.py increment
```

## インクリメント用のWebページ

POSTリクエストで内部の数値をインクリメントするページを実装済み

```
python manage.py runserver
```

上記実行後、ブラウザで http://127.0.0.1:8000/ にアクセス