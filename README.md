# INA226_Library


## serviceの自動起動の登録の方法

サービス定義ファイルの配備

＊ 本リポジトリをルート直下にあることを仮定としたコマンドです．リポジトリをcloneした場所に応じて変更してください
```bash
sudo ln -s ~/INA226_lib/INA226VoltAndCurrent.service /etc/systemd/system/INA226VoltAndCurrent.service
```

サービスの自動起動の登録
```bash
sudo systemctl enable INA226VoltAndCurrent.service
```

サービスの起動
```bash
sudo systemctl start INA226VoltAndCurrent.service
```

サービスの起動確認
```bash
sudo systemctl status INA226VoltAndCurrent.service
```
