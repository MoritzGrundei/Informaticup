FROM python
COPY InformatiCupGame /InformatiCupGame
WORKDIR InformatiCupGame
RUN pip install -r requirements.txt
CMD ["python","main.py"]
