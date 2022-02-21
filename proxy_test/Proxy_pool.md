### 免费代理池维护

1. 代理池分为四个基本模块  

   + 储存模块：储存爬取下来的代理  
   + 获取模块：定时在各大代理网站爬取代理
   + 检测模块：定时检测储存模块中的代理是否可用
   + 接口模块：勇API提供对外服务的接口

2. 存储模块  
   使用Redis的有序集合，集合中每个元素即使代理，例如：60.207.237.111:8888  
   有序集合中每个元素都有一个分数字段，根据元素分数大小进行排序，实现有序。
   分数设置方案：
   ```tex
   新获取的代理的设置分数为10；一经验证可用设置为100；如果检测到代理不可用，将分数减1，减到0，删除该代理
   原因：
   	1.免费代理网站获取代理不稳定，存在一定失败率，如果可用设为100，确保代理有机会被调用；
   	2.连续失败100次才将代理删除，是因为可用代理十分宝贵；
   	3.新获取的代理连续失败10次即删除，减小开销。
   ```  
   语法解释：
   ```python
   def random(self) -> Proxy:
       pass
   # -> 主要是标记返回值数据类型,这样只看代码就知道该方法返回什么类型数据。
    ```  
   + \_\_init__方法用于初始化，参数是Redis的链接信息，默认链接信息定义为常量；
   + add方法添加代理并设置分数；
   + random方法用户随机获取代理，首先获取分数为100的代理，然后从中随机返回一个；如果不存在100分，按照排名，获取前100位代理，然后随机返回一个；否则抛出异常；
   + decrease检测到无效代理，减1分；
   + exists判断代理是否存在于合集中；
   + max 将代理的分数设为PROXY_SCORE_MAX（100）
   + count 返回集合中元素个数（未失效代理个数）
   + all 返回集合中所有元素的列表。
   
3. 获取模块  
   在父类中实现通用爬取的fetch方法，然后在每个子类里实现解析方法  
4. 检测模块  
   使用aiohttp库进行异步检测  
5. 接口模块  
   考虑因素：
   + redis信息安全；  
   + 远程redis服务器如果只允许本地连接；
   + 爬虫所在主机没有连接redis模块；或这爬虫不是由python编写；
   + RedisClient或者数据结构更新，爬虫端必须同步  
   综上：将代理池作为独立服务运行，增加接口模块，使用Flask库来实现。  
6. 调度模块  
   对测试模块，获取模块和接口模块都设置开关
   然后使用多线程
   
###付费代理
1.付费代理分类  
  按照使用流程大致分为两类代理：  
  + 代理商提供代理提取接口的付费代理；
  + 代理商搭建了隧道代理的付费代理，可以直接将此类代理设置为固定的IP和端口，无需进一步通过请求接口获取随即代理并设置。（代理商进行了代理池的维护）  
    + 私密代理
    + 隧道代理
    
##ADSL拨号代理的搭建方法
ADSL（Asymmetric Digital Subscriber Line）非对称数字用户环路。  
它的上行带宽和下行带宽不对称，采用频分复用技术把普通电话分成了电话，上行和下行三个相对独立的信道，从而避免相互干扰。  
IP分布在多个A段，量级为千万级，如果将ADSL主机作为代理，隔时拨号更换IP可以防止IP封禁，此外稳定性也会更好。  
购买ADSL云服务器，安装代理软件（流行的有Squid和TinyProxy）。  
动态获取IP cui在Pypi上发布了一个adslproxy的工具。

# 模拟登录  

## 模拟登录原理

1. 模拟登录主要分为两种模式：
   - 基于Session和Cookie；  
   - 基于JWT（JSON Web Token）的模拟登录  
     前后端分离式，请求数据时服务器会校验请求中携带的JWT是否有效   

2. 基于Session和Cookie  
Cookie和Session一定是相互配合工作。
   + Cookie里可能只保存了SessionID相关信息，服务器就能根据这个信息找到对应的Session；  
   + Cookie直接保存了某些凭证信息。  
