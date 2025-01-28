ARG REGISTRY=docker.osdc.io/ncigdc
ARG BASE_CONTAINER_VERSION=latest

FROM ${REGISTRY}/python3.9-builder:${BASE_CONTAINER_VERSION} as builder

COPY ./ /bio-tarball-to-fastqgz

WORKDIR /bio-tarball-to-fastqgz

RUN pip install tox && tox -e build

FROM ${REGISTRY}/python3.9:${BASE_CONTAINER_VERSION}

LABEL org.opencontainers.image.title="bio-tarball-to-fastqgz" \
      org.opencontainers.image.description="Tool to extract fastq files from complicated tarballs and provide them as standard gzipped fastq files with metadata as json." \
      org.opencontainers.image.source="https://github.com/NCI-GDC/bio-tarball-to-fastqgz" \
      org.opencontainers.image.vendor="NCI GDC"

COPY --from=builder /bio-tarball-to-fastqgz/dist/*.whl /bio-tarball-to-fastqgz/
COPY requirements.txt /bio-tarball-to-fastqgz/

WORKDIR /bio-tarball-to-fastqgz

RUN pip install --no-deps -r requirements.txt \
	&& pip install --no-deps *.whl \
	&& rm -f *.whl requirements.txt

USER app

ENTRYPOINT ["bio-tarball-to-fastqgz"]

CMD ["--help"]
