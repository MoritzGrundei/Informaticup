FROM python
COPY InformatiCupGame /InformatiCupGame
ENV PYTHONPATH "${PYTHONPATH}:/InformatiCupGame"
WORKDIR InformatiCupGame
CMD ["python","main.py"]
