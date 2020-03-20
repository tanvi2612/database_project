import subprocess as sp
import pymysql

def display(table_name):
    query = "SELECT * FROM {}".format(str(table_name))
    cursor.execute(query)

    row = cursor.fetchone()
    while row is not None:
        print(row)
        row = cursor.fetchone()   

# ---- ADMIN START -----

## ---- AUDIT START ----

def add_audit():
    name = input("Enter Agency Name: ") 
    query = "INSERT INTO AUDIT_AGENCY (NAME) VALUES (%s)"
    try:
        cursor.execute(query, (name))
        db.commit()
    except:
        print("Error: Check value and try again")

def delete_audit():
    ID = int(input("Enter Agency ID: "))
    try:
        query = "DELETE FROM AUDIT_AGENCY WHERE ID = %s"
        cursor.execute(query, (ID))
        db.commit()
    except:
        print("Error: Check ID again and try again")

def update_audit():
    name = input("Enter Agency Name: ") 
    ID = int(input("Enter Agency ID to be updated: "))
    try:
        query = "UPDATE "
        cursor.execute(query, (ID))
        db.commit()
    except:
        print("Error: Check ID again and try again")

def audit():
    print("1. View All")
    print("2. Insert")
    print("3. Delete")
    print("4. Update")
    print("5. Quit")
    ch = int(input("Enter choice :> "))
    if ch is 5:
        return
    elif ch>=6 or ch<1:
        print("Error: Option does not exist.")
    else:
        if ch is 1:
            display("AUDIT_AGENCY")
        elif ch is 2:
            add_audit()
        elif ch is 3:
            delete_audit()
        elif ch is 4:
            update_audit()

## ----- AUDIT END -----
## ----- PURCHASER START -----

def add_purchaser():
    name = input("Enter Purchaser Name: ") 
    try:
        query = "INSERT INTO PURCHASER (NAME) VALUES (%s)"
        cursor.execute(query, (name))
        db.commit()
    except:
        print("Error.")

def delete_purchaser():
    ID = int(input("Enter Purchaser ID: "))
    try:
        query = "DELETE FROM PURCHASER WHERE ID = %s"
        cursor.execute(query, (ID))
        db.commit()
    except:
        print("Error.")

# def update_purchaser():


def purchaser():

    print("1. View All")
    print("2. Insert")
    print("3. Delete")
    print("4. Update")
    print("5. Quit")
    ch = int(input("Enter choice :> "))
    tmp = sp.call('clear',shell=True)
    if ch is 5:
        return
    elif ch>=6 or ch<1:
        print("Error: Option does not exist.")
    else:
        if ch is 1:
            display("PURCHASER")
        elif ch is 2:
            add_purchaser()
        elif ch is 3:
            delete_purchaser()
        elif ch is 4:
            update_purchaser()

## ---- PURCHASER END ------
## ---- COMPANY START ------

def add_company():
    name = input("Enter Manufacturer Name: ") 
    query = "INSERT INTO COMPANY (NAME) VALUES (%s)"
    try:
        cursor.execute(query, (name))
        db.commit()
    except:
        print("Error")

def delete_company():
    ID = int(input("Enter Company ID: "))
    query = "DELETE FROM COMPANY WHERE ID = %s"
    try:
        cursor.execute(query, (ID))
        db.commit()
    except:
        print("Error")

# def update_company():

def company():
    print("1. View All")
    print("2. Insert")
    print("3. Delete")
    print("4. Update")
    print("5. Quit")
    ch = int(input("Enter choice :> "))
    tmp = sp.call('clear',shell=True)
    if ch is 5:
        return
    elif ch>=6 or ch<1:
        print("Error: Option does not exist.")
    else:
        if ch is 1:
            display("COMPANY")
        elif ch is 2:
            add_company()
        elif ch is 3:
            delete_company()
        elif ch is 4:
            update_company()

## ---- COMPANY END --------
## ---- PARTS START --------

