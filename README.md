# 学生でも作成できる！お手軽SocialDistanceプログラム
AI X CORE　を使用して、30秒間のSocialDistanceを計測するプログラム

#特徴

瞬間的にSocialDistanceを違反したら緑色、30秒間違反したら赤くなります。

#AIモデルについて

Intelの二つのAIモデルを使用した

人間識別    person-detection-retail-0013

個別識別    person-reidentification-retail-0200


#工夫した点

モザイク処理をかけた

瞬間的な検知だけではなく、一定時間の検知も行った

#今後改善したいところ

既存のAIモデルを使用すると、精度に限界がある。

また、SocialDistaceの計算方法も、単純なユークリッド行列距離をしています。
