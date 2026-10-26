# Docker勉強会用Djangoサンプル

## 概要

DB上に数値を格納し、インクリメントしていく機能のみを持つdjangoのプロジェクト

同じアプリを、次の 3 通りで動かせる。

| 動かし方 | 構成 | 説明 |
| :-- | :-- | :-- |
| 開発環境 | `runserver` | [開発環境の構築](#開発環境の構築) |
| サーバ | nginx + uWSGI + Django | [サーバへの配置](#サーバへの配置) |
| Docker | nginx + uWSGI + Django（Docker Compose） | [Docker で動かす](#docker-で動かす) |

## リポジトリ

| 名称 | URL | 備考 |
| :-- | :-- | :-- |
| ソースコードリポジトリ | https://github.com/northtorch/django-docker | ソースコードを管理するリポジトリ |


## 開発環境

| 項目 | 値 | 備考 |
| :-- | :-- | :-- |
| 開発言語 | python | バージョン3.12 |
| フレームワーク | Django | バージョン5.2 |
| パッケージ管理 | uv | https://docs.astral.sh/uv/ |
| 開発環境 | vscode | リポジトリ上のcode-workspaceにて開発を行うこと |
| リンタ・フォーマッタ | ruff | https://github.com/astral-sh/ruff |
| 型チェック | mypy | https://github.com/python/mypy |
| DocString | Googleスタイル | vscodeの拡張機能autoDocstringで生成する |
| Unit Test | PyTest | vscode統合済み |

# 開発環境の構築

## 前提条件

- uvインストール済み（ https://docs.astral.sh/uv/getting-started/installation/ ）
- Windows WSL2 ( Ubuntu ) 上での環境構築を想定  
  それ以外の環境の場合、セットアップ手順のコマンド等を適宜読みかえること
- vscodeインストール済み

## セットアップ手順

1. ソースコードをクローンし、クローンしたディレクトリに降りる

    ```
    git clone https://github.com/northtorch/django-docker.git
    cd django-docker
    ```

1. Python仮想環境を構築し、必要なパッケージをインストール

    `.python-version` に書かれたバージョンの Python が、`.venv` に用意される（なければ uv がダウンロードする）

    ```
    uv sync
    ```

1. djangoの設定ファイルをコピー

    ```
    cp core/local_settings.py.org core/local_settings.py
    ```

1. djangoのSECRET_KEYを作成

    ```
    uv run python get_random_secret_key.py
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
    uv run python manage.py migrate
    ```

# 機能

## djangoコマンド

djangoのコマンドとして内部の数値をインクリメントするコマンドを実装済み

```
uv run python manage.py increment
```

## インクリメント用のWebページ

POSTリクエストで内部の数値をインクリメントするページを実装済み

```
uv run python manage.py runserver
```

上記実行後、ブラウザで http://127.0.0.1:8000/ にアクセス

# サーバへの配置

nginx の後ろで uWSGI を動かし、uWSGI から Django を呼び出す構成。設定ファイルの例は `deploy/` にある。

| ファイル | 置き場所 | 内容 |
| :-- | :-- | :-- |
| `deploy/uwsgi.ini` | （リポジトリの中のまま使う） | uWSGI の設定 |
| `deploy/django-docker.service` | `/etc/systemd/system/django-docker.service` | uWSGI を systemd のサービスとして動かす設定 |
| `deploy/django-docker.env.example` | `/etc/django-docker.env` | SECRET_KEY やドメイン名など、環境ごとの値 |
| `deploy/nginx.conf` | `/etc/nginx/sites-available/django-docker` | nginx のサイト設定 |
| `core/local_settings.py.production` | `core/local_settings.py` | 本番用の Django の設定（値は環境変数から読む） |

Ubuntu のサーバに、ユーザー `ubuntu` で配置する場合の流れ。ユーザー名やドメイン名が違う場合は、各ファイルを書き換える。

1. 必要なパッケージと uv をインストールし、リポジトリをクローンする

    ```
    sudo apt update
    sudo apt install -y build-essential nginx
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.local/bin/env
    git clone https://github.com/northtorch/django-docker.git ~/django-docker
    cd ~/django-docker
    ```

1. uWSGI も含めてパッケージをインストールし、本番用の設定ファイルをコピーする

    ```
    uv sync --no-dev --group server
    cp core/local_settings.py.production core/local_settings.py
    ```

1. 環境ごとの値を書く（SECRET_KEY は `uv run python get_random_secret_key.py` で作る）

    ```
    sudo cp deploy/django-docker.env.example /etc/django-docker.env
    sudo vi /etc/django-docker.env
    sudo chmod 600 /etc/django-docker.env
    ```

1. DB の作成と、静的ファイルの収集

    ```
    set -a; source <(sudo cat /etc/django-docker.env); set +a
    sudo mkdir -p /var/www/django-docker/static
    sudo chown ubuntu: /var/www/django-docker/static
    uv run python manage.py migrate
    uv run python manage.py collectstatic --noinput
    ```

1. uWSGI をサービスとして起動する

    ```
    sudo cp deploy/django-docker.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now django-docker
    ```

1. nginx のサイト設定を有効にする（`server_name` を自分のドメイン名に書き換える）

    ```
    sudo cp deploy/nginx.conf /etc/nginx/sites-available/django-docker
    sudo vi /etc/nginx/sites-available/django-docker
    sudo ln -s /etc/nginx/sites-available/django-docker /etc/nginx/sites-enabled/
    sudo rm /etc/nginx/sites-enabled/default
    sudo nginx -t
    sudo systemctl reload nginx
    ```

1. https にする場合は、certbot で証明書を取得する（nginx の設定に https の設定が書き足される）

    ```
    sudo apt install -y certbot python3-certbot-nginx
    sudo certbot --nginx -d example.com
    ```

ソースコードを更新したときは、`touch reload/reload` で uWSGI が読み込み直す。

# Docker で動かす

## Docker Compose（nginx + uWSGI + Django）

サーバと同じ構成を、コンテナで動かす。DB（SQLite）と静的ファイルは、Docker のボリュームに保存される。

```
SECRET_KEY=$(uv run python get_random_secret_key.py) docker compose up -d --build
```

上記実行後、ブラウザで http://localhost:8000/ にアクセス

| 環境変数 | 既定値 | 説明 |
| :-- | :-- | :-- |
| SECRET_KEY | （必須） | Django の SECRET_KEY |
| WEB_PORT | 8000 | nginx が待ち受けるポート |
| DJANGO_ALLOWED_HOSTS | localhost,127.0.0.1 | アクセスを受け付けるドメイン名 |
| DJANGO_CSRF_TRUSTED_ORIGINS | （なし） | https でフォームを送るときの送信元（例: https://example.com） |

止めるときは `docker compose down`（ボリュームも消すときは `docker compose down -v`）。

## Docker の実験用スクリプト

Docker 勉強会で使った、イメージの作成とコンテナの実行の例。

| スクリプト | 内容 |
| :-- | :-- |
| `build_server.sh` | Web ページ用のイメージ（uWSGI で 8000 番ポートを待ち受ける）を作る |
| `run_server_01.sh` | Web ページ用のコンテナを動かす。コンテナを消すと DB も消える |
| `run_server_02.sh` | Web ページ用のコンテナを動かす。DB はホストの `db/` に保存される |
| `build_cmd.sh` | `increment` コマンド用のイメージを作る |
| `run_cmd_01.sh` | `increment` コマンドを実行する。コンテナを消すと DB も消える |
| `run_cmd_02.sh` | `increment` コマンドを実行する。DB はホストの `db/` に保存される |
| `clear_db.sh` | ホストの `db/` の DB を消す |
