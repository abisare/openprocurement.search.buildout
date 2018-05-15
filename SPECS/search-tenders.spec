
%define name search-tenders
%define version 0.8
%define build_timestamp %{lua: print(os.date("%Y%m%d"))}
%global commit aaef7f6bc0804fb189335003149ff04194d7aedd
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global _python_bytecompile_errors_terminate_build 0

Summary: OpenProcurement Tenders Indexer and Search API
Name: %{name}
Version: %{version}
Release: %{build_timestamp}
Source0: https://github.com/abisare/openprocurement.search.buildout/archive/%{commit}/openprocurement.search.buildout-%{shortcommit}.tar.gz
License: Apache 2
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: /opt/search-tenders
BuildArch: x86_64

Provides:      search-tenders = 0.8-el7
Provides:      search-tenders(x86_64) = 0.8-el7
Requires:      /bin/sh
Requires:      /usr/bin/python
Requires:      libc.so.6()(64bit)
Requires:      libpthread.so.0()(64bit)
Requires:      librt.so.1()(64bit)
Requires:      libzmq.so.5()(64bit)
Requires:      rtld(GNU_HASH)
Requires:      elasticsearch >= 1.7
Requires:      bash-completion
Requires:      bind-utils
Requires:      file
Requires:      gcc
Requires:      git
Requires:      logrotate
Requires:      make
Requires:      wget
Requires:      java
Requires:      python-devel
Requires:      python-setuptools
Requires:      zeromq-devel

%description
OpenProcurement Tenders Indexer and Search API

#%%prep
#%%autosetup -n openprocurement.search.buildout-%{shortcommit}.tar.gz   

%build
cd openprocurement.search.buildout-%{commit}
python bootstrap.py
python bin/buildout

%install

install -m 755 -d %{buildroot}/%{prefix}
install -m 755 -d %{buildroot}/%{prefix}/bin
install -m 755 -d %{buildroot}/%{prefix}/eggs
install -m 755 -d %{buildroot}/%{prefix}/share
install -m 755 -d %{buildroot}/%{_sysconfdir}/cron.d
install -m 755 -d %{buildroot}/%{_sysconfdir}/search-tenders

find %{_builddir}/openprocurement.search.buildout-%{commit}/bin -type f -exec install -Dm 755 "{}" "%{buildroot}/%{prefix}/bin" \;
find %{_builddir}/openprocurement.search.buildout-%{commit}/eggs -type f -exec install -Dm 755 "{}" "%{buildroot}/%{prefix}/eggs" \;
find %{_builddir}/openprocurement.search.buildout-%{commit}/share -type f -exec install -Dm 755 "{}" "%{buildroot}/%{prefix}/share" \;

install -m 664 %{_builddir}/openprocurement.search.buildout-%{commit}/debian/search-tenders/etc/cron.d/search-tenders %{buildroot}/%{_sysconfdir}/cron.d/search-tenders
install -m 664  %{_builddir}/openprocurement.search.buildout-%{commit}/debian/search-tenders/etc/search-tenders/ftpsync.ini %{buildroot}/%{_sysconfdir}/search-tenders/ftpsync.ini
find %{_builddir}/openprocurement.search.buildout-%{commit}/etc -type f -exec install -Dm 755 "{}" "%{buildroot}/%{_sysconfdir}/search-tenders" \;


%files
/opt
%config %{_sysconfdir}


%clean
rm -rf %{buildroot}

%post -p /bin/sh
#!/bin/sh

USER=search-tenders
GROUP=search-tenders
NAME=search-tenders
HOME=/opt/$NAME

if ! id $USER ; then
  adduser --system --home $HOME --no-create-home --shell /bin/false --user-group $USER
fi

for DIR in $HOME/var $HOME/var/log $HOME/var/run /var/log/$NAME ; do
  mkdir -p $DIR
  chown -R $USER:$GROUP $DIR
done

if [ -d /etc/elasticsearch ] ; then
  test -e /etc/elasticsearch/stopwords || mkdir /etc/elasticsearch/stopwords
  cp -n $HOME/share/stopwords/*.txt /etc/elasticsearch/stopwords
fi

if [ -x /bin/systemctl ] ; then
  /bin/systemctl daemon-reload
fi


%preun -p /bin/sh
#!/bin/sh

if [ -d /etc/elasticsearch/stopwords ] ; then
    rm /etc/elasticsearch/stopwords/ukrainian.txt
    rmdir /etc/elasticsearch/stopwords
fi

if [ -d %{prefix} ] ; then
  rm -rf %{prefix}
fi
%changelog



