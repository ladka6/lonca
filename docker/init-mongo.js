db = db.getSiblingDB('admin');
db.auth('root', '12345678');

db = db.getSiblingDB('products');
db.createUser({
  user: 'app_user',
  pwd: 'password',
  roles: [
    {
      role: 'readWrite',
      db: 'products',
    },
  ],
});

db.createCollection('product');