def add_parts():
	man_name = input("Enter Manufacturer Name: ") 
	part_name = input("Enter Part Name: ")
	classification = input("Enter Type of Part: ")

	try:
		if classification == "Engine" or classification == "engine":
			query = "SELECT EXISTS(SELECT * FROM ENGINE WHERE %s IN (SELECT NAME FROM ENGINE))"
			cursor.execute(query, (part_name))
			row = cursor.fetchone()
			
			if row[0] == 1:
				print("Part Already Exists")
			else:
				query = "SELECT EXISTS(SELECT * FROM COMPANY WHERE %s IN (SELECT NAME FROM COMPANY))"						
				cursor.execute(query, (man_name))
				row = cursor.fetchone()
				
				if row[0] == 0:
					add_company(man_name)

				query = "SELECT ID FROM COMPANY WHERE NAME = %s"
				cursor.execute(query, (man_name))
				row = cursor.fetchone()
				man_id = row[0]

				cost = int(input("Enter Cost of part: "))
				power = int(input("Enter Power of Engine: "))
				classification = input("Enter Type of Engine: ")
				
				query = "INSERT INTO PARTS (MANUFACTURER_ID,COST) VALUES (%s,%s)"
				print("Manufacturer id ",man_id,type(man_id))
				print("Cost ",cost,type(cost))
				cursor.execute(query, (int(man_id),int(cost)))

				print("Inserted into parts table")
				
				query = "SELECT ID FROM PARTS ORDER BY ID DESC LIMIT 1;"
				cursor.execute(query)
				row = cursor.fetchone()
				part_id = row[0]
				
				query = "INSERT INTO ENGINE (PART_ID,NAME,TYPE,POWER) VALUES (%s,%s,%s,%s);"
				cursor.execute(query,(part_id,part_name,classification,power))

				print("Inserted into engine table")
				print("Successfully Added")

				db.commit();

		elif classification == "Software" or classification == "software":
			query = "SELECT EXISTS(SELECT * FROM SOFTWARE WHERE %s IN (SELECT NAME FROM SOFTWARE))"
			cursor.execute(query, (part_name))
			row = cursor.fetchone()
			
			if row[0] == 1:
				print("Part Already Exists")
			else:
				query = "SELECT EXISTS(SELECT * FROM COMPANY WHERE %s IN (SELECT NAME FROM COMPANY))"						
				cursor.execute(query, (man_name))
				row = cursor.fetchone()
				
				if row[0] == 0:
					add_company(man_name)

				query = "SELECT ID FROM COMPANY WHERE NAME = %s"
				cursor.execute(query, (man_name))
				row = cursor.fetchone()
				man_id = row[0]

				cost = int(input("Enter Cost of part: "))
				
				query = "INSERT INTO PARTS (MANUFACTURER_ID,COST) VALUES (%s,%s)"
				print("Manufacturer id ",man_id,type(man_id))
				print("Cost ",cost,type(cost))
				cursor.execute(query, (int(man_id),int(cost)))

				print("Inserted into parts table")
				
				query = "SELECT ID FROM PARTS ORDER BY ID DESC LIMIT 1;"
				cursor.execute(query)
				row = cursor.fetchone()
				part_id = row[0]
				
				query = "INSERT INTO SOFTWARE (PART_ID,NAME) VALUES (%s,%s);"
				cursor.execute(query,(part_id,part_name))

				print("Inserted into engine table")
				print("Successfully Added")

				db.commit();
		else:
			print("Incorrect part type entered")
	except:
		print("Error found somewhere")

def delete_parts():
    ID = int(input("Enter Part ID: "))
    query = "DELETE FROM PARTS WHERE ID = %s"
    try:
        cursor.execute(query, (ID))
        db.commit()
    except:
        print("Error")	

def parts():
    print("1. View All")
    print("2. Insert")
    print("3. Delete")
    print("4. Update")
    print("5. Quit")
    ch = int(input("Enter choice :> "))
    tmp = sp.call('clear',shell=True)
    if ch is 5:
        return
    elif ch>=6 or ch<1:
        print("Error: Option does not exist.")
    else:
        if ch is 1:
            display("PARTS")
        elif ch is 2:
            add_parts()
        elif ch is 3:
            delete_parts()
        elif ch is 4:
            update_purchaser()

## --- PARTS END -------
## ------ PLANE START ---------


