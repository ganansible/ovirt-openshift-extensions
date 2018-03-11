Name:       ovirt
Version:    %{?_version}
Release:    %{?_release}%{?dist}
License:    ASL 2.0
URL:        http://www.ovirt.org
Source0:    %{name}-flexdriver-%{version}%{?_release:_%_release}.tar.gz
Summary:    flexvolume and provisioner

%description
A Flexvolume driver to provision k8s volumes using oVirt

%package flexvolume-driver 
Summary:    Flexvolume driver k8s using oVirt 

%description flexvolume-driver
A Flexvolume driver to provision k8s volumes using oVirt

%package provisioner
Summary:    Storage provisioner plugin for k8s using oVirt 

%description provisioner 
Storage provisioner plugin for k8s using oVirt

%global vendor ovirt
%global kube_plugin_dir   /usr/libexec/kubernetes/kubelet-plugins/volume/exec/%{vendor}~%{name}
%global repo github.com/rgolangh
%global golang_version 1.9.1
%global debug_package %{nil}

BuildRequires: golang >= %{golang_version} 

%prep
%setup -c

%build
# set up temporary build gopath for the rpmbuild 
set -x
mkdir -p ./_build/src/%{repo}                    
ln -s $(pwd) ./_build/src/%{repo}/%{name}-flexdriver        

export GOPATH=$(pwd)/_build
cd _build/src/%{repo}/%{name}-flexdriver
make build

%install
mkdir -p %{buildroot}%{kube_plugin_dir}
install -p -m 755 %{name}-flexvolume-driver %{buildroot}%{kube_plugin_dir}
install -p -m 644 deployment/%{name}-flexvolume-driver/%{name}.conf.j2 %{buildroot}%{kube_plugin_dir}/%{name}-flexvolume-driver.conf
install -p -m 755 %{name}-provisioner %{buildroot}

%files flexvolume-driver
%dir %{kube_plugin_dir}
%{kube_plugin_dir}/%{name}-flexvolume-driver
%{kube_plugin_dir}/%{name}-flexvolume-driver.conf

%files provisioner
/usr/bin/%{name}-provisioner

%changelog
