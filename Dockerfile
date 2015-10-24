FROM python:3-onbuild

ENTRYPOINT ["python", "foodProcessor.py", "/in", "/out"]
