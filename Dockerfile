FROM python:3.7

RUN python -m venv /venv
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH
ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt
ADD . /app

ENV PYTHONPATH=multitude
CMD ["uvicorn", "api:app"]
