FROM python:3.6-stretch

ENV BINARY=tarball_to_fastqgz

RUN apt-get update \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

COPY ./dist/ /opt
COPY metadata/tcga.rna.11128.tarball.meta.tsv /opt/

WORKDIR /opt

RUN make init-pip \
  && ln -s /opt/bin/${BINARY} /bin/${BINARY} \
  && chmod +x /bin/${BINARY}

ENTRYPOINT ["/bin/tarball_to_fastqgz"]

CMD ["--meta", "tcga.rna.11128.tarball.meta.tsv"]
