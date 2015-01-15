HOME=$(shell pwd)
VERSION="3.99.5"
RELEASE=$(shell ./make_helper/get-git-rev .)
NAME=lame
SPEC=$(shell ./make_helper/get-spec ${NAME})
ARCH=$(shell ./make_helper/get-arch)
OS_RELEASE=$(shell lsb_release -rs | cut -f1 -d.)

all: build

clean:
	rm -rf ./rpmbuild
	rm -rf ./SOURCES
	mkdir -p ./rpmbuild/SPECS/ ./rpmbuild/SOURCES/
	mkdir -p ./SPECS ./SOURCES

getsources:
	wget  -P ./SOURCES/ -q http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz

build: clean getsources
	cp -r ./SPECS/* ./rpmbuild/SPECS/ || true
	cp -r ./SOURCES/* ./rpmbuild/SOURCES/ || true
	rpmbuild -ba ${SPEC} \
	--define "ver ${VERSION}" \
	--define "rel ${RELEASE}" \
	--define "name ${NAME}" \
	--define "os_rel ${OS_RELEASE}" \
	--define "arch ${ARCH}" \
	--define "_topdir %(pwd)/rpmbuild" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \

publish:
	echo "publish"