3. 基于JWT  
   Session和Cookie的校验存在一定问题：  
   + 服务器需维护用户登录的Session信息；
   + 分布式部署不方便，不适合前后端分离的项目。  
   
   JWT是为了在网络环境中传递而执行的一种基于JSON的开放标准，实际上就是在每次登录时都通过一个Token字段校验登录状态，  
   一般用来在身份提供者和服务提供者之间传递要认证的用户身份信息。，以便从资源服务器获取资源，此外可以增加一些业务必要的校验逻辑。
   JWT一般是一个经过Base64加密的字符串，拥有自己的标准，如下：
   ```text
   eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6ImJhb2JhbyIsImV4cCI6MTU5OTkyMjUyOCwidXNlcklkIjoyMX0.YhA3kh9KZOAb7om1C7o3vBhYp0f61mhQWWOoCrrhqvo
    ```       
   中间有两个分隔作用的'.'，三段式加密，分别为Header，Payload和Signature：  
   + Header：声明JWT的签名算法（加密算法），还可能包括JWT编号或者类型；  
   + Payload：通常为业务需要但不敏感信息；  
   + Signature：签名，利用密钥secret对Header和Payload的信息加密后形成的，这个密钥保存在服务器端。如果Header和Payload被修改，可以通过Signature来判断。  
   
4. 模拟登录  
5. 账号池  
   通过账号分流防止被封  

## 账号池
1. 账号池具备的功能：  
    + 能够保存登录目标站点的账号和登陆后的Cookie信息；
    + 定时检测每个Cookie的有效性，如果失效，重新模拟登录生成；
    + 一个数据获取接口，能够获取随机Cookie的接口。  
2. 账号池架构
   + 存储模块：负责储存每个账号的用户名，密码以及账号对应的Cookie信息；  
   + 获取模块：负责生成新的Cookie并储存；  
   + 检测模块：需要定时检测存储模块中Cookie的有效性；  
   + 接口模块：使用API提供对外服务的接口，随机存取。  
3. 存储模块  
   存储的内容为***账号信息***和***Cookie***信息  
   账号：用户名+密码  
   
   
# JavaScript逆向爬虫
## 网站加密和混淆技术  
根据保护对象分为：  
1. URL/API参数加密；  
    通过约定客户端和服务端的接口校验方式，通常会使用到加密技术。  
    例如：双方约定一个sign作为接口校验的签名，客户端将URL路径进行MD5加密，然后拼接上某个参数再进行Base64编码，得到sign，客户端会对内容做同样的出来，判断sign是否一致，从而判断内容是否被篡改。  
