FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-runtime
LABEL authors="zackfair"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置国内 PyPI 源，加速依赖安装
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

# 确保复制代码到容器中
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动应用程序
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
