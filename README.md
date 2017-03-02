CNNを用いたカラースケッチに基づくイラスト検索
======================
卒業論文研究です.  
  
マウスなどで短時間で大まかに描いたカラースケッチに基づいて,データベースにある同じ構図のキャラクターのイラストを検索するモデルです．語句による検索のできない構図の指定ができて,検索の幅が広がります．  
  
卒論の時間の関係で,CNNの学習には1000枚のイラスト(dataset from:[nico-opendata](https://nico-opendata.jp/ja/seigadata/index.html))しか使用していません．  
  
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