def add_plane():
	name = input("Enter Plane Model Name: ");

	query = "SELECT EXISTS(SELECT * FROM PLANE WHERE %s IN (SELECT NAME FROM PLANE))"
	cursor.execute(query, (name))
	row = cursor.fetchone()
	
	try:
		if row[0] == 1:
			print("Plane already exists")
		else:
			date_of_release = input("Enter Plane Release Date: ");
			
			query = "SELECT EXISTS(SELECT * FROM PLANE_AGE WHERE %s IN (SELECT DATE FROM PLANE_AGE))"
			cursor.execute(query, (date_of_release))
			row = cursor.fetchone()
			
			if row[0] == 0:
				query = "INSERT INTO PLANE_AGE VALUES(%s,TIMESTAMPDIFF(YEAR, %s, CURDATE()));"
				cursor.execute(query, (date_of_release,date_of_release))

			reference_code = ""
			while reference_code == "":
				reference_code = input("Enter Reference code: ");
				query = "SELECT EXISTS(SELECT * FROM PLANE WHERE %s IN (SELECT REFERENCE_CODE FROM PLANE))"
				cursor.execute(query, (date_of_release))
				row = cursor.fetchone()
				if row[0] == 1:
					print("Reference code already in use. Please Enter New Reference Code")
					reference_code = ""

			wing_dim = input("Enter Wingspan Dimensions: ");
			nose_dim = input("Enter Nose-Tail Dimensions: ");
			safe_runway_len = input("Enter Safe Runway Length: ");
			capacity = input("Enter Plane Capacity: ");

			query = "INSERT INTO PLANE (NAME,REFERENCE_CODE,DATE_OF_RELEASE,WINGSPAN_DIMENSIONS,NOSE_TAIL_DIMENSIONS,SAFE_RUNWAY_LENGTH,CAPACITY) VALUES (%s,%s,%s,%s,%s,%s,%s);"
			cursor.execute(query,(name,reference_code,date_of_release,wing_dim,nose_dim,safe_runway_len,capacity))
			db.commit()
	except:
		print("Error.")

def delete_plane():
    ID = int(input("Enter Plane ID: "))
    query = "DELETE FROM PLANE WHERE ID = %s"
    try:
        cursor.execute(query, (ID))
        db.commit()
    except:
        print("Error.")

def plane():
    print("1. View All")
    print("2. Insert")
    print("3. Delete")
    print("4. Update")
    print("5. Quit")
    ch = int(input("Enter choice :> "))
    tmp = sp.call('clear',shell=True)
    if ch is 5:
        return
    elif ch>=6 or ch<1:
        print("Error: Option does not exist.")
    else:
        if ch is 1:
            display("PLANE")
        elif ch is 2:
            add_plane()
        elif ch is 3:
            delete_plane()
        elif ch is 4:
            update_plane()

def admin():
    
    while(1):
        tmp = sp.call('clear',shell=True)
        print("1. Audit Table")
        print("2. Purchaser Table")
        print("3. Company Table")
        print("4. Parts Table")
        print("5. Plane Table")
        print("6. Quit")
        print("7. Clear")

        ch = int(input("Enter choice :> "))
        if ch==6:
            break
        elif ch>6 or ch<1:
            print("Error: Option does not exist.")
        else:
            if ch is 1:
                audit()
            elif ch is 2:
                purchaser()
            elif ch is 3:
                company()
            elif ch is 4:
                parts()
            else:
                plane()

# ----- ADMIN END ---------

# ----- EMPLOYEE START -----

def add_Purchase():
    print("Enter the following details")
    cname = input("Purchaser name: ")
    pname = input("Plane model name: ")
    qty = int(input("Enter quantity: "))
    prog = int(input("progress: "))
    dtp = input("date of purchase: ")
    dtd = input("date of commission: ")
    sql1 = "INSERT INTO PURCHASER (NAME) VALUES ('%s');" %(cname)
    cursor.execute(sql1)
    db.commit()
    
    sql = "INSERT INTO SALE (PLANE_MODEL_ID, COMPANY_ID, COST, QUANTITY, PROGRESS) VALUES ((SELECT ID FROM PLANE WHERE NAME = '%s'), (SELECT ID FROM PURCHASE WHERE NAME = '%s'), NULL, %d, %d);"%(pname, cname, qty, prog)
    cursor.execute(sql)
    db.commit()
    print("s1")
    sql = "INSERT INTO LIST_OF_PLANES (PLANE_MODEL_ID, PURCHASER_ID, DATE_OF_PURCHASE, SALE_ID, DECOMMISION_DATE) VALUES ((SELECT ID FROM PLANE WHERE NAME = '%s'), (SELECT ID FROM PURCHASE WHERE NAME = '%s'), %s, LAST_INSERT_ID(), '%s'));" %(pname, cname, dtp, dtd)
    cursor.execute(sql)
    db.commit()

