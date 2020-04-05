# %%
import os
import sys
import urllib
import time
import pandas as pd
import requests

# %% 設定
index_file = 'index.csv'    # インデックスファイル名
dl_dir = 'scripts'          # 台本保存先ディレクトリ名
overwrite = False           # ファイルが存在したら上書きするか
max_count = 500             # 最大ダウンロード数
interval = 2                # ダウンロード間の待ち時間 (秒)

# %% インデックスファイルを読み込む
df = pd.read_csv(index_file)

# script_id と url だけにする
df = df.loc[:, ['script_id', 'url']]

# %% 件数を表示
print(f'Total: {len(df)} scripts')

# %% 保存先ディレクトリのチェック

# この .py ファイルのディレクトリ のパス
cur_dir_path = os.path.dirname(os.path.abspath(__file__))

# 保存先ディレクトリのパス
dl_dir_path = os.path.join(cur_dir_path, dl_dir)

# 保存先ディレクトリと同名のファイルがあれば中断
if os.path.isfile(dl_dir_path):
    print(f'ファイル {dl_dir} を削除してやり直してください。')
    sys.exit()

# 保存先ディレクトリがなければ作る
if not os.path.isdir(dl_dir_path):
    os.makedirs(dl_dir_path)

# %% 一括ダウンロード
count = 0
for row in df.itertuples():
    script_id = int(row.script_id)
    
    # 保存先ファイル名
    save_name = f'{script_id:06}.txt'
    save_path = os.path.join(dl_dir_path, save_name)
    
    # 存在したらスキップする
    if os.path.exists(save_path) and not overwrite:
        continue
    
    # ダウンロード用の POST リクエストを準備する
    cgi_path = f'scriptdl.cgi/{script_id}.txt'
    action_url = urllib.parse.urljoin(row.url, cgi_path)
    data = {'script': str(script_id), 'type': 'win'}
    
    # ネットワーク負荷を考慮して待ち時間を入れる
    if count > 0:
        time.sleep(interval)
    
    # リクエストして結果をテキストで得る
    response = requests.post(action_url, data=data)
    # encoding が正しく判定されないので直に指定する
    response.encoding = 'sjis'
    
    # テキストを保存する
    with open(save_path, mode='w', encoding='utf-8', newline='') as f:
        f.write(response.text)
    
    count += 1
    print(f'{count}: {save_name} を保存しました。')
    
    # 上限に達したら終了
    if count >= max_count:
        break

# %% 終了メッセージ
print(f'ダウンロードが終わりました ({count}件) 。')
