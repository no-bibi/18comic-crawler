#coding=utf-8
import requests
import re
import os
import time
from bs4 import BeautifulSoup
import sys

print('输入18comic的漫画页url,然后提取该漫画的所有图片保存到文件夹下')
print('url(例如: https://18comic.pro/photo/121906/) = ')

url = input()

with open('log','a+') as f:
	f.write('Start downloading:'+url+'\n-----------------------')

os.system('start python 18comic.py')
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
r_url=requests.get(url,headers=headers)

soup = BeautifulSoup(r_url.text,'lxml')

p_image_link = re.compile(r'/media/photos/\S+/\S+jpg')
res_images_link = []
res_images_link = p_image_link.findall(r_url.text)

p_split_name = re.compile(r'/')
p_split_18comic = re.compile(r'/photo/')

foldername = soup.title.string
foldername = foldername.strip('\n')
foldername = foldername.replace('|','')
current_dir = os.path.dirname(os.path.abspath(__file__))
FilePath = current_dir + '\\comic\\'+foldername+'\\'

if os.path.exists(FilePath) == False:
	os.mkdir(FilePath)
	
imageNumMax = len(res_images_link)
imageNumMin = 0

for imageLink in res_images_link:
	r_imageLink=requests.get(p_split_18comic.split(url)[0]+imageLink,headers=headers)
	filename = p_split_name.split(imageLink)[4]
	with open(FilePath+filename,'wb+') as f:
		f.write(r_imageLink.content)
	imageNumMin=imageNumMin+1
	sys.stdout.write('\r'+str(imageNumMin)+'/'+str(imageNumMax)+' '+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	sys.stdout.flush()
	
with open('log','a+') as f:
	f.write('Finished downloading:'+url+'\n-----------------------')
input('\n下载完成!! 已保存到: '+FilePath)

