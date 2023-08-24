# gem5-simpoint-benchmark

scripts and notes about slice benchmark with simpoint on gem5

## setup demo

step1:clone dhrystone benchmark
[https://github.com/chsgcxy/dhrystone_linux.git](https://github.com/chsgcxy/dhrystone_linux.git)

step2:clone simpoint3.2
因为官方的Simpoint3.2直接编译是无法通过的，所以这里建议下载修改好之后的版本
[https://github.com/chsgcxy/Simpoint3.2.git](https://github.com/chsgcxy/Simpoint3.2.git)

step3: patch gem5
gem5_23.0.0.1已经准备弃用se.py和fs.py，通过其相关介绍，gem5现在推荐使用gem5_library。
*arm-simpoint-benchmarks.py*是基于gem5_library构建的一个极简单的支持生成simpoint BBV的配置脚本。
将此脚本放在config目录任意文件夹下即可，这里推荐使用目录：**configs/example/gem5_library/**
==后续会考虑构建gem5版本管理==

step4: run gem5 and generate bbv

```bash
./build/ARM/gem5.debug configs/example/gem5_library/arm-simpoint-benchmarks.py -c ../dhrystone/dhrystone.elf --simpoint-profile --simpoint-interval 1000
```

step5: run simpoint

```bash
./simpoint -maxK 30 -numInitSeeds 1 -loadFVFile ../input/simpoint.bb.gz -inputVectorsGzipped -saveSimpoints ../output/dhrystone.simpoints -saveSimpointWeights ../output/dhrystone.weights
```
