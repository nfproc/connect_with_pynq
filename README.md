Sources for "various methods to connect self-built circuits with PYNQ" for ACRi Blog
====================================================================================

このリポジトリには、ACRi ブログでのコース (連載) の1つである<a href="https://www.acri.c.titech.ac.jp/wordpress/archives/category/21q1-01b">「自作回路を PYNQ につなぐ様々な方法」</a>で使用したソースコードの一式が含まれています。一部、<a href="https://swest.toppers.jp/SWEST23/">SWEST23</a> の SWEST/ACRi 共同企画セッション向けに使用したソースコードも含みます。

ディレクトリ構造は以下のとおりです。

- knight: 第1回で使用したナイトライダー回路の記述一式
- blink: ナイトライダー回路を簡略化した LED 点滅回路の記述一式
- knight2: 第2回で使用した改良版ナイトライダー IP コアのソースコード一式
- TRNG_IP: 第3回で使用した真性乱数生成 IP コアのソースコード一式（別リポジトリ）
- stencil_hdl: 第4回で使用したステンシル計算コプロセッサの記述一式（IP コアは別リポジトリ）
- stencil_hls: 第5回で使用したステンシル計算コプロセッサ（HLS 版）の記述一式
- sender_hls: <a href="https://www.acri.c.titech.ac.jp/wordpress/archives/8512">AXI でプロセッサとつながる IP コアを作る (3)</a>で取り上げたパターン送信回路の PYNQ, Vitis HLS 対応版
- LICENSE.txt: ライセンス文
- README.md: このファイル

詳しくは、上記リンクからブログコースの各記事をご参照ください。