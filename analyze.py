# %% 
import os
import matplotlib.pyplot as plt

# %% 設定
datasets = ['hariko/scripts',]

# %% "「" を含む行数をカウントする関数
def count_kakko(f_path):
    '''行数と "「" を含む行数を取得する
    
    parameters
    ----------
    f_path : str
        調査するファイルのパス名
    
    returns
    -------
    lines : int
        ファイルの行数
    lines_with_kakko
        "「" を含む行数
    '''
    
    lines = 0
    lines_with_kakko = 0
    with open(f_path, encoding='utf-8') as f:
        while True:
            l = f.readline()
            if not l:
                break
            if '「' in l:
                lines_with_kakko += 1
            lines += 1
    return (lines, lines_with_kakko)

# %% すべてのファイルについて調べる
params = []
for set_dir in datasets:
    files = os.listdir(path=set_dir)
    for f in files:
        f_path = os.path.abspath(os.path.join(set_dir, f))
        if os.path.isfile(f_path):
            params.append(count_kakko(f_path))

# %% 可視化する
(x, y) = zip(*params)
plt.scatter(x, y)
