FROM python
COPY Source /Source
RUN pip install -r Source/requirements.txt
CMD ["python", "-m", "Source.Main.Utility.WebSocketTest.py"]
