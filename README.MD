# litestar MVC 项目

## 环境
python 3.11+

## 安装依赖
清华源
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 运行
litestar
```bash
python app.py
```
uvicorn
```bash
uvicorn app:app --reload
```

### 数据库表迁移

数据库表迁移

```sh
alembic revision --autogenerate -m "comment"
alembic upgrade head
```
