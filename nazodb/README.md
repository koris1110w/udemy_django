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