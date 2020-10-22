FROM python:3.6-stretch

ENV BINARY=python_project

RUN apt-get update \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

COPY ./dist/ /opt

WORKDIR /opt

RUN make init-pip \
  && ln -s /opt/bin/${BINARY} /bin/${BINARY} \
  && chmod +x /bin/${BINARY}

ENTRYPOINT ["/bin/python_project"]

CMD ["--help"]
