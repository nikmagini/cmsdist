### RPM cms confdb 0.0.1
Source: git://github.com/geneguvo/web-confdb?obj=Server/ec4b924bd421f4f5b8870050482908837822d6b1&export=%n&output=/%n.tar.gz
Requires: python cherrypy oracle oracle-env py2-cx-oracle py2-sqlalchemy py2-marshmallow
Requires: rotatelogs pystack

%prep
%setup -n %n

%build

%install
cp -rp Server/Application_py266 %i/
python -m compileall %i/Application_py266 || true

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d/
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
