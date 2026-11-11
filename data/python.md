# Python

## pip 国内镜像安装

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

安装时若遇到SSL问题，可尝试使用如下http源进行安装：

```bash
pip install xxx-package -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip install xxx-package -i http://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com
```

**清华镜像地址：**`https://pypi.tuna.tsinghua.edu.cn/simple`

例如，假设要安装 `numpy` 库，则在原来的语句上添加 `-i` 和镜像地址即可

```bash
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

其他国内源：

```bash
阿里云：http://mirrors.aliyun.com/pypi/simple/

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

华中理工大学：http://pypi.hustunique.com/

山东理工大学：http://pypi.sdutlinux.org/

豆瓣：http://pypi.douban.com/simple/
```

## 生成requirements.txt文件

整个环境下的安装包都保存到requirements.txt中,使用如下命令

```bash
pip freeze > requirements.txt   
```

## CentOS服务器安装Python3.10

在 CentOS 系统上安装 Python 3.10 可能需要一些额外的步骤，因为 CentOS 的软件仓库默认可能不包含 Python 3.10。以下是在 CentOS 上安装 Python 3.10 的步骤：

### 1. 安装依赖

首先，你需要安装一些基本的开发工具和库，这些是编译 Python 所必需的：

```bash
sudo yum groupinstall "Development Tools"
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel
```

### 2. 下载 Python 3.10

接下来，你需要从 Python 官网下载 Python 3.10 的源代码：

```bash
wget https://mirrors.aliyun.com/python-release/source/Python-3.10.8.tgz
```

请检查 Python 官网以获取最新的版本和下载链接。

### 3. 解压源代码

解压下载的文件：

```bash
tar -xf Python-3.10.8.tgz
cd Python-3.10.8
```

### 4. 配置和编译 Python

配置 Python 并准备编译：

```bash
./configure --enable-optimizations --with-ssl
```

这个命令会检查系统环境并配置 Python。`--enable-optimizations` 选项会启用一些优化，这可能会使 Python 运行得更快，但会增加编译时间。

### 5. 编译并安装 Python

编译 Python 并安装到系统中：

```bash
sudo make altinstall  
```

使用 `altinstall` 而不是 `install` 是为了避免覆盖系统默认的 Python 版本。

### 6. 验证安装

安装完成后，你可以通过以下命令验证 Python 版本：

```bash
python3.10 --version
```

这应该会显示 `Python 3.10.8`，表明 Python 3.10 已成功安装。

### 7. 设置默认 Python 版本（可选）

如果你想将 `python3` 命令指向新安装的 Python 3.10，你可以修改 `/etc/alternatives`：

```bash
sudo alternatives --config python3
```

然后选择 Python 3.10 作为默认版本。

### 注意事项

- 确保你的 CentOS 系统是最新的，或者至少是 Python 3.10 支持的版本。
- 编译 Python 可能需要一些时间，具体取决于你的系统性能。
- 如果你使用的是 CentOS 8 或更高版本，可能需要启用 PowerTools 仓库来获取一些依赖。
- 其他问题，例如SSL请参考博客：[centos7安装python3.10及以上版本最佳步骤（不踩openssl的坑）_centos 安装python3.10-CSDN博客](https://blog.csdn.net/Bsummer/article/details/140001234)

## python虚拟环境

### 1. 创建虚拟环境

虚拟环境是一个独立的目录树，包含特定版本的 Python 解释器和额外的包。使用虚拟环境可以避免全局 Python 环境的污染，并且可以为每个项目单独管理依赖。

**创建虚拟环境的步骤：**

1. 选择一个目录来存放虚拟环境。例如，创建一个名为 `myenv` 的虚拟环境：

   ```bash
   python3.10 -m venv myenv
   ```

   这将创建一个名为 `myenv` 的目录，其中包含一个独立的 Python 环境。

2. 激活虚拟环境：

   - **在 Unix 或 macOS 上**：

     ```bash
     source myenv/bin/activate
     ```

   - **在 Windows 上**：

     ```bash
     myenv\Scripts\activate
     ```

   激活虚拟环境后，你的 shell 提示符会显示虚拟环境的名称，例如：

   ```
   (myenv) $
   ```

### 2. 在虚拟环境中使用 pip

在虚拟环境中，`pip` 会自动安装包到虚拟环境的目录中，而不会影响全局 Python 环境。

**安装包：**

```bash
(myenv) $ pip install fastapi
```

**升级包：**

```bash
(myenv) $ pip install --upgrade fastapi
```

**卸载包：**

```bash
(myenv) $ pip uninstall fastapi
```

**查看已安装的包：**

```bash
(myenv) $ pip list
```

**生成 `requirements.txt` 文件：**

```bash
(myenv) $ pip freeze > requirements.txt
```

**从 `requirements.txt` 安装包：**

```bash
(myenv) $ pip install -r requirements.txt
```

### 3. 退出虚拟环境

当你完成工作后，可以通过以下命令退出虚拟环境：

```bash
(myenv) $ deactivate
```

这将恢复到全局 Python 环境。

## * centos7安装python3.10及以上版本最佳步骤

### 1.安装预备环境

```bash
#安装源码编译需要的编译环境
yum install gcc zlib zlib-devel libffi libffi-devel make
yum install bzip2-devel xz-devel sqlite-devel tk-devel uuid-devel ncurses-devel
#解决后期出现的方向键、删除键乱码问题
yum install -y readline-devel
#
yum install -y wget
```

### 2.安装openssl

```bash
# openssl所需要的依赖
yum -y install perl perl-CPAN
#安装 IPC::Cmd模块,此过程会有几次交互，直接按y即可
cpan IPC::Cmd
#下载openssl
wget https://www.openssl.org/source/openssl-3.0.14.tar.gz  #此处若无法下载，可尝试手动打开链接，科学上网下载，然后传入服务器中解压
#解压
tar -xzvf openssl-3.0.14.tar.gz
#配置
cd openssl-3.0.14
./config --prefix=/usr/local/openssl3.0.14 --libdir=lib --openssldir=/etc/ssl
#编译
make -j1 depend
make -j8
#安装
make install_sw
```

### 3.安装python

```bash
#解压
tar -zxvf Python-3.10.8.tgz
#配置
cd Python-3.10.8
./configure --with-openssl=/usr/local/openssl3.0.14 --with-openssl-rpath=auto --prefix=/usr/local/python3.10
#编译
make -j8
#安装
make altinstall
#建软链
ln -s /usr/local/python3.10/bin/python3.10 /usr/bin/python3
ln -s /usr/local/python3.10/bin/pip3.10 /usr/bin/pip3

#验证
python3 --version
pip3 --version
```


