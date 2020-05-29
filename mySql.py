import mysql.connector

mydb = mysql.connector.connect(user='root', host='localhost', password='', database='cannabistock')

mycursor = mydb.cursor()
print("hello world123")


def insertData(company_name, stock_price, symbol, previousDay, priceChange, percentChange):
    sql = "INSERT INTO company ( company_name, stock_price, symbol,previousDay,priceChange,percentChange) VALUES (%s, %s, %s, %s, %s, %s)"
    val = [(company_name, stock_price, symbol, previousDay, priceChange, percentChange)]
    mycursor.executemany(sql, val)
    mydb.commit()


def company_id():
    mycursor.execute("SELECT max(id) FROM company")
    myresult = mycursor.fetchall()
    id = myresult[0]
    return id


def insertDataPL(period, revenues, COGS, operating_income, operating_profit, net_income, company_id):
    sql = "INSERT INTO quarterly_dataPL (period, revenues, COGS, operating_income, operating_profit, net_income,company_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = [(str(period), str(revenues), str(COGS), str(operating_income), str(operating_profit), str(net_income),
            str(company_id))]
    mycursor.executemany(sql, val)
    mydb.commit()


def insertDataCF(Net_Operating_Cash_Flow, Net_Investing_Cash_Flow, Net_Financing_Cash_Flow, Quarterly_free_cash_flow,
                 company_id):
    sql = "INSERT INTO quarterly_dataCF (Net_Operating_Cash_Flow, Net_Investing_Cash_Flow, Net_Financing_Cash_Flow, Quarterly_free_cash_flow,company_id) VALUES (%s, %s, %s, %s, %s)"
    val = [(str(Net_Operating_Cash_Flow), str(Net_Investing_Cash_Flow), str(Quarterly_free_cash_flow),
            str(Quarterly_free_cash_flow), str(company_id))]
    mycursor.executemany(sql, val)
    mydb.commit()


def insertDataBS(total_asset, adequacy_ratio, ROA, ROE, tot_shareholder_equity, company_id):
    sql = "INSERT INTO quarterly_dataBS (total_asset, adequacy_ratio, ROA, ROE,tot_shareholder_equity,company_id) VALUES (%s, %s, %s, %s, %s, %s)"
    val = [(str(total_asset), str(adequacy_ratio), str(ROA), str(ROE), str(tot_shareholder_equity), str(company_id))]
    mycursor.executemany(sql, val)
    mydb.commit()


def revenues():
    mycursor.execute("SELECT revenues FROM quarterly_dataPL")
    myresult = mycursor.fetchall()
    id = myresult[0]
    print(id)
    return id


mydb.close()