2. JavaScript压缩、混淆和加密：  
    不能单纯依靠接口加密技术解决问题，愿意：  
    + JavaScript代码运行与客户端，它必须在用户浏览器端加载并运行；
    + JavaScript代码是公开透明的，也就是说浏览器可以直接获取到正在运行的JavaScript的源码。  
    
    JavaScript代码压缩、混淆和加密技术：
    + 代码压缩：去除代码中不必要的的空格、换行等内容，使源码压缩为几行内容，降低代码的可读性同时提高网站的加载速度；  
        主流前端技术会用webpack和Rollup等工具进行打包，它们会对远大吗进行编译和压缩；  
    + 代码混淆：使用变量替换、字符串阵列化、控制流平坦化、多态变异、僵尸函数、调试保护等手段，将代码变得难以阅读和分析；  
        现在JavaScript混淆的主流实现是***javascript-obfuscator***、***terser***两个库
    + 代码加密：通过某种手段将JavaScript代码进行加密，转成人无法阅读或者解析的代码，例如WebAssembly技术，它可以将JavaScript代码用C/C++实现，JavaScript调用其编译形成后的文件来执行相应功能。  
    + 变量名混淆：可以在javascript-obfuscator中identifierNamesGenerator来实现，如：将其值设为hexadecimal，则会将变量名替换为十六进制。  
    + 字符串混淆：将一个字符串放到一个数组里面，使之无法被直接搜索到。可以通过stringArray参数控制，默认为true；  
    + 代码自我保护：我们可以通过设置selfDefending参数开启代码自我保护功能。开启之后，混淆后的JavaScript会强制以一行形式显示，如果将混淆后的代码进行格式化或者重命名，改代码将无法执行。  
    + 控制流平坦化：其实是将代码的执行逻辑混淆，使其变得复杂、难度。其基本思想是将一些逻辑处理块都统一加上一个前驱逻辑块，每个逻辑块都由前置逻辑块进行条件判断和分发，构成闭环逻辑，导致整个执行逻辑复杂、难读。  
    + 无用代码注入：无用代码即不会被执行的代码或对上下文没有任何影响的代码，诸如后可以对现有的JavaScript代码阅读形成干扰。可以使用deadCodeInjection参数开启这个选项，默认为false。  
    + 对象键名替换：如果是一个对象，可以使用transformObjectKeys来对对象的键值进行替换。  
    + 禁用控制台输出：可以使用disableConsoleOutput来禁用掉console.log输出功能，增大调试难度；  
    + 调试保护：在Javascript代码中加入debugger关键字，执行到该位置时，就会进入断点调试模式。如果在多个位置加入debugger，或者某个逻辑反复执行debugger就会反复进入断点调试模式，原本的代码就无法顺畅执行。  
    + 域名锁定：通过控制domainLock来控制JavaScript代码只能在特定域名下运行，降低被模仿或者盗用的风险；
    + 特殊编码：使用特殊的工具包（aaencode、jjencode、jsfuck等）对代码进行混淆和编码；  
3.WebAssembly  
    基本思路：将核心逻辑代码使用其他语言（C/C++）来编写，并编译成类似字节码的文件并通过JavaScript来调用，从而起到二进制级别的防护。  

## 浏览器常用技巧  
1. Elements：元素面板，用于查看或者修改当前网页HTML节点的属性、CSS属性、监听时间。HTML和CSS头可以即时修改和即时显示。
    + 改写JavaScript文件，将浏览器原始JavaScript保存后修改再使用Chrome原始Overrides替换。  
2. JavaScript Hook的使用
    + Hook技术：又叫钩子技术，指再程序运行的过程中，对其中的某个方法进行重写，在原先的方法前后加入自定义代码。相当于在系统没有调用该函数之前，钩子程序先捕获该消息，得到控制权，此时钩子函数既可以加工处理该函数的执行行为，也可以强制结束消息的传递。  
    + 油猴脚本  
3. 模拟登录：
    + 使用断点寻找token生成的规则；  
    + 使用hook函数，改写目标函数使目标信息展示出来。例如在调用目标函数前展示信息；  
    + 无限debugger，如每秒钟进行一次debugger，类似的还有无限for循环，while循环，无限递归等；  
        + 禁用断点：使用全局禁用，或者局部禁用甚至添加禁用条件来控制断点；  
        + 替换文件：在新文件里将debugger关键字删除。  

## 使用Node.js执行JavaScript  
1. 安装node.js  
2. 拿到JavaScript加密方法的代码；  
3. 使用node.js调用加密方法获取Token；  
4. 可以使用npm安装express框架将node.js作为持续监听服务，post请求获取数据。
## 局部调用游览器  
1. 直接使用浏览器进行局部方法调用； 
2. 将局部方法挂载到全局window对象上；  
3. 利用playwright的Request Interception机制将想要替换的任意文件进行替换，然后修改源码。

## ATS  
ATS全称Abstract Syntax Tree,抽象语法树。  
一段代码执行前通常进行的三个步骤：
1. 词法分析：一段代码先会被分解成一段段有意义的词法单元；  
2. 语法分析:接着编译器会对一个个词法单元进行语法分析，将其转换为能代表程序语法结构的数据结构；  
3. 指令生成：最后将ATS转换为实际真正可执行的指令并执行。


