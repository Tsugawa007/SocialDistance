# 学生でも作成できる！お手軽SocialDistanceプログラム
AI X CORE　を使用して、30秒間のSocialDistanceを計測するプログラム



# 特徴

瞬間的にSocialDistanceを違反したら緑色、30秒間違反したら赤くなります。

静止画
![静止画](https://github.com/AAEEON/SocialDistance/blob/master/shot.png)


# AIモデルについて

Intelの二つのAIモデルを使用した。

人間識別    person-detection-retail-0013

個別識別    person-reidentification-retail-0200


# 工夫した点

モザイク処理をかけた

瞬間的な検知だけではなく、一定時間の検知も行いました。



# 今後改善したいところ

既存のAIモデルを使用すると、精度に限界がある。

また、SocialDistaceの計算方法も、単純なユークリッド行列距離をしています。



# 使用手順
1.2個のAIモデル(.xml ファイル、.binファイル)をDownloadします。
```
# Download model(person-detection-retail-0013) into a directory
curl --create-dirs https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/person-detection-retail-0013/FP16/person-detection-retail-0013.xml https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/person-detection-retail-0013/FP16/person-detection-retail-0013.bin -o model/person-detection-retail-0013.xml -o model/person-detection-retail-0013.bin

# Download model(person-reidentification-retail-0200) into a  directory
https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/person-reidentification-retail-0200/FP16/person-reidentification-retail-0200.xml https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/person-reidentification-retail-0200/FP16/person-reidentification-retail-0200.bin -o model/person-reidentification-retail-0200.xml -o model/person-reidentification-retail-0200.bin
```

