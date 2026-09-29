# 鏁版嵁鏍煎紡杞崲宸ュ叿

[English](README.md)

鍦?CSV銆丣SON 鏁扮粍鍜?JSON Lines锛圝SONL/NDJSON锛変箣闂磋浆鎹㈣褰曞瀷鏁版嵁銆?
## 涓昏鍔熻兘

- CSV 杞?JSON 鎴?JSONL銆?- JSON 鏁扮粍鎴栧崟涓璞¤浆 CSV/JSONL銆?- JSONL 杞?CSV 鎴?JSON銆?- 鍙缃緭鍏ュ拰杈撳嚭缂栫爜銆?- 鑷姩璇嗗埆鎴栨墜鍔ㄦ寚瀹?CSV 鍒嗛殧绗︺€?- 宓屽 JSON 鍐欏叆 CSV 鏃朵細淇濆瓨鎴愮揣鍑?JSON 鏂囨湰銆?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/data-format-converter.git
cd data-format-converter
python -m pip install -e .
```

## 浣跨敤

```bash
data-convert examples/products.csv products.json
data-convert products.json products.jsonl
data-convert products.jsonl products.csv
data-convert legacy.csv output.json --input-encoding gb18030
data-convert data.txt result.csv --from jsonl --to csv
```

濡傛灉杈撳嚭鏂囦欢宸茬粡瀛樺湪锛岀▼搴忎細瑕嗙洊瀹冦€傝浆鎹㈤噸瑕佹暟鎹墠璇蜂繚鐣欏浠姐€?
## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT

