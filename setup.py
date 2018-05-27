from distutils.core import setup

setup(
  name='flask-lxc',
  packages=['flask_lxc'],
  version='0.0.1',
  description='Flask LXC API Blueprint',
  author='Angelo Moura',
  author_email='m4n3dw0lf@gmail.com',
  url='https://github.com/m4n3dw0lf/flask-lxc',
  download_url='https://github.com/m4n3dw0lf/flask-lxc/archive/0.0.1.tar.gz',
  install_requires=['Flask>=0.10.1','lxc-python2>=0.1']
)