def view_Purchase():
    sql = "SELECT P.ID, P.NAME, S.ID SALE_ID, S.PLANE_MODEL_ID, S.QUANTITY, S.PROGRESS, L.DATE_OF_PURCHASE, L.DECOMMISION_DATE FROM PURCHASER P, SALE S, LIST_OF_PLANES L WHERE P.ID = S.COMPANY_ID AND P.ID = L.PURCHASER_ID;"
    cursor.execute(sql)
    db.commit()

def add_Maintenance ():
    print("Enter the following details")
    cname = input("Audit Agency name: ")
    pname = input("Plane model name: ")
    dtp = input("date of maintenance: ")
    dtd = int(input("cost: "))
    pid = int(input("id of the part changed"))
    
    sql = "INSERT INTO MAINTENANCE_REPORTS (AUDITOR_ID, PLANE_MODEL_ID, MAINTENANCE_DATA, COST, PARTS_CHANGED) VALUES ( (SELECT ID FROM AUDIT_AGENCY WHERE NAME LIKE '%s'), (SELECT ID FROM PLANE WHERE NAME LIKE '%s'), '%s', %d,);"%(cname, pname, dtp, dtd)
    cursor.execute(sql)
    db.commit()
    sql = "INSERT INTO CHANGED_PART (MAINTENANCE_REPORT_ID, PART_ID) VALUES (LAST_INSERT_ID(), %d);" %(pid)
    cursor.execute(sql)
    db.commit()

def view_Maintenance():
    sql = "SELECT R.ID, R.PLANE_MODEL_ID, A.ID AUDITOR_ID, A.NAME AUDITOR_NAME, R.MAINTENANCE_DATA, C.PART_ID, R.COST FROM MAINTENANCE_REPORTS R, AUDIT_AGENCY A, CHANGED_PART C WHERE A.ID = R.AUDITOR_ID AND R.ID = C.MAINTENANCE_REPORT_ID;"
    cursor.execute(sql)
    db.commit()

def add_Crashreport():
    print("Enter the following details")
    cname = input("Investigating agency name: ")
    pname = input("Plane model name: ")
    qty = input("Reason for crash: ")
    prog = int(input("Casualities: "))
    dtp = input("date of purchase: ")
    dtd = input("date of incident: ")
    dtm = input("date of last maintenance check: ")
    pid = int(input("id of the part that caused incident: "))
  
    sql = "INSERT INTO CRASHREPORTS (PLANE_MODEL_ID, DATE_OF_PURCHASE, DATE_OF_INCIDENT,DATE_OF_LAST_MAINTENANCE_CHECK, REASON_FOR_CRASH, INVESTIGATING_AGENCY, CASUALITIES) VALUES ((SELECT ID FROM PLANE WHERE NAME = '%s'),  '%s', '%s', '%s', '%s', (SELECT ID FROM AUDIT_AGENCY WHERE NAME = '%s'), '%d))" %(pname, dtp, dtd, dtm, qty, cname, prog)

    cursor.execute(sql)
    db.commit()
    sql = "INSERT INTO PART_FAILURE_CRASH VALUES (LAST_INSERT_ID(), %d)" %(pid)
    cursor.execute(sql)
    db.commit()

def view_Crashreport():
    sql = "SELECT C.*, A.NAME INVESTING_AGENCY_NAME, P.PART_ID PART_FAILED FROM CRASHREPORTS C, AUDIT_AGENCY A, PART_FAILURE_CRASH P WHERE C.ID = P.CRASHREPORT_ID AND C.INVESTIGATING_AGENCY = A.ID;"
    cursor.execute(sql)
    db.commit()

def Employee():
    while(1):
        print("You can choose from the following options")
        print("1. Add a new purchase")
        print("2. View all purchases till a date")
        print("3. Add a new maintenance check")
        print("4. View all Maintenance checks till a date")
        print("5. Add a new crash report")
        print("6. View all Crash reports till a date")
        inp = int(input("Enter a number now: "))
        if inp == 1:
            add_Purchase()

        elif inp == 2:
            view_Purchase()
        elif inp == 3:
            add_Maintenance()
        elif inp == 4:
            view_Maintenance()
        elif inp == 5:
            add_Crashreport()
        elif inp == 6:
            view_Crashreport()
        else:
            print("Incorrect number")


# ----- EMPLOYEE END -------

# ----- ANALYSIS START -----

