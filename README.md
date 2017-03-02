CNNを用いたカラースケッチに基づくイラスト検索
======================
卒業論文研究です.  
  
マウスなどで短時間で大まかに描いたカラースケッチに基づいて,データベースにある同じ構図のキャラクターのイラストを検索するモデルです．語句による検索のできない構図の指定ができて,検索の幅が広がります．  
  
卒論の時間の関係で,CNNの学習には1000枚のイラスト(dataset from:[nico-opendata](https://nico-opendata.jp/ja/seigadata/index.html))しか使用していません．  
  
### 実験の流れ
1. 1000枚のデータセットから20枚のイラストを目標イラストとして選び出す．  
2. 目標イラストを検索するためのクエリスケッチをユーザに描いてもらう．  
3. 計500枚のクエリスケッチを提案モデルで検索し，目標イラストがTOP3（またはTOP5、TOP10）に入っていましたら「正解」とカウントする． 
4. 正解率を計算する．  
  
### クエリスケッチの作成の要求
ツール：マウス，ペンタブなど  
ソフト：Windows のペイント  
サイズ：450 ピクセル×450 ピクセル  
作成時間：最大5 分/枚（1、2 分/枚が望ましい）  

  
検索例
----------------

### クエリスケッチの例1
 <img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/user_query/origin_query/userquery01/01.jpg" width="100px">  
  
### 検索結果のTOP5
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/1.67.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/2.84.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/3.54.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/4.93.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user01/01/5.10.jpg" width="100px">  
  
### クエリスケッチの例2
 <img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/user_query/origin_query/userquery25/09.png" width="100px">  
  
### 検索結果のTOP5
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/1.451.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/2.496.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/3.487.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/4.465.jpg" width="100px">
<img src="https://github.com/La4La/Color-Sketch-Based-Illustration-Retrieval-Using-CNN/blob/master/search/search_result/user25/09/5.468.jpg" width="100px">  
