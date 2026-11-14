# ホテル収益管理ワークショップ

[English](README.md)

需要、残室数、顧客の支払意思額によって、最適な提示価格がどう変わるかを学びます。
販売が成立するたびに残室が 1 室減り、その部屋は在庫に戻りません。
架空の入力だけを使い、最適価格表の作成と条件間の比較までを行います。

## 3 つの Notebook

| Notebook | 役割 |
| --- | --- |
| `01_synthetic_scenario_setup.ipynb` | シナリオを選び、新しい実行フォルダを作成する |
| `02_scenario_distributions.ipynb` | 支払意思額と到着確率の分布を確認する |
| `03_estimate_optimized_price_table.ipynb` | 最適価格を計算し、需要条件ごとに比較する |

[SKILL.md](SKILL.md) に uv の導入、Python 3.14 の固定環境、全 Notebook の実行、
ローカル JupyterLab の起動、依存パッケージの監査・更新手順をまとめています。
uv 導入後は次のコマンドで環境を作成します。

```bash
uv sync --locked
```

リポジトリのルートで Notebook 01 を実行してください。その後、生成された
**`workshop-run/` 内の 02 と 03** を開き、そのフォルダを作業ディレクトリとして実行します。
コマンドラインから同じ実行フォルダを作成することもできます。

```bash
uv run --locked python scripts/prepare_synthetic.py
```

シナリオごとに新しいフォルダを使用してください。既存のフォルダは上書きしません。

```bash
uv run --locked python scripts/prepare_synthetic.py --scenario scenarios/synthetic_demo.yaml --output workshop-run-second
```

生成される実行フォルダには、Notebook 02〜03、3 種類の入力パラメータファイル、
設定、依存ライブラリの定義が入ります。研究用データ、旧 Python モジュール、
既存のモデル、Notebook の保存済み出力はコピーしません。
Notebook はモデルファイルを読む前に、旧形式の実行設定でないことを確認します。

## リポジトリの構成と各ファイルの役割

```text
.
├── 01_synthetic_scenario_setup.ipynb
├── 02_scenario_distributions.ipynb
├── 03_estimate_optimized_price_table.ipynb
├── README.md / README_JP.md
├── PRACTICAL_SESSION.md / PRACTICAL_SESSION_JP.md
├── SKILL.md
├── pyproject.toml / uv.lock / .python-version
├── requirements.txt
├── scenarios/
│   └── synthetic_demo.yaml
├── python/
│   └── synthetic.py
├── scripts/
│   ├── prepare_synthetic.py
│   └── execute_workshop.py
├── tests/
│   ├── test_pricing.py
│   └── test_synthetic.py
└── runs/
    ├── pricing-workshop/
    │   ├── README.md
    │   ├── scenario.yaml / config.yaml / requirements.txt
    │   ├── execution-report.json / validation.json
    │   ├── model/
    │   ├── result/price_tables.csv
    │   └── fig/distributions/ and fig/pricing/
    └── uv-verification/
        └── README.md / validation.json
```

ルートの Notebook は教材のソースであり、保存済みの実行出力も含んでいます。
各 Notebook の役割は上の表を参照してください。その他のファイルの役割は次のとおりです。

