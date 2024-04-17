### nazodb

```
SCSSのコンパイルについて
node V20.11.1 が今の最新のLTSです。
cd static
npm install

# 自動監視&CSSにコンパイル
npm run watch
```


```
docker-compose build
docker-compose up
```

### djangoのコマンドを使いたい時
```
docker-compose exec app bash
```


```
postgresのバージョンが変わったので
docker-compose down -v #ボリューム削除で完全に削除してから立ち上げる
```


### 本番環境のデプロイ手順
```
初回のssh接続
ssh root@IPアドレス

Vimエディターの場合
i # 編集可能に
escボタン # 編集できない
:wq # 上書き保存
:q! # 編集を無視して終了
1


ubuntu SSH設定
Ubuntu 20.4
1.  adduser shuhei
2.  usermod -aG sudo shuhei
3.  vim /etc/ssh/sshd_config  # permit login no　変更 #rootログインは推奨されないので、アクセスできない設定にする
4.  systemctl reload sshdlogout
 失敗する場合sudo apt install openssh-server systemctl reload ssh
5.  logout
6.  sudo ufw allow ssh # 22番ポートでデフォルトで許可されてる
7.  sudo ufw enable

sudo ufw status
sudo ufw allow http or 80
sudo ufw deny ＜ポート番号＞
sudo ufw reload

Dockerの場合
sudo apt-get update
curl -fsSL https://get.docker.com -o get-docker.sh1
sh ./get-docker.sh1
-----------------
インストールできなかったら
sudo apt upgrade
docker --version
------------------
sudo systemctl start docker
sudo systemctl status docker.service
sudo systemctl enable docker
sudo curl -L https://github.com/docker/compose/releases/download/1.23.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
sudo apt-get install git

https://github.com/settings/ssh で下記で取得したssh Keyを登録する
Gitのssh
mkdir ~/.ssh
cd ~/.ssh
ssh-keygen -t rsa
cat id_rsa.pub

cd /home/<ユーザー名>
git clone ..

# 必要ないのでdockerのインストールフォルダは消す
rm -r get-docker.sh1ls

```