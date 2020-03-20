#!/usr/bin/python3

import pymysql
# import pymysql.cursor
# Open database connection
db = pymysql.connect(host="localhost", user="root", passwd="")

# prepare a cursor object using cursor() method
cursor = db.cursor()
cursor.execute('DROP DATABASE IF EXISTS AIRLINE')
sql = "CREATE DATABASE IF NOT EXISTS AIRLINE"
# db._execute_command


def Parts_analysis():
    print("Following are the available parts:")
    cursor.execute("SELECT ID FROM PARTS;")
    part = input("Enter the part id for which you want to check the reports: ")
    sql = "SELECT C.ID CRASH_ID, C.DATE_OF_PURCHASE, C.DATE_OF_INCIDENT, M.ID MANUFACTURER_ID, M.NAME MANUFACTURER_NAME FROM CRASHREPORTS C, PARTS P, PART_FAILURE_CRASH F, COMPANY M WHERE P.ID = %d AND F.PART_ID = P.ID AND M.ID = P.MANUFACTURER_ID AND C.ID = F.CRASHREPORT_ID;" % (
        part)
    cursor.execute(sql)


def Maintainence_cost():
    print("Following are the available parts:")
    cursor.execute("SELECT ID FROM PARTS;")
    part = input(
        "Enter the part id for which you want to check the maintainence reports: ")
    sql = "SELECT M.ID MANUFACTURER_ID, M.NAME MANUFACTURER_NAME, IFNULL(SUM(R.COST),0) TOTAL_COST  FROM MAINTENANCE_REPORTS R, CHANGED_PART C, PARTS P, COMPANY M WHERE P.ID = %d AND C.PART_ID = P.ID AND M.ID = P.MANUFACTURER_ID AND C.MAINTENANCE_REPORT_ID = R.ID;" % (
        part)
    cursor.execute(sql)


def Maintainence_cost_per_part():
    sql = "SELECT P.ID PART_ID, SUM(R.COST) TOTAL_COST  FROM MAINTENANCE_REPORTS R, CHANGED_PART C, PARTS P WHERE C.PART_ID = P.ID AND C.MAINTENANCE_REPORT_ID = R.ID GROUP BY P.ID;"
    cursor.execute(sql)


def Revenue_per_purchaser():
    print("Following are the revenue generated per purchasers:")

    sql = "SELECT P.ID, P.NAME, ABS(SUM(S.COST) - SUM(R.COST)) REVENUE FROM PURCHASER P, LIST_OF_PLANES L, SALE S, MAINTENANCE_REPORTS R WHERE L.SALE_ID = S.ID AND L.PURCHASER_ID = P.ID AND R.PLANE_MODEL_ID = L.ID AND S.COMPANY_ID = P.ID GROUP BY P.ID;"
    cursor.execute(sql)


def Analyst():
    while(1):
        print("You can choose from the following options")
        print("1. Analysis of crash report of companies manufacturinf a part")
        print("2. Analysis of maintenance of a part and companies manufacturing a part")
        print("3. Analysis of all the parts and the cost spent in manufacturing them")
        print("4. Analysis of total revenue generated from a purchaser")
        inp = input("Enter a number now: ")
        if inp == 1:
            Parts_analysis()

        elif inp == 2:
            Maintainence_cost()
        elif inp == 3:
            Maintainence_cost_per_part()
        elif inp == 4:
            Revenue_per_purchaser()
        else:
            print("Incorrect number")

def add_Purchase():
    print("Enter the following details")
    cname = input("Purchaser name: ")
    pname = input("Plane model name: ")
    qty = input("Enter quantity: ")
    prog = input("progress: ")
    dtp = input("date of purchase: ")
    dtd = input("date of commission: ")
    sql1 = "INSERT INTO PURCHASER (NAME) VALUES ('%s');" %(cname)
    cursor.execute(sql1)
    db.commit()
    sql = "INSERT INTO SALE (PLANE_MODEL_ID, COMPANY_ID, QUANTITY, PROGRESS) VALUES ((SELECT ID FROM PLANE WHERE NAME LIKE '%s'), (SELECT ID FROM PURCHASE WHERE NAME LIKE '%s'), %d, %d);"%(pname, cname, qty, prog)
    cursor.execute(sql)
    db.commit()
    sql = "INSERT INTO LIST_OF_PLANES (PLANE_MODEL_ID, PURCHASER_ID, DATE_OF_PURCHASE, SALE_ID, DECOMMISION_DATE) VALUES ((SELECT ID FROM PLANE WHERE NAME LIKE '%s'), (SELECT ID FROM PURCHASE WHERE NAME LIKE '%s'), %s, LAST_INSERT_ID(), '%s'));" %(pname, cname, dtp, dtd)
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
    dtd = input("cost: ")
    pid = input("id of the part changed")
    
    sql = "INSERT INTO MAINTENANCE_REPORTS (AUDITOR_ID, PLANE_MODEL_ID, MAINTENANCE_DATA, COST) VALUES ( (SELECT ID FROM AUDIT_AGENCY WHERE NAME LIKE '%s'), (SELECT ID FROM PLANE WHERE NAME LIKE '%s'), '%s', %d);"%(cname, pname, dtp, dtd)
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
    prog = input("Casualities: ")
    dtp = input("date of purchase: ")
    dtd = input("date of incident: ")
    dtm = input("date of last maintenance check: ")
    pid = input("id of the part that caused incident: ")
  
    sql = "INSERT INTO CRASHREPORTS (PLANE_MODEL_ID, DATE_OF_PURCHASE, DATE_OF_INCIDENT,DATE_OF_LAST_MAINTENANCE_CHECK, REASEON_FOR_CRASH, INVESTIGATING_AGENCY, CASUALITIES) VALUES ((SELECT ID FROM PLANE WHERE NAME LIKE '%s'),  %s, %s, %s, %s, (SELECT ID FROM PURCHASE WHERE NAME LIKE '%s'), '%s'))" %(pname, dtp, dtd, dtm, qty, cname, prog)

    cursor.execute(sql)
    db.commit()
    sql = "INSERT INTO PART_FAILURE_CRASH VALUES (LAST_INSERT_ID(), %s)" %(pid)
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
        inp = input("Enter a number now: ")
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

db.commit()


# disconnect from server
db.close()
