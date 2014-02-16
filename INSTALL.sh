# You should have virtualenv and pip already.
set -e
cp ./dependencies/setuptools-0.6c11-py2.7.egg.noticemegit ./setuptools-0.6c11-py2.7.egg
cp ./dependencies/pip-1.1.tar.gz .
virtualenv --never-download venv
rm -rf setuptools-0.6c11-py2.7.egg pip-1.1.tar.gz
source ./venv/bin/activate

export INSTALL_DIR=`pwd`
export BASKET_ROOT=$INSTALL_DIR/dependencies
pip install --no-index -f file://$BASKET_ROOT \
    Basket \
    Flask \
    SQLAlchemy \
    Flask-SQLAlchemy \
    Flask-OpenID \
    Flask-RESTful

python ./server/init_db.py foo
echo "Should be good to go.sh!"

