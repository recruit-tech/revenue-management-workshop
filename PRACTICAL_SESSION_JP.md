# 実習：ホテルの最適価格を計算して比較する

[English](PRACTICAL_SESSION.md)

上から順番に進めてください。最初に基準条件で実行し、次に一つの条件を変えて再実行して、価格表を比較します。

JupyterLab を使う間、この手順書は GitHub または別のブラウザータブで開いておきます。
詳しい説明は Notebook と [README 日本語版](README_JP.md) を参照してください。

## 1. ファイルを準備して JupyterLab を開く

講師から配布された教材ソースの ZIP をダウンロードして展開するか、アクセス権のあるリポジトリの作業コピーを使います。
`01_synthetic_scenario_setup.ipynb` と `pyproject.toml` があるフォルダでターミナルを開いてください。

uv が未導入の場合は、[uv と固定環境の導入手順](SKILL.md#1-install-uv-and-the-locked-environment)を済ませてから戻ってきてください。
今回の実習では、SKILL.md にある Notebook の自動実行手順は実施しなくて構いません。

ソースのフォルダで、次のコマンドを順に実行します。

```bash
uv sync --locked
uv run --locked python -c "from pathlib import Path; from scripts.execute_workshop import stage_sources; p = Path('workshop-run-student'); p.mkdir(); stage_sources(p)"
uv run --locked jupyter lab --no-browser --ServerApp.ip=127.0.0.1 --ServerApp.port=8888 --ServerApp.port_retries=0 --ServerApp.root_dir="$PWD/workshop-run-student"
```

2 番目のコマンドは、必要なソースだけを含む新しい教材フォルダを作成します。
`workshop-run-student` がすでにある場合は、2 番目と 3 番目のコマンドで別のフォルダ名を指定してください。
残しておきたい結果のあるフォルダは削除しません。このコマンドは macOS/Linux のシェル向けです。Windows では WSL で実行できます。

Jupyter が表示した localhost の URL を、`?token=...` を含めてブラウザーで開きます。
ターミナルは動かしたままにしてください。ポート 8888 が使用中の場合は、最後のコマンドで別の空いているポートを指定します。
JupyterLab に 3 つの Notebook と `scenarios/` フォルダが表示されることを確認してください。

ファイルの役割は、[リポジトリの構成と各ファイルの役割](README_JP.md#リポジトリの構成と各ファイルの役割)を参照してください。

## 2. Notebook 01 で基準条件の実験を作る

1. JupyterLab で `01_synthetic_scenario_setup.ipynb` を開きます。
2. `scenario_path = Path('scenarios/synthetic_demo.yaml')` は変更しません。
3. 最後のコードセルの出力フォルダを、次のように変更します。

   ```python
   output_folder = Path('workshop-run-baseline')
   ```

4. **Run → Run All Cells** を選び、コードセルの実行が終わるまで待ちます。
5. 表示された設定を確認します。客室数は **10**、潜在的な到着人数の期待値は **18**、支払意思額（WTP）の平均は **18,000**、標準偏差は **6,000**、需要倍率は **0.6、1.0、1.2** です。
6. 最後のメッセージに `workshop-run-baseline` が表示されることを確認します。

セルでエラーが出た場合は、解消してから先に進んでください。
出力フォルダがすでにある場合は、新しい名前に変え、以降の手順でもその名前を使います。実験ごとに新しいフォルダが必要です。

各設定の意味は、[入力](README_JP.md#入力)を参照してください。

## 3. Notebook 02 で基準条件の分布を確認する

1. JupyterLab のファイル一覧で **`workshop-run-baseline/`** を開きます。
2. **そのフォルダ内の** `02_scenario_distributions.ipynb` を開きます。
3. **Run → Run All Cells** を選び、実行完了を待ちます。
4. 支払意思額の確率密度と購入確率のグラフを確認します。
5. 到着時期と日ごとの到着確率のグラフを確認します。3 つの需要条件が表示されていることを確かめます。
6. **File → Save Notebook** で保存します。

必要に応じて Notebook の説明を読んでください。モデルの前提は、[価格計算モデル](README_JP.md#価格計算モデル)を参照してください。

## 4. Notebook 03 で基準条件の最適価格を確認する

1. 同じ **`workshop-run-baseline/`** 内の `03_estimate_optimized_price_table.ipynb` を開きます。
2. **Run → Run All Cells** を選び、実行完了を待ちます。
3. **Compare price tables on the same colour scale** の箇所に移動します。
4. ヒートマップと、その下の数値の表を確認します。表の価格は小数点以下を四捨五入して表示します。`Closed` は残室がない状態です。
5. 各需要条件の表で、**チェックインの 30 日前**の行と、**残室 5 室**の列を探します。需要倍率 0.6、1.0、1.2 の価格を比較してください。
6. **Demand x 1** の価格を、下記の比較表の項目に沿って記録します。
7. Notebook を保存し、比較用に開いたままにします。

`remaining_rooms` は変更しません。後半の議論やペア向けの問いは参考として読むだけでよく、今回の実習では取り組む必要はありません。そのまま次へ進んでください。

計算方法は [最適価格の計算](README_JP.md#最適価格の計算)、保存される表や図は [出力と解釈](README_JP.md#出力と解釈)を参照してください。

| 実験 | 支払意思額の平均 | 需要倍率 | チェックインまでの日数 | 残室数 | 確認した最適価格 |
| --- | ---: | ---: | ---: | ---: | --- |
| 基準条件 | 18,000 | 1.0 | 30 | 5 | 手順 4 の後に記録 |
| 支払意思額を上げる | 21,000 | 1.0 | 30 | 5 | 手順 6 の後に記録 |
| 支払意思額を下げる（任意） | 15,000 | 1.0 | 30 | 5 | 手順 7 の後に記録 |

記録には自分のメモを使って構いません。この手順書を編集する必要はありません。
価格候補は離散的なので、条件を変えても価格が変わらないセルもあります。

## 5. 条件を一つ変えて新しい実験を作る

1. JupyterLab のファイル一覧の最上位に戻り、**`scenarios/synthetic_demo.yaml`** をテキストエディターで開きます。
2. 支払意思額の平均だけを 18,000 から 21,000 に変更します。該当箇所を次のようにしてください。

   ```yaml
   wtp:
     mean: 21000
     std: 6000
   ```

3. YAML ファイルを保存します。支払意思額の影響を比較するため、客室数、到着条件、価格候補など、その他の設定は変更しません。
4. **最上位の Notebook 01** に戻ります。`scenario_path` は変更せず、最後のコードセルを次のように変更します。

   ```python
   output_folder = Path('workshop-run-high-wtp')
   ```

5. **Run → Run All Cells** を選びます。表示された平均が **21,000** で、最後のメッセージが `workshop-run-high-wtp` を指すことを確認します。

編集するのは `scenarios/` 内の元の YAML です。既存の実験フォルダにある `scenario.yaml` は保存用の写しです。
その写しを変更したり、03 だけを再実行したりしても入力は再生成されません。
[生成する実行フォルダと保存済み結果の違い](README_JP.md#生成する実行フォルダと保存済み結果の違い)も参照してください。

## 6. 変更した条件で実行して比較する

1. **`workshop-run-high-wtp/02_scenario_distributions.ipynb`** を開きます。
2. 全セルを実行します。支払意思額のグラフがどう変わったかを確認してください。到着条件は変わっていません。
3. **`workshop-run-high-wtp/03_estimate_optimized_price_table.ipynb`** を開きます。
4. 全セルを実行し、**Compare price tables on the same colour scale** に戻ります。
5. **Demand x 1** の **30** の行、**5** の列を探し、基準条件の価格と並べて記録します。
6. 二つの **Demand x 1** の表について、ほかのセルも同じ行・同じ列で比較します。価格が上がった箇所や、変わらなかった箇所を確認してください。
7. 両方の Notebook を保存します。基準条件の結果は `workshop-run-baseline/` に残っています。

両方の実験で同じ価格候補を使っているため、ヒートマップの色尺度の上下限も共通です。正確な価格は数値の表で確認してください。

## 7. 支払意思額の平均を下げてみる（任意）

次の箇所だけを変えて、手順 5〜6 を繰り返します。

- `scenarios/synthetic_demo.yaml` の `wtp.mean` を **15000** にして保存します。
- Notebook 01 で `output_folder = Path('workshop-run-low-wtp')` とします。
- Notebook 01 を実行し、続けて **`workshop-run-low-wtp/` 内の** 02 と 03 を実行します。
- 同じ需要倍率・日数・残室数の価格を記録し、3 条件を比較します。

これで各実験の価格表が別々に保存されました。さらに試す場合も、一度に変える条件は一つにし、新しいフォルダ名で同じ手順を繰り返します。

## 8. 終了する

Notebook を保存します。後から結果を確認したい場合は、実験フォルダを残しておいてください。
終了するときは JupyterLab を起動したターミナルに戻り、**Ctrl-C** を押します。終了確認が出たら確認して停止します。
