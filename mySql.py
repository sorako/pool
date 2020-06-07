import mysql.connector

mydb = mysql.connector.connect(user='root', host='localhost', password='', database='cannabistock')

mycursor = mydb.cursor()


def deleteData():
    sql_Delete_query = "DELETE FROM  company;"
    sql_1 = " ALTER TABLE company AUTO_INCREMENT=0;"
    mycursor.execute(sql_Delete_query)
    mycursor.execute(sql_1)
    mydb.commit()
    print("company Deleted successfully ")


def delete1Data():
    sql_Delete_query = "DELETE FROM quarterly_dataPL;"
    sql_1 = "ALTER TABLE quarterly_dataPL AUTO_INCREMENT=0;"
    mycursor.execute(sql_Delete_query)
    mycursor.execute(sql_1)
    mydb.commit()
    print("quarterly_dataPL Deleted successfully ")


def delete2Data():
    sql_Delete_query = "DELETE FROM quarterly_dataCF;"
    sql_1 = "ALTER TABLE quarterly_dataCF AUTO_INCREMENT=0;"
    mycursor.execute(sql_Delete_query)
    mycursor.execute(sql_1)
    mydb.commit()
    print("quarterly_dataCF Deleted successfully ")


def delete3Data():
    sql_Delete_query = "DELETE FROM quarterly_dataBS;"
    sql_1 = "ALTER TABLE quarterly_dataBS AUTO_INCREMENT=0;"
    mycursor.execute(sql_Delete_query)
    mycursor.execute(sql_1)
    mydb.commit()
    print("quarterly_dataBS Deleted successfully ")


def insertData(company_name, market_cap, stock_price, symbol, previousDay, priceChange, percentChange):
    sql = "INSERT INTO company ( company_name, market_cap, stock_price, symbol,previousDay,priceChange,percentChange) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = [(company_name, market_cap, stock_price, symbol, previousDay, priceChange, percentChange)]
    mycursor.executemany(sql, val)
    mydb.commit()


def company_id():
    mycursor.execute("SELECT max(id) FROM company")
    myresult = mycursor.fetchall()
    id = myresult[0]
    return id


def insertDataPL(period, revenues, cogs, sga, sales_profit, sales_margin, net_income, Gross_sales_margin_float, company_id):
    sql = "INSERT INTO quarterly_dataPL (period, revenues, cogs, sga, sales_profit, sales_margin, net_income, Gross_sales_margin_float, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = [(str(period), str(revenues), str(cogs), str(sga), str(sales_profit), str(sales_margin), str(net_income), str(Gross_sales_margin_float), str(company_id))]
    mycursor.executemany(sql, val)
    mydb.commit()


def insertDataCF(Net_Operating_Cash_Flow, Net_Investing_Cash_Flow, Net_Financing_Cash_Flow, Quarterly_free_cash_flow,
                 company_id):
    sql = "INSERT INTO quarterly_dataCF (Net_Operating_Cash_Flow, Net_Investing_Cash_Flow, Net_Financing_Cash_Flow, Quarterly_free_cash_flow, company_id) VALUES (%s, %s, %s, %s, %s)"
    val = [(str(Net_Operating_Cash_Flow), str(Net_Investing_Cash_Flow), str(Net_Financing_Cash_Flow),
            str(Quarterly_free_cash_flow), str(company_id))]
    mycursor.executemany(sql, val)
    mydb.commit()



def insertDataBS(Total_Asset_Cash_Value, Total_SH_Equity_Value, Capital_Ratio, ROA, ROE, ROA_float, ROE_float, company_id):
    sql = "INSERT INTO quarterly_dataBS (Total_Asset_Cash_Value, Total_SH_Equity_Value, Capital_Ratio, ROA, ROE, ROA_float, ROE_float, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = [(str(Total_Asset_Cash_Value), str(Total_SH_Equity_Value), str(Capital_Ratio), str(ROA), str(ROE), str(ROA_float), str(ROE_float), str(company_id))]
    mycursor.executemany(sql, val)
    mydb.commit()
