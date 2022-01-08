***20220106***  
1.CSS位置偏移反爬案例  
节点额外有偏移设置  
left:0px代表不偏移；left:16px代表从左算起向右偏移16个像素。  
解决方法：  
>首先判断h3节点的name，如果为’name whole‘则直接返回h3节点text内容；如果不是则提取span节点内容包括text内容与偏移量，然后再进行排序返回。  

2.字体反爬案例分析  
![::before](E:\Mydata\picture\before.png)  
在CSS中::before字段可以创建一个伪节点，可以往特定的节点中插入内容。  
读取CSS文件并提取映射结果，即可获得分数  


***20220108***  
****爬虫验证码识别****  
1.OCR（Optical Character Recognition），光学字符识别。  
pytesseract与tesserocr都是python下的OCR识别库，都是对tesseract做的一层python封装，pytesseract是是Google的Tesseract-OCR引擎包装器。