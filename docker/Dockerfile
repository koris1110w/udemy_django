# python:3.8の公式 image をベースの image として設定
FROM python:3.12

# 作業ディレクトリの作成
RUN mkdir /nazoapp

# 作業ディレクトリの設定（以後の RUN は WORKDIR で実行）
WORKDIR /nazoapp

# カレントディレクトリにある資産をコンテナ上の指定のディレクトリにコピーする
ADD nazodb /nazoapp

# pipでrequirements.txtに指定されているパッケージを追加する
RUN pip install -r requirements.txt

# 起動(今回はなし)
# CMD python3 manage.py runserver 0.0.0.0:8000
