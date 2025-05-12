CREATE TABLE address_codes(
   id        INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT
  ,zip_code  VARCHAR(20)  NOT NULL
  ,state     VARCHAR(2) NOT NULL
  ,city      VARCHAR(50) NOT NULL
  ,latitude  NUMERIC(15,4) NOT NULL
  ,longitude NUMERIC(15,4) NOT NULL
  ,street1   VARCHAR(50) NULL
  ,street2   VARCHAR(50) NULL
);

CREATE TABLE customers(
   id              INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT
  ,first_name      VARCHAR(50) NOT NULL
  ,last_name       VARCHAR(50) NOT NULL
  ,email           VARCHAR(50) UNIQUE NOT NULL
  ,phone           VARCHAR(15) NOT NULL
  ,address_code_id INTEGER NOT NULL
  ,FOREIGN KEY (address_code_id) REFERENCES address_codes(id)
);

CREATE TABLE dogs(
   id                         INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT
  ,customer_id                INTEGER  NOT NULL
  ,name                       VARCHAR(50) NOT NULL
  ,breed                      VARCHAR(50) NOT NULL
  ,gender                     VARCHAR(6) NOT NULL
  ,size                       INTEGER  NOT NULL
  ,age                        INTEGER  NOT NULL
  ,special_instructions       VARCHAR(4000)
  ,FOREIGN KEY (customer_id)  REFERENCES customers(id)
);

CREATE TABLE employees(
   id              INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT
  ,first_name      VARCHAR(50) NOT NULL
  ,last_name       VARCHAR(50) NOT NULL
  ,email           VARCHAR(50) UNIQUE NOT NULL
  ,phone           VARCHAR(15) NOT NULL
  ,max_dogs        INTEGER  NOT NULL
  ,address_code_id INTEGER NOT NULL
  ,FOREIGN KEY (address_code_id) REFERENCES address_codes(id)
);

CREATE TABLE walks(
   id          INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT
  ,employee_id INTEGER  NOT NULL
  ,start_time  DATETIME  NOT NULL
  ,end_time    DATETIME  NOT NULL
  ,address_code_id INTEGER NOT NULL
  ,notes       VARCHAR(4000)
  ,FOREIGN KEY (employee_id) REFERENCES employees(id)
  ,FOREIGN KEY (address_code_id) REFERENCES address_codes(id)

);

CREATE TABLE walks_dogs(
   walk_id  INTEGER NOT NULL
  ,dog_id  INTEGER NOT NULL
  ,cost   DECIMAL
  ,notes   VARCHAR(4000)
  ,FOREIGN KEY (walk_id) REFERENCES walks(id)
  ,FOREIGN KEY (dog_id) REFERENCES dogs(id)
  ,PRIMARY KEY(walk_id,dog_id)
);

CREATE TABLE employee_availability(
   id                 INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT
  ,employee_id        INTEGER  NOT NULL
  ,availability_start DATETIME  NOT NULL
  ,availability_end   DATETIME  NOT NULL
  ,FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE dog_walk_times_desired(
   id                 INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT
  ,dog_id             INTEGER  NOT NULL
  ,desired_walk_start DATETIME  NOT NULL
  ,desired_walk_end   DATETIME  NOT NULL
  ,FOREIGN KEY (dog_id) REFERENCES dogs(id)
);

CREATE TABLE pricing (
    id INT PRIMARY KEY AUTO_INCREMENT,
    size INT,
    cost_per_hour DECIMAL
);