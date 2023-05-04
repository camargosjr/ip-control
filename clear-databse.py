#!/usr/bin/python3
from logging import DEBUG, CRITICAL, ERROR, WARNING, INFO, DEBUG
from logging import basicConfig
from logging import critical, error, warning, info, debug
from logging import FileHandler, StreamHandler
import sqlite3
from sqlite3 import Error
from datetime import datetime
import sys, os


date = datetime.strftime(datetime.now(),'%Y-%m-%d-%H:%M:%S')


log_path =f"/home/guile/superso/ip-control/clear-bd/{date}.log"

# Configurar LOG
file_handler = FileHandler(log_path, 'w')
file_handler.setLevel(INFO)

stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setLevel(level=ERROR)

basicConfig(
    level=INFO,
    datefmt="%d-%m-%Y %H:%M:%S",
    format= '%(levelname)-5s:%(asctime)s: %(message)s',
    handlers=[file_handler]
)

# Cria conexão com banco SQLite
def create_connection(db_file):
    conn = None
    try:
        conn = conn = sqlite3.connect(db_file)
    except Error as e:
        error(f"ERRO AO CRIAR CONEXÃO -> {e}")
        sys.exit(e)

    return conn

# Deleta endereço MAC do banco
def delete_mac(conn, id):
    sql = "delete from maccontrol_macaddress where id=?"
    cur = conn.cursor()
    try:
        cur.execute(sql,(id,))
        conn.commit()

    except Error as e:
       error(f"ERRO AO DELETAR MAC -> {e}")
       sys.exit(e)

# Busca todos MACs com cadastro expirados
def select_macs(conn):
    utc_now = datetime.utcnow()
    cur = conn.cursor()
    cur.execute(f"select * from maccontrol_macaddress where allowed_days<?", (utc_now,))
    return cur.fetchall()

# MAIN
def main():
    db_path = "/home/guile/superso/ip-control/ipcontrol/db.sqlite3"

    conn = create_connection(db_path)
   
    with conn:
        mac_address_list = select_macs(conn)

        for mac in mac_address_list:
            expiration_date = mac[4]
            
            delete_mac(conn, mac[0])
            info(f"EXCLUIDO {mac[1]:<20} {mac[2]} {expiration_date[:19]}")
            

      
if __name__ == '__main__':
    main()