| ファイル・フォルダ | 役割 |
| --- | --- |
| `README.md` / `README_JP.md` | 同じ内容を英語・日本語で説明する導入ガイド |
| `PRACTICAL_SESSION.md` / `PRACTICAL_SESSION_JP.md` | 基準条件の実行から条件変更・再実行・価格表比較までの学生向け手順（英語・日本語） |
| `SKILL.md` | uv による環境構築・実行・監査・Jupyter 起動の手順 |
| `pyproject.toml` / `uv.lock` / `.python-version` | 依存関係の定義、ハッシュ付き固定バージョン、Python の固定バージョン |
| `requirements.txt` | uv.lock から自動出力した配布用の依存関係 |
| `scripts/execute_workshop.py` | 架空データのみの新規フォルダで 01〜03 を実行し、出力を保存する |
| `scenarios/synthetic_demo.yaml` | 客室数、需要、支払意思額、到着時期、価格範囲を定める編集可能な架空の入力設定 |
| `python/synthetic.py` | シナリオの検証、3 種類の入力パラメータの生成、独立した実行フォルダの作成 |
| `scripts/prepare_synthetic.py` | Notebook 01 の代わりに、コマンドラインから実行フォルダを作成する入口 |
| `tests/test_pricing.py` | Notebook 03 の価格計算関数を、独立した小規模問題の解と照合するテスト |
| `tests/test_synthetic.py` | シナリオの検証、生成される入力、実行フォルダの分離、Notebook の構成を確認するテスト |
| `runs/pricing-workshop/README.md` | 保存済みの価格計算結果と図を見るための入口 |
| `runs/pricing-workshop/scenario.yaml` | 保存済みの実行で使った入力設定のスナップショット |
| `runs/pricing-workshop/config.yaml` | その入力設定から生成された実行用設定 |
| `runs/pricing-workshop/requirements.txt` | 保存済みの実行に対応する依存ライブラリのスナップショット |
| `runs/pricing-workshop/execution-report.json` | 保存済みの実行における Notebook 名と実測した実行時間 |
| `runs/pricing-workshop/validation.json` | その実行時点のソースコミットと検証項目の記録。現在のテスト状態を示すものではない |
| `runs/pricing-workshop/model/` | 保存済みの実行で生成した入力と、計算した価格・期待収益の表 |
| `runs/pricing-workshop/result/price_tables.csv` | 需要、リードタイム、残室数ごとの価格と期待収益 |
| `runs/pricing-workshop/fig/distributions/` | 支払意思額と到着分布の保存済みの図 |
| `runs/pricing-workshop/fig/pricing/` | 価格のヒートマップ、推移、基準条件との差分の保存済みの図 |
| `runs/uv-verification/` | uv 環境の検証記録。現在のセキュリティ監査結果を示すものではない |
| `.gitignore` | 生成した `workshop-run*` フォルダ、ローカルの実行環境、キャッシュを Git の管理対象から除外する設定 |

### 生成する実行フォルダと保存済み結果の違い

`workshop-run/` は Notebook 01 または準備用スクリプトを実行すると作成されるフォルダで、
Git 管理対象のソースには含まれません。出力を消去した Notebook 02〜03 のコピー、
`scenario.yaml`、`config.yaml`、`requirements.txt`、`pyproject.toml`、`uv.lock`、`.python-version`、および `model/`、`result/`、`fig/`
が入ります。新しい実験では、新しい実行フォルダを作成してください。

| 生成ファイル | 作成する処理 | 内容 |
| --- | --- | --- |
| `model/opt_table_params.pickle` | セットアップ | 価格範囲の上下限と刻み幅 |
| `model/wtp_parameters.pickle` | セットアップ | 支払意思額の平均と標準偏差 |
| `model/visit_curve.pickle` | セットアップ | 日ごとの到着時期の重み |
| `model/opt_price.pickle` | Notebook 03 | 需要倍率ごとの最適価格表 |
| `model/opt_revenue.pickle` | Notebook 03 | 需要倍率ごとの期待収益表 |
| `result/price_tables.csv` | Notebook 03 | 確認用にまとめた価格・期待収益の表 |
| `fig/distributions/*.png` | Notebook 02 | 入力分布の図 |
| `fig/pricing/*.png` | Notebook 03 | 最適価格の比較図 |

`runs/pricing-workshop/` は過去の実行結果を確認するためにコミットしたスナップショットです。
新しい実行フォルダの生成時に、入力として読み込まれることはありません。
実験条件を変える場合は、このスナップショットではなくシナリオを編集し、新しい実行フォルダを作成してください。

## 実習の進め方

学生向けの手順は [PRACTICAL_SESSION_JP.md](PRACTICAL_SESSION_JP.md)に分離しました。
基準条件を実行し、結果を確認してから、支払意思額の平均を変えて再実行し、最適価格表を比較します。

## 出力と解釈

Notebook 02 は分布図を 2 枚保存します。Notebook 03 は共通の色尺度を使うヒートマップ、
価格の推移、基準需要との差分の比較図を保存します。
残室 0 の状態は販売停止を意味し、ヒートマップの色尺度から除外します。
`result/price_tables.csv` にはすべての価格・期待収益の状態をまとめ、`model/` には
最適価格表と期待収益表を保存します。価格は離散的な候補の中から選ばれます。

この実行経路には、乱数によるシミュレーション、予測精度の比較、返金規定、反復回数の設定はありません。
値は決定論的に計算した期待収益です。
モデルと検証の詳細は、下記の「価格計算モデル」を参照してください。

[保存済みの実行結果](runs/pricing-workshop/README.md) には、実行に用いたシナリオ、表、4 枚の図が含まれます。
ルートの Notebook にも実行出力を保存しています。

## 価格計算モデル

Notebook 01（シナリオ設定）、02（分布の確認）、03（価格計算）の順に進めます。
イベント予測や予約取消のモデルは含まず、成立した販売は確定とします。

### 入力

