

class DbConstant:

    DB_TYPE = 'QSQLITE'
    DB_NAME = 'docker.db'
    
    SELECT_STAR = "select * from %s"
    DROP_TABLE = "drop table %s"
    
    CREATE_TABLE_ENVIRONMENT = "create table %s (" \
                               "env_id integer primary key autoincrement," \
                               "env_name varchar(32))"

    INSERT_ENVIRONMENT = "insert into %s (env_name) values (:name)"

    CREATE_TABLE_ENVIRONMENT_SETTING = "create table %s (" \
                                       "es_name varchar(256)," \
                                       "es_value varchar(1024)," \
                                       "env_id integer, " \
                                       "primary key (env_id, es_name))"

    INSERT_ENVIRONMENT_SETTING = "insert into %s (es_name, es_value, env_id) values (:name,:value,:env_id)"

    SELECT_SETTINGS_BY_ENV = "select * from %s where env_id = :env_id"

    CREATE_TABLE_REGISTRY = "create table %s (" \
                            "reg_id integer primary key," \
                            "reg_name varchar(32)," \
                            "reg_hostname varchar(128))"

    INSERT_REGISTRY = "insert into %s (reg_name, reg_hostname) values (:name, :hostname)"
