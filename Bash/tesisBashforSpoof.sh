#!/bin/bash

contador=2
for i in $(seq 1 $contador)
do
	sudo mn -c
	sleep 1s
	mkdir /data/Descargas/media_org/temp
	chmod 777  /data/Descargas/media_org/temp
	echo "START NETWORK MININET"
	sudo python auto_vlc_StreambandwidthSpoof.py
	sudo cp /data/Descargas/media_org/temp/mininet_video_h7_1234.mp4 /data/Descargas/media_org/media/streamSpoof/mininet_video_h7_1234_$i.mp4
	sleep 2s
	sudo ffmpeg -r 24 -i /data/Descargas/media_org/media/bunny.mp4 -r 24 -i /data/Descargas/media_org/media/streamSpoof/mininet_video_h7_1234_$i.mp4 -lavfi "[0:v]setpts=PTS-STARTPTS[reference]; [1:v]scale=320:240:flags=bicubic,setpts=PTS-STARTPTS[distorted]; [distorted][reference]libvmaf=psnr=1:ssim=1:log_fmt=csv:model_path=/usr/local/share/model/vmaf_v0.6.1.pkl:log_path=/data/Descargas/media_org/dataset/datosSpoof/logprDoS$i.csv" -f null -
	sleep 15s
	sudo rm -rf /data/Descargas/media_org/temp/
	
done

