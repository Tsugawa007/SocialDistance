# 学生でも作成できる！お手軽SocialDistanceプログラム
AI X CORE　を使用して、30秒間のSocialDistanceを計測するプログラム

# AI X COREとは？
:https://jellyware.jp/aicorex/




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



# 実行手順
[注意]
このプログラムは、AI X CORE(デバイスは"MYRIAD"、OpenVinoのversionは"2020年1")を使用した、Social＿Distanceプログラムです。
よって、デバイス、OpenVinoのversionが異なると、使用するAIモデル、AIモデルのSettingのコードを変更する必要があります。
その点を、踏まえてコードをご覧になって頂くと、幸いです。

1.2個のAIモデル(.xml ファイル、.binファイル)をDownloadします。
```
# Download model(person-detection-retail-0013) into a directory
curl --create-dirs https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/person-detection-retail-0013/FP16/person-detection-retail-0013.xml https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/person-detection-retail-0013/FP16/person-detection-retail-0013.bin -o model/person-detection-retail-0013.xml -o model/person-detection-retail-0013.bin

# Download model(person-reidentification-retail-0200) into a  directory
https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/person-reidentification-retail-0200/FP16/person-reidentification-retail-0200.xml https://download.01.org/opencv/2020/openvinotoolkit/2020.1/open_model_zoo/models_bin/1/person-reidentification-retail-0200/FP16/person-reidentification-retail-0200.bin -o model/person-reidentification-retail-0200.xml -o model/person-reidentification-retail-0200.bin
```
2.sample.pyの20行目の"$(pwd)"をカレントディレクトリのフルパスに書き換えます。

3.sample.pyの28行目の"Social_parameter"をカスタマイズします。
実際のSocialDistanceの距離ではなく、画像のx、y座標の距離となっています。
なので、実際に動かしながら、調整をしていただきたいです。