def Parts_analysis():
    print("Following are the available parts:")
    cursor.execute("SELECT ID FROM PARTS")
    result = cursor.fetchall()
    for x in result:
        print(x)
    part = int(input("Enter the part id for which you want to check the reports: "))
    sql = "SELECT C.ID CRASH_ID, C.DATE_OF_PURCHASE, C.DATE_OF_INCIDENT, M.ID MANUFACTURER_ID, M.NAME MANUFACTURER_NAME FROM CRASHREPORTS C, PARTS P, PART_FAILURE_CRASH F, COMPANY M WHERE P.ID = %d AND F.PART_ID = P.ID AND M.ID = P.MANUFACTURER_ID AND C.ID = F.CRASHREPORT_ID;" % (
        part)
    cursor.execute(sql)
    result = cursor.fetchall()
    for x in result:
        print(x)
    

def Maintainence_cost():
    print("Following are the available parts:")
    cursor.execute("SELECT ID FROM PARTS;")
    result = cursor.fetchall()
    for x in result:
        print(x)
    part = int(input(
        "Enter the part id for which you want to check the maintainence reports: "))
    sql = "SELECT M.ID MANUFACTURER_ID, M.NAME MANUFACTURER_NAME, IFNULL(SUM(R.COST),0) TOTAL_COST  FROM MAINTENANCE_REPORTS R, CHANGED_PART C, PARTS P, COMPANY M WHERE P.ID = %d AND C.PART_ID = P.ID AND M.ID = P.MANUFACTURER_ID AND C.MAINTENANCE_REPORT_ID = R.ID;" % (
        part)
    cursor.execute(sql)
    result = cursor.fetchall()
    for x in result:
        print(x)


def Maintainence_cost_per_part():
    sql = "SELECT P.ID PART_ID, SUM(R.COST) TOTAL_COST  FROM MAINTENANCE_REPORTS R, CHANGED_PART C, PARTS P WHERE C.PART_ID = P.ID AND C.MAINTENANCE_REPORT_ID = R.ID GROUP BY P.ID;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for x in result:
        print(x)


def Revenue_per_purchaser():
    print("Following are the revenue generated per purchasers:")

    sql = "SELECT P.ID, P.NAME, ABS(SUM(S.COST) - SUM(R.COST)) REVENUE FROM PURCHASER P, LIST_OF_PLANES L, SALE S, MAINTENANCE_REPORTS R WHERE L.SALE_ID = S.ID AND L.PURCHASER_ID = P.ID AND R.PLANE_MODEL_ID = L.ID AND S.COMPANY_ID = P.ID GROUP BY P.ID;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for x in result:
        print(x)

def analysis():

    while(1):
        tmp = sp.call('clear', shell=True)
        print("1. Analysis of crash report of companies manufacturing a part")
        print("2. Analysis of maintenance of a part and companies manufacturing a part")
        print("3. Analysis of all the parts and the cost spent in manufacturing them")
        print("4. Analysis of total revenue generated from a purchaser")
        print("5. Quit")
        ch = int(input("Enter choice :> "))

        if ch is 5:
            break
        else:
            if ch == 1:
                Parts_analysis()
            elif ch == 2:
                Maintainence_cost()
            elif ch == 3:
                Maintainence_cost_per_part()
            elif ch == 4:
                Revenue_per_purchaser()
            else:
                print("Incorrect number")

# ----- ANALYSIS END -----



def user_config(ch):
    if ch is 1:
        admin()
    elif ch is 2:
        Employee()
    elif ch is 3:
        analysis()
    else:
        print("Error: User does not exist")

tmp = sp.call('clear',shell=True)

try:
    con = db = pymysql.connect("localhost","root","","BOEING")
    tmp = sp.call('clear',shell=True)

    if(con.open):
        print("Connected")
    else:
        print("Failed to connect")

except:
    tmp = sp.call('clear',shell=True)
    print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
    tmp = input("Enter any key to CONTINUE>")

    tmp = input("Enter any key to CONTINUE>")

with con:
    cursor = cur = con.cursor()
    tmp = sp.call('clear',shell=True)
    print("1. Admin")
    print("2. Employee")
    print("3. Analyst")
    print("4. Quit")

    try:
        ch = int(input("Enter choice :> "))
        tmp = sp.call('clear',shell=True)
        if ch>4 or ch<1:
            print("User does not exist. Abort.")
        else:
            user_config(ch)
            tmp = input("Enter any key to CONTINUE>")
    except:
        print("Error")
