![灵仙儿和二狗子](explain/LOGO2.png "LOGO2")    
哈喽！我是二狗子（2🐕）！仅局部重绘采样器与变异种子采样器来啦！     
Hello! I am Er Gouzi (2) 🐕）！ Only partial redrawing sampler and variant seed sampler are here!    

如果你没有代码基础，或者安装节点时不想敲pip可以使用我制作的环境安装器    
[二狗子环境编辑安装器]([https://space.bilibili.com/19723588?spm_id_from=333.1007.0.0](https://github.com/11dogzi/Comfyuinodes-HJGL)   

## 局部重绘采样器    
Local redraw sampler    
实现仅对蒙版区域进行需求分辨率的重绘（类似WebUi的仅局部重绘模式）    
Implement only the required resolution redrawing for masked areas (similar to WebUi's local redrawing mode)    
![局部重绘采样器](explain/局部重绘采样器.png "局部重绘采样器")  
![局部重绘](explain/局部重绘.png "局部重绘")    

并且保留还原非重绘区域像素空间的原像素,常规重绘模式中非重绘区域由于压缩导致像素信息丢失        
And retain the original pixels that restore the pixel space of non redrawn areas. In conventional redrawn modes, non redrawn areas lose pixel information due to compression    
![丢失细节](explain/丢失细节.png "丢失细节")   

局部重绘采样器还原非重绘区域细节（安照原图像素）    
Partial redrawn sampler restores details of non redrawn areas (as shown in the original image pixels)    
![保存细节](explain/保存细节.png "保存细节")     

## 变异种子采样器  
Mutant seed sampler    
通过对原噪声图seed进行组合微调实现在不改变图像构图的情况下实现微调生成    
By combining and fine-tuning the original noise image seed, achieving fine-tuning generation without changing the image composition    
![通过变异种子对图像进行微调](explain/通过变异种子对图像进行微调.png "通过变异种子对图像进行微调")      
![微调1](explain/微调1.png "微调1")     
![变异种子微调](explain/变异种子微调.png "变异种子微调")     
![变异种子微调实例](explain/变异种子微调实例.png "变异种子微调实例")        

## 局部重绘采样器的CN实现   
CN Implementation of Local Redraw Sampler    
通过2🐕Local Image节点对CN控制网进行裁剪处理以匹配局部重绘采样器    
具体连接方式可使用实例工作流    
Through 2 🐕 The Local Image node prunes the CN control network to match the local redraw sampler
The specific connection method can be achieved using instance workflow    
![局部CN应用](explain/局部CN应用.png "局部CN应用")
通过线稿进行局部重绘    
Partial redrawing through line drafts    
![局部CN应用结果](explain/局部CN应用结果.png "局部CN应用结果")    

## 局部重绘采样器参数    
Partial redraw sampler parameters    
![局部重绘参数](explain/局部重绘参数.png "局部重绘参数")    

## 局部重绘采样器CN控制网参数  
Partial redrawn sampler CN control network parameters
![局部裁剪参数](explain/局部裁剪参数.png "局部裁剪参数")    

## 变异种子采样器参数    
Mutation seed sampler parameters    
![变异参数](explain/变异参数.png "变异参数") 


## 更多SD免费教程
More SD free tutorials   
灵仙儿和二狗子的Bilibili空间，欢迎访问：   
Bilibili space for Lingxian'er and Ergouzi, welcome to visit:   
[灵仙儿二狗子的Bilibili空间](https://space.bilibili.com/19723588?spm_id_from=333.1007.0.0)   
欢迎加入我们的QQ频道，点击这里进入：   
Welcome to our QQ channel, click here to enter:   
[二狗子的QQ频道](https://pd.qq.com/s/3d9ys5wpr)   
![LOGO1](explain/LOGO1.png "LOGO1")![LOGO](explain/LOGO1.png "LOGO1")![LOGO](explain/LOGO1.png "LOGO1")    