#### 20220208  
##### Charles抓包
1. 安装java及ideal 2021.3；
2. 安装charles并进行手机抓包
    + 电脑端安装证书；
    + 手机端安装证书并信任（手机访问chls.pro/ssl下载证书）；
    + 手机端设置代理。  
3. 功能：  
    + 分析请求；
    + 重发请求：将捕获到的请求内容加以修改并把修改后的内容发送出去；
    + 修改响应内容： 例如可以将响应内容修改为本地或者远程的某个文件，实现数据的修改和伪造；
##### mitmproxy  
1. 手机端设置代理后需要访问mitm.it来下载证书

####  mitmdump
1. 配合py脚本可以抓取App相关请求内容。例如:mitmdump -s script.py  
    ```python
   def response(flow):
       # flow.request.headers['User-Agent'] = 'MitmProxy'
       print(flow.request.url)
       print(flow.response.text)
   ```
  可以打印请求url和响应内容。
####  appium   
1. 安装Android Studio及配置Android SDK；
2. 安装appium-inspector,但是没有搞清楚怎么使用。
####  Airtest
1. 安装Airtest并尝试使用；
2. 运行过程出错cannot import name ‘_registerMatType‘。  
    原因：同时安装了opencv-python和opencv-contrib-python 版本之间不匹配造成的  
    解决方法：卸载一项后再次安装相同版本的包即可。
3. 基于Poco的UI组件自动化
4. 手机群控爬取  
    + 使用py包adbutils  
    + 使用云控手机（例如河马云）
    
### 安卓逆向  
1. jadx  
    + app包进行反编译，然后可以使用Android Studio进行查看关键逻辑实现的具体代码；  
    + 反混淆：App在编译和打包阶段做了混淆操作，jadx可以进行反混淆操作
2. JEB(与jadx类似)
3. xpose：java层hook工具  
4. Frida：基于Python和JavaScript的Hook和调试框架
5. 对比：  
xpose优缺点：  
+ 优点：十分适合Java层的Hook逻辑；适合一些持久化的Hook操作，编写完毕可以独立且永久运行在手机；
+ 缺点：环境配置复杂；调试过程需要编译和重新安装Xpose模块；对于Native层逻辑无能为力；  
Frida优缺点：
+ 优点：Java层和Native层逻辑都可以Hook；电脑上编写和执行脚本，修改后无需重新编译和额外在手机上安装App；环境配置灵活；
+ 缺点：使用JavaScript操作Java逻辑，兼容性较差；更适合在调试阶段使用，不太适合应用与生产实践
#### SSL Pining（证书锁定）  
防止中间人攻击的技术，只针对HTTPS协议。  
校验证书指纹，在开发阶段如果知道服务器返回的证书指纹，可以提前把指纹写死在客户端，客户端获取证书后对比证书指纹与预定的指纹是否一致，一致通过校验；不一致，断开通讯。  
1. 实现方式：
    + 7.0及以上Android版本提供了原生支持。将指纹写在一个xml文件中，后续引用；
    + 写在Android代码里，Android的HTTP请求使用OkHttp库，库中的SDK就提供了SSL Pining的支持。  
2. 绕过  
    + 使用安卓原生支持方式的，可以使用7.0以下版本系统；
    + 直接Hook用于校验的API，无论证书是否可信，直接返回True；
    + 反编译还原App代码，修改校验逻辑，重新打包。
    + Xpose + JustTruestMe方式： JustTrustMe是一个Xpose模块；
    + VirtualXpose + JustTrustMe：  
        VirtualXpose是基于VirtualApp和epic，在非ROOT环境下运行Xpose模块实现（支持Android 5.0 - 10.0）  
    +Frida + DroidSSLUnpining：同样基于Hook证书校验逻辑绕过。
#### Android脱壳  
Android的壳用来保护App源码不被轻易反编译和修改，加壳之后App的源码无法通过直接反编译获得。  
1. 加壳原理：  
    壳本身也是一个dex文件，可以称之为shell.dex文件。原App的dex文件被加密，shell.dex文件可以解密并运行解密后dex文件。
