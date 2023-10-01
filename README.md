# INA226_Library


## serviceの自動起動の登録の方法

サービス定義ファイルの配備

＊ 本リポジトリをルート直下にあることを仮定としたコマンドです．リポジトリをcloneした場所に応じて変更してください
```bash
sudo ln -s ~/INA226_lib/INA226VoltAndCurrent.service /etc/systemd/system/INA226VoltAndCurrent.service
```

### サービスの自動起動の登録
```bash
sudo systemctl enable INA226VoltAndCurrent.service
```

### サービスの起動
```bash
sudo systemctl start INA226VoltAndCurrent.service
```

### サービスの起動確認
```bash
sudo systemctl status INA226VoltAndCurrent.service
```

### シリアライズされた状態のログファイルを直接確認する方法
- 以下を実行するとファイルロックを取得した上で直接catされる。パイプ等でよしなにしてください。
```bash
./read_log_data_with_flock.sh
```

### ログデータのcsvへの変換
- 以下を実行すると このプログラムを実行したディレクトリのvol_and_cur_data.csvにcsvが出力される
```bash
python3 pyfiles/read_log_data.py
```

### 一番直近で取得したセンサ値の表示
```bash
python3 pyfiles/read_latest_data.py
```

### ロボットに保存されているログデータを手元のPCに持ってくる方法
- 以下を実行すると、対象ロボットのログをcsvとして手元のPCに持ってくる
- 対象のロボットのid（必須）と、出力ファイル名（任意）を指定する
- wifi経由でsshが出来る状態である必要がある。また、sshpassをインストールしておく必要がある

```bash
./get_ina_data_from_robot.py [robot_id] [output_filename(optional)]
```
