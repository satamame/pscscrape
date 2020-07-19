# %%
import os
import glob
import shutil

# %% 設定
src_dir = 'scripts'     # 入力ディレクトリ名
dest_dir = 'cleaned'    # 出力ディレクトリ名

# 区切り行
delimiter = '　---------------------------------------------'

# %% 準備

# この .py ファイルのディレクトリ のパス
cur_dir_path = os.path.dirname(os.path.abspath(__file__))

# 入力ディレクトリのパス
src_dir_path = os.path.join(cur_dir_path, src_dir)

# 出力ディレクトリのパス
dest_dir_path = os.path.join(cur_dir_path, dest_dir)

# 出力ディレクトリがなければ作る
if not os.path.isdir(dest_dir_path):
    os.makedirs(dest_dir_path)
# 出力ディレクトリがあれば空にする
else:
    ptn = os.path.join(dest_dir_path, '*.txt')
    for f in glob.glob(ptn):
        os.remove(f)

# %% メインループ

count = 0

# 入力ディレクトリ内をループ
for entry in os.scandir(path=src_dir_path):
    # 入力/出力ファイル名
    inf = os.path.join(src_dir_path, entry.name)
    outf = os.path.join(dest_dir_path, entry.name)
    
    # 入力ファイルから行を取り出しリストにする
    with open(inf, encoding='utf_8_sig') as f:
        lines = [l.rstrip() for l in f]
    
    # 連続する区切り行を削除
    for i in range(len(lines) - 1, 0, -1):
        if lines[i] == lines[i - 1] == delimiter:
            del lines[i]

    # 連続する空行を削除
    for i in range(len(lines) - 1, 0, -1):
        if lines[i].strip() == lines[i - 1].strip() == '':
            del lines[i]

    # 区切り行の位置を取得
    delimiter_idxs = [i for i,l in enumerate(lines) if l == delimiter]
    
    
    if len(delimiter_idxs) < 2:
        print(f'{entry.name}: 区切り行がないのでそのまま保存します。')
        shutil.copy(inf, outf)
        # 処理件数表示
        if count % 100 == 0:
            print(count)
        count += 1
        continue
    
    # 区切り行の (-2) 番目～ (-1) 番目を本文とする
    lines = lines[delimiter_idxs[-2] + 1 : delimiter_idxs[-1]]
    
    # 先頭の空行を削除
    if lines[0].strip() == '':
        lines = lines[1:]

    # 末尾の空行を削除
    if lines[-1].strip() == '':
        lines = lines[:-1]
    
    # 残りを改行つきで出力
    with open(outf, 'w', encoding='utf-8') as f:
        f.writelines([l + '\n' for l in lines])

    # 処理件数表示
    if count % 100 == 0:
        print(count)
    count += 1

# %% 完了

print('処理が終わりました。')
