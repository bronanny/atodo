# You should have virtualenv and pip already.

virtualenv venv
source ./venv/bin/activate

export INSTALL_DIR=`pwd`
export BASKET_ROOT=$INSTALL_DIR/dependencies
pip install --no-index -f file://$BASKET_ROOT Basket Flask SQLAlchemy Flask-SQLAlchemy

echo "Should be good to go.sh!"

