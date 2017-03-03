CNNを用いたカラースケッチに基づくイラスト検索
======================
卒業論文研究です.  
  
マウスなどで短時間で大まかに描いたカラースケッチに基づいて,データベースにある同じ構図のキャラクターのイラストを検索するモデルです．語句による検索のできない構図の指定ができて,検索の幅が広がります．  
  
卒論の時間の関係で,CNNの学習には1000枚のイラスト(dataset from:[nico-opendata](https://nico-opendata.jp/ja/seigadata/index.html))しか使用していません．  
  
### CNN
+ DenseNetをベースにしている  
+ 特徴抽出のために局所平均プーリングを使っている  
+ 特徴を2進数に変換し，ハミング距離で類似度を比較する  
  
### 検索モデル
+ 準備段階：CNN の学習とデータセットにあるイラストの特徴ベクトルの保存  
+ 第一段階：推定ラベルによる検索範囲の絞り（coarse-level 検索）
+ 第二段階：特徴ベクトルの類似度による順位付け（fine-level 検索）
  

実験
----------------
  
### 実験の流れ
1. 1000枚のデータセットから20枚のイラストを目標イラストとして選び出す．  
2. 目標イラストを検索するためのクエリスケッチをユーザに描いてもらう．  
3. 計500枚のクエリスケッチを提案モデルで検索し，目標イラストがTOP3（またはTOP5、TOP10）に入っていましたら「正解」とカウントする． 
4. 正解率を計算する．  
  
### 検索例  
+ クエリスケッチの例1  
 <img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/user_query/origin_query/userquery01/01.jpg" width="100px">  
+ 検索結果のTOP5  
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/1.67.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/2.84.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/3.54.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/4.93.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/5.10.jpg" width="100px">  
  
+ クエリスケッチの例2  
 <img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/user_query/origin_query/userquery25/09.png" width="100px">  
+ 検索結果のTOP5  
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/1.451.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/2.496.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/3.487.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/4.465.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/5.468.jpg" width="100px">  
