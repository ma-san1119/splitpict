# -*- coding: utf-8 -*-
"""
卒業アルバムの画像ファイルから, ひとりひとりの顔写真の輪郭を検出し個別のファイルに書き出す。
手順:
1. 卒業アルバムのクラス毎の写真のページをスキャンする。
2. ファイル名を指定する。
3. 実行すると顔写真個別にファイルに書き出される。

Created on Sat Apr 09 10:11:27 2016

@author: Masahiro Uno (25th gradiate)
"""

import cv2
import os


filename = "../IMG_20160424_0006.png"
im = cv2.imread(filename)

dirname = '../split/'

# 元の写真を BGRからグレースケールに変更
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# グレースケール画像を2値化。フィルタ後の方がノイズは少ないが, 文字認識のためにフィルタ無しとした。
#ret, im_th = cv2.threshold(im_gray, 200, 255, cv2.THRESH_TOZERO)
ret, im_th = cv2.threshold(im_gray, 220, 255, cv2.THRESH_BINARY)
# こうしないと, im_thはfindContours後にContour付きネガに変わってしまう。
cv2.imwrite(dirname + 'im_th.jpg', im_th)

# 2値画像から輪郭を検出。
# 
contours = cv2.findContours(im_th,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]
contours.sort(key=cv2.contourArea, reverse=True) 

#輪郭の矩形化
indx = 0

im2=im
im_ocr = cv2.imread(dirname + 'im_th.jpg')

deltah=52
for i in range(len(contours)):
    x,y,w,h=cv2.boundingRect(contours[i])

    if (w > 500) & (w < 600) & (h > 400) & (h < 450): # 幅, 高さが所望のサイズ以上のもののみ選択
        # 輪郭で画像を切り出しファイルに書き出す。
        cv2.imwrite(dirname+'demo'+str(indx)+'.jpg', im[y:y+h+deltah, x:x+w])

        # 名前を OCR で読み込むための画像ファイルを作成
        cv2.imwrite(dirname+'demo_ocr'+str(indx)+'.jpg', im_ocr[y+h:y+h+deltah, x:x+w])

        # OCRで名前を読み込み, ファイルに書き出す
        os.system("tesseract {:s} {:s} -l jpn".format(dirname+'demo_ocr'+str(indx)+'.jpg',dirname+'demo_name'+str(indx)))
#        text = open("out.txt").read().replace('ー', '1').replace('\\', '¥')
 
        # 元ファイル上に輪郭を重ねて表示する。
        cv2.rectangle(im2, (x, y), (x + w, y + h+deltah), (0, 255, 0), 3)
        cv2.imwrite(dirname+'all.jpg', im2)

        indx = indx + 1


# OCR
# 次のサイトを参考に, Windows版バイナリをインストールする。ただしWindows版は3.02であり, 
# その後のアップデートはない。
# https://github.com/tesseract-ocr/tesseract/wiki
# 日本語データとしてjpn.traineddataをTesseractのインストールされたフォルダのTessdataフォルダに置く。
# このファイルは 3.04用なので, そのまま実行するとエラーが出る。
# "read_params_file: parameter not found: allow_blob_division"
# そこで次のサイトを参考に書き換える。ただし管理者権限で cmd を開き作業を行うこと。
# http://a244.hateblo.jp/entry/2015/08/25/051222
#

