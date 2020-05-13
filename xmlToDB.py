
from xml.dom import minidom
from os import listdir
from os.path import isfile, isdir
import mysql.connector

#lista de archivos en una carprta, función directo de internet
#creación lista con archivos dentro de una carpeta
#entrada: path carpeta contenedora de archivos 
def lista_archivos(path):    
    return [obj for obj in listdir(path) if isfile(path + obj)]


        
#creación de tabla factura
#entrada: con conexión        
def sql_tabla_factura(con):
    cnx = mysql.connector.connect(**con)
    cursorObj = cnx.cursor()
    cursorObj.execute("CREATE TABLE facturas(datetime int, tipo text, folio text, emisor text,receptor text, total int)")
    cnx.commit()
    cnx.close()
    
#creación de tabla detalle factura
#entrada: con conexión  
def sql_tabla_detalle_factura(con):
    cnx = mysql.connector.connect(**con)
    cursorObj = cnx.cursor()
    cursorObj.execute("CREATE TABLE detalle_factura(rut text, folio text, nombre text, monto int, iva float8)")
    cnx.commit()
    cnx.close()
    
#creación de tabla emisor_receptor
#entrada: con conexión  
def sql_tabla_emisor_receptor(con):
    cnx = mysql.connector.connect(**con)
    cursorObj = cnx.cursor()
    cursorObj.execute("CREATE TABLE empresas(rut text, razon_social text,PRIMARY KEY (rut(10)))")
    cnx.commit()
    cnx.close()

#se inserta el emisor o receptor como rut de empresa y su razón social
#entrada: con conexión
#         rut         =rut del emisor-receptor
#         razon_social=razón social de la empresa 
def insert_emisor_receptor(con,rut,razon_social):
    try:
        cnx = mysql.connector.connect(**con)
        cursorObj = cnx.cursor()
        stmt_select = "SELECT rut FROM empresas where rut='"+rut+"'"
        cursorObj.execute(stmt_select)
        
        rows = None
        try:
            rows = cursorObj.fetchall()
            cnx.close()
        except mysql.connector.InterfaceError as e:
            raise
        print (rows)
        if rows == []:
            try:
                cnx = mysql.connector.connect(**con)
                cursorObj = cnx.cursor()
                cursorObj.execute("INSERT INTO empresas VALUES('"+rut+"','"+razon_social+"')")
                cnx.commit()
                cnx.close()
            except mysql.connector.InterfaceError as e:
                raise           
        else:
            print ("repetido")
        
    except mysql.connector.InterfaceError as e:
            raise        
#se inserta el detalle de las facturas
#entrada: con   = conexión
#         rut   = rut emisor factura
#         folio = folio factura
#         nombre= nombre asociado al ítem del detalle
#         monto =monto asociado al ítem del detalle
#         iva   =asociado al iva del detalle
def insert_detalle_factura(con,rut,folio, nombre,monto, iva):
    try:
        cnx= mysql.connector.connect(**con)
        cursorObj = cnx.cursor()
        cursorObj.execute("INSERT INTO detalle_factura VALUES('"+rut+"','"+folio+"','"+nombre+"',"+str(monto)+","+str(iva)+")")        
        cnx.commit()
        cnx.close()
    except mysql.connector.InterfaceError as e:
            raise
        
#se inserta la data de la factura
#entrada: con     = conexión
#         datetime= marca de tiempo
#         tipo    = si es boleta o factura
#         folio   = folio factura
#         emisor  = rut emisor
#         receptor= rut receptor
#         total   = monto total    
def insert_factura_boleta(con,datetime,tipo,folio,emisor, receptor,total):
    try:
        cnx = mysql.connector.connect(**con)
        cursorObj = cnx.cursor()
        cursorObj.execute("INSERT INTO facturas VALUES("+str(datetime)+",'"+tipo+"','"+folio+"','"+emisor+"','"+receptor+"',"+str(total)+")")
        cnx.commit()
        cnx.close()
    except mysql.connector.InterfaceError as e:
            raise

#se hacen los llamados para crear las tablas, esto se hace solo una vez
#entrada: con   = conexión
def crear_tablas(con):
    sql_tabla_factura(con)
    sql_tabla_detalle_factura(con)
    sql_tabla_emisor_receptor(con)


#se carga la data desde una carpeta de archivos xml las que se pasan a diferentes tablas
#entrada: con   = conexión
def cargar_data(con):
    lista_xml=lista_archivos('dte-files/')
    for xml in lista_xml:
        doc = minidom.parse("dte-files/"+xml)
        dte = doc.getElementsByTagName("dte")[0]
        emision=int(dte.getAttribute("emision"))
        tipo=dte.getAttribute("tipo")
        folio=dte.getAttribute("folio")
        emisor=dte.getElementsByTagName("emisor")[0]
        rut_emisor=emisor.getAttribute("rut")
        razon_emisor=emisor.getAttribute("razonSocial")
        receptor=dte.getElementsByTagName("receptor")[0]
        rut_receptor=receptor.getAttribute("rut")
        razon_receptor=receptor.getAttribute("razonSocial")
        detalle=dte.getElementsByTagName("items")[0].getElementsByTagName("detalle")
        i=0
        total=0
        while (i<len(detalle)):
            monto=int(detalle[i].getAttribute("monto"))
            iva=float(detalle[i].getAttribute("iva"))
            nombre=detalle[i].firstChild.nodeValue
            total=monto+total
            insert_detalle_factura(con,rut_emisor, folio,nombre,monto, iva)
            i=i+1
        insert_emisor_receptor(con,rut_emisor,razon_emisor)
        insert_emisor_receptor(con,rut_receptor,razon_receptor)
        insert_factura_boleta(con,emision,tipo, folio,rut_emisor,rut_receptor,total)
        

config = {
	'host': 'sql10.freemysqlhosting.net',
	'port': 3306,
	'database': 'sql10340036',
	'user': 'sql10340036',
	'password': 'XuxANBggVz',
	'charset': 'utf8',
	'use_unicode': True,
	'get_warnings': True,
}




#se crean las tablas, se hace una vez, luego se comenta la siguiente línea
crear_tablas(config)

#se carga la información
cargar_data(config)

