1 : 在当前目录下 执行 . env 
2 : bash run_big.sh 跑大数据
3 ：bash run_sample.sh 跑测试数据



或者直接用python 执行 ：
python ../Source/main.py   -m -s -l 
三个选项 ：
m ： sample 那么输出到定向到 SampleResult ；参数 为full  输出会定向到Result
s : subway.txt 的地址 ，这个地址是相对于 env中参数 CODEHOME  的路径，也就是当前路径的父目录
c : subway.log 的地址 , 同上