2. 加壳过程  
    1. 对原dex文件加密：从需要加壳的apk文件中，可以提取出一个dex文件（origin.dex），利用加密算法对该文件进行加密，得到encrypt.dex文件；  
    2. 合成新的dex文件：合并加密得到的encrypt.dex文件和shell.dex文件，将encrypt.dex文件追加在shell.dex文件后面，形成新的dex文件，称之为new.dex文件；  
    3. 替换dex文件：把APK文件中的origin.dex文件替换成new.dex文件并重新打包签名。  
3. 壳的分类  
    + 一代壳：整体加壳，整体保护即上述 “2”中整体替换；  
    + 二代壳：提供方法粒度的保护，即方法抽取型壳。将保护力度细化到了方法级别，对于dex中的某些方法置空，只有在被调用的时候才会解密加载；  
    + 三代壳：指令粒度的保护，即指令抽取型壳。主要分为VMP壳和dex2C壳。就是将Java层的方法Native化。
4. 脱壳  
    + 一代壳：市面上免费加壳服务几乎都是一代壳，例如：360加固，腾讯加固，阿里加固等；  
    + 二代壳：一般需要付费（银行App），脱壳基本思路为***主动调用***,主流脱壳工具是FART； 
    + 三代壳：基本靠手工。
5. 实践  
    1. frida_dump：主要原理为通过文件头内容搜索dex文件并dump下来；  
    2. FRIDA-DEXDump：基于Frida对手机App进行暴力内存搜索实现脱壳；  
    3. FART：对于二代壳主流解决方案是FART，在ART环境下基于主动调用的自动化脱壳方案。
#### 利用IDA Pro静态分析  
Java中的JNI，即 Java本地接口（Java Native Interface），这是Java调用Native语言的一种特性（通常指 C/C++）。通过JNI调用C/C++编写的代码。  
Android中使用JNI的好处：提升防护等级。因为使用C/C++编写好代码后会被编译到一个以so为后缀的文件，Java层需要直接加载该so文件并调用so文件暴露的方法，只通过jadx-gui反编译无法把so文件还原为原来的C/C++代码。  
完整还原C/C++代码几乎不可能，但是可以通过反汇编得到底层汇编代码还原C/C++。
1. IDA Pro：交互式反汇编器专业版。  
    可以将二级制文件中的的机器代码转化成汇编代码，甚至根据汇编代码的执行逻辑还原出高级语言（C/C++）  
#### OLLVM混淆后模拟执行so文件  
如果在so文件中加入混淆机制，即使还原出C/C++代码也几乎不可读。Native层实现混淆常用OLLVM，即针对LLVM的代码混淆工具。  
LLVM是一个编译器架构，是模块化、可重用的编译器和工具链技术的集合，功能是把源代码（C/C++）转化成目标机器能执行的代码。  
1. LLVM架构从广义上分为三部分——前端、优化器、后端。  
    + 前端：前端会使用一个Clang的套件，负责完成一些代码的词法分析、语法分析、语义分析和生成中间代码。  
    + 后端：代码优化和生成目标程序可以归类为LLVM后端，将前端生成的代码转化为机器码。  
    + 中间过程会使用LLVM Pass模块。
2. OLLVM的核心为修改Pass模块，对中间代码进行混淆，这样后端根据中间代码生成的目标程序也会混淆。  
3. OLLVM支持LLVM支持的所有前端语言和所有目标平台。  
    具有三大功能：  
    + Instructions Substitution（指令替换）；  
    + Bogus Control Flow（混淆控制流）；  
    + Control Flow Flattening（控制流平展）。
4. 混淆后so文件代码逻辑调用  
    两种方法：  
    + 直接通过工具和调试找出so文件代码逻辑再实现；  
    + 不关心so文件内部逻辑直接调用so文件。
5. 基于Frida-RPC模拟调用so文件  
    + 电脑安装frida-tools;  
    + 手机下载并运行frida-server;  
    + 手机和电脑处于同一局域网下，并且能够使用adb连接手机。
