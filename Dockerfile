FROM python:3.9
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip3 install --no-cache-dir /usr/src/app
RUN pip3 install uvicorn
EXPOSE 8000
ENTRYPOINT ["python3", "-m", "uvicorn", "--host", "0.0.0.0", "netlifycms_oauth_github_provider:app"]
