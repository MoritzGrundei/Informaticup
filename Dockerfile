FROM python
COPY InformatiCupGame /InformatiCupGame
WORKDIR InformatiCupGame
CMD ["python","main.py"]
