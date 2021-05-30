FROM ${BASE_IMAGE:-ubuntu:18.04}

ENV DEBIAN_FRONTEND noninteractive

ARG JAVA_VERSION=8
ENV JAVA_VERSION=${JAVA_VERSION:-8}

##############################################
#### ---- Installation Directories   ---- ####
##############################################
ENV INSTALL_DIR=${INSTALL_DIR:-/usr}
ENV SCRIPT_DIR=${SCRIPT_DIR:-$INSTALL_DIR/scripts}

########################################
#### update ubuntu and Install Python 3
########################################
ARG LIB_BASIC_LIST="curl iputils-ping nmap net-tools build-essential software-properties-common "
ARG LIB_COMMON_LIST="bzip2 libbz2-dev git wget unzip vim python3-pip python3-setuptools python3-dev python3-venv python3-numpy python3-scipy python3-pandas python3-matplotlib"
ARG LIB_TOOL_LIST="libsqlite3-dev sqlite3"

#apt-get install -y curl iputils-ping nmap net-tools build-essential software-properties-common libsqlite3-dev sqlite3 bzip2 libbz2-dev git wget unzip vim python3-pip python3-setuptools python3-dev python3-venv python3-numpy python3-scipy python3-pandas python3-matplotlib && \
RUN apt-get update -y && \
    apt-get install -y apt-utils automake pkg-config libpcre3-dev zlib1g-dev liblzma-dev && \
    apt-get install -y ${LIB_BASIC_LIST} && \
    apt-get install -y ${LIB_COMMON_LIST} && \
    apt-get install -y ${LIB_TOOL_LIST} && \
    apt-get install -y git xz-utils && \
    apt-get install -y sudo && \
    apt-get clean -y

########################################
#### ------- OpenJDK Installation ------
########################################
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get update && apt-get install -y --no-install-recommends \
		bzip2 \
		unzip \
		xz-utils \
	&& rm -rf /var/lib/apt/lists/*

# Default to UTF-8 file.encoding
ENV LANG C.UTF-8

ENV JAVA_HOME=/usr/lib/jvm/java-${JAVA_VERSION}-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# ------------------
# OpenJDK Java:
# ------------------

#ARG OPENJDK_PACKAGE=default-jdk
ARG OPENJDK_PACKAGE=${OPENJDK_PACKAGE:-openjdk-${JAVA_VERSION}-jdk}

ARG OPENJDK_INSTALL_LIST="${OPENJDK_PACKAGE} ${OPENJDK_SRC}"

RUN apt-get update -y && \
    apt-get install -y ${OPENJDK_INSTALL_LIST} && \
    ls -al ${INSTALL_DIR} ${JAVA_HOME} && \
    export PATH=$PATH ; echo "PATH=${PATH}" ; export JAVA_HOME=${JAVA_HOME} ; echo "java=`which java`" && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------------------------
# update-alternatives so that future installs of other OpenJDK versions don't change /usr/bin/java
# ... and verify that it actually worked for one of the alternatives we care about
# ------------------------------------------------------------------------------------------------
RUN update-alternatives --get-selections | awk -v home="$(readlink -f "$JAVA_HOME")" 'index($3, home) == 1 { $2 = "manual"; print | "update-alternatives --set-selections" }'; \
	update-alternatives --query java | grep -q 'Status: manual'

###################################
#### ---- Install Maven 3 ---- ####
###################################
ARG MAVEN_VERSION=${MAVEN_VERSION:-3.6.3}
ENV MAVEN_VERSION=${MAVEN_VERSION}
ENV MAVEN_HOME=/usr/apache-maven-${MAVEN_VERSION}
ENV PATH=${PATH}:${MAVEN_HOME}/bin
RUN curl -sL http://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz \
  | gunzip \
  | tar x -C /usr/ \
  && ln -s ${MAVEN_HOME} /usr/maven

########################################
#### ---- PIP install packages ---- ####
########################################
COPY requirements.txt ./

## -- if pkg-resources error occurs, then do this! -- ##
## -- Warning:
## WARNING: pip is being invoked by an old script wrapper. This will fail in a future version of pip.
## Please see https://github.com/pypa/pip/issues/5599 for advice on fixing the underlying issue.
## To avoid this problem you can invoke Python with '-m pip' instead of running pip directly.

# pip3 uninstall pkg-resources==0.0.0
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip  --no-cache-dir install --upgrade pip && \
    python3 -m pip --no-cache-dir install --ignore-installed -U -r requirements.txt && \
    python3 -m pip install 'pandas==1.1.5'

## -- added Local PIP installation bin to PATH
ENV PATH=${PATH}:${HOME}/.local/bin

## VERSIONS ##
ENV PATH=${PATH}:${JAVA_HOME}/bin

RUN mvn --version && \
    python3 -V && \
    pip3 --version
    #Apache Maven 3.6.3; Java version: 1.8.0_275
    #python3 version 3.6.9
    #pip3 version 21.0.1

# Add python modules to python path
ENV PYTHONPATH "/mnt/Git/scripts/modules:/mnt/Git/scripts/disagree"

#########################
#### ---- Entry ---- ####
#########################
CMD ["/bin/bash"]