6. 基于AndServer-RPC模拟调用so文件  
    AndServer是可以运行再Android手机上的一个HTTP服务器，Android的一个第三方包。  
    相当于在手机上启动了一个HTTP服务器，服务器内部可以直接调用App中的方法得到结果并返回。
7. 基于unidbg模拟执行so文件。 
    Python的AndroidNativeEmu和Java的unidbg都支持在电脑上直接执行so文件。  
    unidbg是基于unicorn的逆向工具（unicorn是一个CPU模拟框架），在unicorn的基础上，unidbg可以模拟JNI调用Native API，支持模拟调用系统指令，支持JavaVM、JNIEnv和模拟ARM32、ARM64指令。
##  页面智能解析  
#### 简介  
利用页面解析算法抽取页面中标题、正文等内容。  
利用算法直接计算页面中特定元素的位置和提取路径，包括标题，正文，时间和广告。  
业界已经落地的只能解析算法应用，例如Diffbot、Embedly等。  
1. Diffbot  
####  详情页面智能解析算法  
资讯类网站通常包含两种页面：1.导航的列表页；2.具体内容的详情页。
详情页面的内容解析（标题、正文及发布时间）  
1. 标题：一般来说标题包含在title节点，但是title节点可能并不准确，可以找h节点和meta节点进行参考。   
2. 正文  
    + 正文通常被包含在body节点的p节点中并且p节点一般不会独立存在，而是存在于div等节点内；  
    + 正文所在的p节点可能存在噪声（如网站版权信息、发布人等）；  
    + 正文内容所在的p节点会夹杂style、script等节点，并非正文内容；  
    + 正文内容所在的p节点内可能包含code、span等节点大部分属于正文中的特殊样式字符，一般需要归类到正文中。  

文本密度：简单理解为单位标签内包含的文字个数。  
符号密度：中文中一般会带标点符号，而网页链接、广告信息文字较少通常不包含标点符号，因此可以借助符号密度排除部分内容。  
两者结合计算节点分数，分数最高的就是正文内容所在节点。  
3. 发布时间  
    + 根据meta节点提取真实发布时间；  
    + 根据正则表达式提取时间。  

#### 列表页智能解析算法  
1. 选取组节点；  
2. 合并组节点；  
3. 挑选最佳组节点；  
4. 提取标题和链接
5. 整合  
#### 智能分辨列表页和详情页  
1. 目标：算法区分列表页和详情页  
2. 明确为二分类问题。基本类型为传统机器学习和深度学习。  
    使用SVM模型  
    特征提取：  
    + 文本密度；  
    + 超链接节点数量和比例；  
    + 符号密度；  
    + 列表簇的数量；  
    + meta信息；  
    + 正文标题和title内容相似度。
    
## scrapy
+ Engine：引擎，用来处理整个系统的数据流和事件，是整个框架的核心；  
+ Item：抽象数据结构，定义了爬取结果的数据结构，爬取的数据会被赋值成Item对象。  
+ Scheduler：调度器，用来接受Engine发过来的Request并将其加入队列，同时将Request发回给Engine供Downloader执行，主要维护Request的调度逻辑。  
+ Spiders：spider（蜘蛛）的复数统称，每个spider定义了站点的爬取逻辑和页面解析规则，主要负责解析响应并生成Item核心的请求然后发送给Engine处理。  
+ Downloader：下载器，完成“向服务器发送请求，然后拿到响应的过程”。  
+ Item Pipelines：项目管道，可以对应多个Item Pipeline。Item Pipeline主要负责处理由 Spider从页面抽取的Item，做数据清洗、验证和储存等工作。  
+ Downloader Middlewares：下载器中间件，Engine和Downloader之间的Hook框架，负责实现Downloader和Engine之间的请求和响应的处理过程。  
+ Spider Middlewares：蜘蛛中间件，位于Engine和Spiders之间Hook框架，负责实现Spiders和Engine之间Item，请求和响应的处理过程。  
1. 数据流
