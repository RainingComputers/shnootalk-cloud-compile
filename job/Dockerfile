FROM archlinux:latest

RUN pacman -Sy
RUN pacman --noconfirm -S llvm clang make git python3 python-pip

RUN git clone https://github.com/RainingComputers/ShnooTalk
RUN ln -s /bin/llvm-config /bin/llvm-config-12
RUN cd ShnooTalk; make build; make install

COPY ./shnootalk_cc_job ./shnootalk_cc_job
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system

RUN pacman --noconfirm -Rs git