価格は任意の通貨単位です。到着はベルヌーイ試行で、1 日に最大 1 人とします。範囲外の確率は切り詰めず、エラーにします。

シナリオの項目は `name`、`leadtime`、`capacity`、`wtp`、`price`、`arrival` に限定しています。古い設定が黙って無視されることを
避けるため、想定外の最上位項目はエラーにします。

- `wtp.mean` と `wtp.std` は、正規分布に従う支払意思額の平均と標準偏差です。
- `price.min`、`price.max`、`price.price_interval` は整数の価格候補を定めます。上限は含みません。同点なら最も低い価格を選びます。
- `arrival.log_mean` と `arrival.log_std` は、到着時刻の対数正規分布を定めます。各日の区間 $[t,t+1)$ の確率を積分し、対象期間全体で合計が 1 になるように正規化します。
- `arrival.people` は需要倍率 1 のときの潜在的な到着人数の期待値です。
- 日ごとの到着確率は $a_t = w_t N m$ で、1 以下である必要があります。ここで $w_t$ は到着時期の重み、$N$ は `arrival.people`、$m$ は需要倍率です。倍率は正の値で重複がなく、基準の 1.0 を含む必要があります。
- 生成する入力は価格候補の範囲、支払意思額のパラメータ、到着時期の重みの 3 種類です。乱数シード、反復回数、予測精度の設定はありません。

支払意思額の正規分布は切断していません。支払意思額が負の場合、正の価格では購入しません。
到着時期、支払意思額、価格に対する購入判断は、ここで定めた外生的な仮定に従います。
実際に予約が成立するかどうかは、残室の有無にも依存します。
シナリオの需要倍率は `arrival.mt_multiplier` で設定します。生成される `config.yaml` は従来のフラットな内部形式を維持します。シナリオを編集した後は作業フォルダを再生成してください。


### 最適価格の計算

日ごとの到着確率を $a_t$、価格 $p$ で購入する確率を $d(p) = \Pr(\mathrm{WTP} \geq p)$、
$s(t,p) = a_t d(p)$ とします。$t$ はチェックインまでの日数、$c$ は残室数、$\mathcal{P}$ は価格候補の集合、$V(t,c)$ は将来の最適期待収益です。状態の変化は販売成立（残室が 1 室減る）と不成立（残室が変わらない）のみです。

$$
V(t,c) = \max_{p \in \mathcal{P}} \left(s(t,p)\left[p + V(t-1,c-1)\right] + \left[1-s(t,p)\right]V(t-1,c)\right).
$$

$$
V(t,0) = 0, \qquad V(-1,c) = 0.
$$

実装は Notebook 03 に記載しています。価格候補ごとの購入確率を正規分布の生存関数で一度だけ計算し、
最適化の途中では値を丸めずに保存します。これは、繰り返し数値積分する代わりに同じ正規分布の上側確率を
直接評価する方法です。残室が総客室数と等しい場合の特別な分岐は必要ありません。
残室 0 の価格は、販売停止を表すため無限大としています。

以前の研究モデルのパラメータを無効化したのではなく、状態遷移を絞ったモデルです。
取り除いた仕組みの入力、状態、分岐、補助モジュールの読み込みは、3 つの教材 Notebook と生成パッケージにはありません。

期待収益は、サンプリングした経路から推定するのではなく直接計算します。
以前のシミュレーション・評価 Notebook は実行しません。

### 実行と検証

Notebook 01 はコピー対象を限定し、新しい独立したフォルダを生成します。
Notebook 02・03 と、必要な入力・環境定義だけをコピーします。
古いモデルファイルを誤って使わないよう、02・03 は実行設定の `pricing-workshop-v1` マーカーを確認します。

価格計算のテストでは Notebook 03 に定義した関数を実行します。
独立した 1 期間の計算と小規模な再帰的意思決定木による照合に加えて、需要 0、残室 0、同点処理、
不正な確率を確認します。入力側のテストでは、パラメータファイルが 3 種類だけ生成され、
旧モジュールがコピーされないことを確認します。テストは現在の価格計算ワークショップだけに依存します。

3 つの Notebook は、必要なソースだけを配置した新しい作業フォルダで実行します。
`runs/pricing-workshop/` の保存済み結果にはシナリオ、実行設定、価格・期待収益の表、4 枚の図、実行記録を含みます。
以前のシミュレーション用コード、テスト、モデル、結果、分析資料は削除済みです。

## テスト

```bash
uv run --locked python -m unittest discover -s tests -v
```

教材 Notebook の価格計算関数を独立した小規模問題で検証し、入力の検証、
実行フォルダの分離、Notebook が 3 つであることも確認します。
