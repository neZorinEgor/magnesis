# Geomagnesis

Запуск API
```shell
uvicorn --factory src.geomagnesis.main:make_asgi
```


```shell
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
```