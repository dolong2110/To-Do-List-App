FROM python:3.9

WORKDIR /usr/app/

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

RUN useradd admin
RUN chown -R admin:admin /usr/app/
USER admin

EXPOSE 8080

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]