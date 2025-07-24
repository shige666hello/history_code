FROM paketobuildpacks/run-jammy-base:0.1.77
COPY . /workspace
WORKDIR /workspace

USER root

RUN mkdir -p /workspace/cpython/ && \
  tar -zxf python_3.10.10_linux_x64_jammy_72b4995d.tgz -C /workspace/cpython && \
  rm -rf python_3.10.10_linux_x64_jammy_72b4995d.tgz

ENV PATH="/workspace/cpython/bin:$PATH"
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+${LD_LIBRARY_PATH}:}"/workspace/cpython/lib"

CMD ["python3", "server.py"]
