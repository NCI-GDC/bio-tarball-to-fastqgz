ARG REGISTRY=docker.osdc.io/ncigdc
ARG BASE_CONTAINER_VERSION=latest

FROM ${REGISTRY}/python3.9-builder:${BASE_CONTAINER_VERSION} as builder

COPY ./ /tarball_to_fastqgz

WORKDIR /tarball_to_fastqgz

RUN pip install tox && tox -e build

FROM ${REGISTRY}/python3.9:${BASE_CONTAINER_VERSION}

LABEL org.opencontainers.image.title="tarball_to_fastqgz" \
      org.opencontainers.image.description="Tool to extract fastq files from complicated tarballs and provide them as standard gzipped fastq files with metadata as json." \
      org.opencontainers.image.source="https://github.com/NCI-GDC/bio-tarball-to-fastqgz" \
      org.opencontainers.image.vendor="NCI GDC"

COPY --from=builder /tarball_to_fastqgz/dist/*.whl /tarball_to_fastqgz/
COPY requirements.txt /tarball_to_fastqgz/

WORKDIR /tarball_to_fastqgz

RUN pip install --no-deps -r requirements.txt \
	&& pip install --no-deps *.whl \
	&& rm -f *.whl requirements.txt

USER app

CMD ["tarball_to_fastqgz --help"]
