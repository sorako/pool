# -*- coding: utf-8 -*- 
import mySql
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import schedule
import time

def web_scraping():   
    mySql.deleteData()

    mySql.delete1Data()

    mySql.delete2Data()

    mySql.delete3Data()

    def unit_exchanger(s):
        """
        unit_changer is changing monetary units into digits.

        :param ll: list, including
        "M"=million, 1,000,000,
        B=billion, 1,000,000,000,
        "()" means negative figures, replace "(" into "-" and remove ")".

        :return:
        list with no abbreviation nor commas.
        リスト内のミリオンMやビリオンBの変換、およびコンマ除去、-符号の追加などを行う関数
        """
        if s[0] == "(" and s[-1] == ")":
            s = (s[1:-1])
            if s[-1] == "M":
                s = float(s[:-1]) * 10 ** 6 * -1
            elif s[-1] == "B":
                s = float(s[:-1]) * 10 ** 9 * -1
            elif s[-1] == "T":
                s = float(s[:-1]) * 10 ** 12 * -1
            elif "," in s:
                s = s.replace(",", "")
                s = float(s) * -1
            else:
                s = float(s) * 10 ** 3 * -1

        elif s[-1] == "M":
            s = float(s[:-1]) * 10 ** 6
        elif s[-1] == "B":
            s = float(s[:-1]) * 10 ** 9
        elif s[-1] == "T":
            s = float(s[:-1]) * 10 ** 12
        elif "," in s:
            s = s.replace(",", "")
            s = float(s)
        elif "-" in s:
            s = "NA"
        else:
            s = float(s) * 10 ** 3

        # float小数点を int整数 にする
        if s == "NA":
            s = "NA"
        elif s.is_integer():
            s = int(s)
        elif s == int:
            s = int(s)

        else:
            s = int(s)

        return s

    def unit_exchanger_fin(ll=None):
        """
        unit_exchanger_fin is to exchange monetary unit in the scraped list by using unit_exchanger.
        ウェブから取得した四半期財務データを今後の利用のために整数にする関数、実際の関数計算はunit_exchangerで行っている。
        :param ll:
        list scraped from website

        :return:
        updated list with integers.

        """
        if ll is None:
            ll = []

        return list(map(unit_exchanger, ll))

    def na_judge(calc_list=None):
        """
        リスト内に'NA'があった場合に、０を代入することで、グラフ表示でエラーを出さなくする
        :param calc_list: 売り上げなどのリスト
        :return: NAの場合は0を代入したリストを返す
        """
        for nj in range(1):
            if 'NA' == calc_list[nj]:
                calc_list[nj] = 0
                nj += 1

        return calc_list

    def non_converter(percentage_list=None):
        """
        グラフ化にあたって、前段でNAを0に戻したものをグラフに表示させないためにnonに変換する
        :param percentage_list:
        :return:
        """
        for nzr in range(5):
            if 0 == percentage_list[nzr]:
                percentage_list[nzr] = 'non'
                nzr += 1

        return percentage_list

    markets = ["ACRGF","TLLTF","GOOGl", "AAPL", "ABBV", "GWPH", "TCNNF", "GTBIF", "CURLF", "KSHB", "CRLBF", "TLRY", "HRVSF"
        , "AYRSF", "ITHUF", "GTBIF", "MEDIF", "APHA", "CWBHF", "ACRGF", "GRWG", "SNDL", "TRSSF", "PLNHF", "HSDEF",
               "GGBXF"
        , "CVSI", "VLNCF", "LHSIF", "NACNF", "IIPR", "MRMD", "HEXO", "CXXIF", "FFLWF", "INDXF", "LQSIF", "CRON", "YCBD"
        , "VFF", "SPRWF", "VREOF", "MJARF", "FFNTF"]
    for i in range(len(markets)):

        url = "https://www.marketwatch.com/investing/stock/" + markets[i] + "/financials/income/quarter"
        url1 = "https://finance.yahoo.com/quote/" + markets[i] + "?p=" + markets[i] + "&.tsrc=fin-srch"
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/69.0.3497.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
        r = requests.get(url, headers=header)
        r1 = requests.get(url1, headers=header)

        # soup 変数にURLに含まれるhtmlをすべて打ち込んでパースにする。
        soup = BeautifulSoup(r.content, "html.parser")
        soup1 = BeautifulSoup(r1.content, "html.parser")

        # 会社名取得
        company_name = soup.find("h2").text.strip("Quarterly Financials for ")
        print("企業名:", company_name)

        # 時価総額
        market_cap = soup1.find_all("table", "W(100%) M(0) Bdcl(c)")[0].find("td", "Ta(end) Fw(600) Lh(14px)").text
        print("時価総額:", market_cap)

        # symbols
        symbols = soup.find("p", {'class': 'textdeemphasized'}).text
        symbol = symbols.lstrip().rstrip()
        print("企業名:", symbol)

        # 本日の株価の抽出
        stock_price = soup.find("p", "data bgLast").text
        print('現在の株価 $', stock_price)

        # 前日終値抽出
        Laststockprice = soup.find("p", "lastcolumn data bgLast price")
        Laststockprice.find("span", "currency").decompose()
        LSP = Laststockprice.text
        previousDay = LSP.strip()
        print('前日終値　 $', previousDay)

        # 前日比の抽出
        priceChange = soup.find("span", "bgChange").text
        print('前日比 　 $', priceChange)
        percentChange = soup.find("span", "bgPercentChange").text
        print('前日比   　', percentChange)

        # save db
        mySql.insertData(company_name, market_cap, stock_price, symbol, previousDay, priceChange, percentChange)
        # company id 
        company_id = mySql.company_id()

        url_cs = "https://www.marketwatch.com/investing/stock/" + markets[i] + "/financials/cash-flow/quarter"
        cs = requests.get(url_cs)
        soup_cs = BeautifulSoup(cs.content, "html.parser")

        # Net Operating Cash Flowの取り込み
        Net_OP_CF_row = soup_cs.find_all("tr", {"class": "totalRow"})[0]
        Net_OP_CF_Values = Net_OP_CF_row.find_all("td", {"class": "valueCell"})
        Net_OP_CF_rowTitle = Net_OP_CF_row.find("td", {"class": "rowTitle"})
        # Net investing Cash Flowの取り込み
        Net_Inv_CF_row = soup_cs.find_all("tr", {"class": "totalRow"})[1]
        Net_Inv_CF_Values = Net_Inv_CF_row.find_all("td", {"class": "valueCell"})
        Net_Inv_CF_rowTitle = Net_Inv_CF_row.find("td", {"class": "rowTitle"})

        # Net Financing Cash Flowの取り込み
        Net_FS_CF_row = soup_cs.find_all("tr", {"class": "totalRow"})[2]
        Net_FS_CF_Values = Net_FS_CF_row.find_all("td", {"class": "valueCell"})
        Net_FS_CF_rowTitle = Net_FS_CF_row.find("td", {"class": "rowTitle"})

        url_bs = "https://www.marketwatch.com/investing/stock/" + markets[i] + "/financials/balance-sheet/quarter"
        bs = requests.get(url_bs)
        soup_bs = BeautifulSoup(bs.content, "html.parser")

        # Total_Asset の取り込み
        Total_Asset_Row = soup_bs.find_all("tr", {"class": "totalRow"})[0]
        Total_Asset_Values = Total_Asset_Row.find_all("td", {"class": "valueCell"})
        Total_Asset_rowTitle = Total_Asset_Row.find("td", {"class": "rowTitle"})
        s = 0
        for i in range(5):
            gs = 0
            """
            四半期データの取得ーー決算期間の取得、thタグの費を取得
            findAllで一旦thタグを全部取得してから、過去５期分の期間区分をperiod_rowとする
            USダラーの会社の場合、注意必要かも！！（現在、USDもCanadaDも同じ値として扱っている。-為替が考慮されていない）
            """
            th_row_ = soup.findAll("th")
            period_row = th_row_[1:6]
            currency = th_row_[0]
            currency_text = currency.text
            currency_in_short = currency_text.replace("millions.", "")
            Period_list = [period_row[i].text]

            """
            四半期データの取得ーー売上金額の取得、tdタグの費を取得、繰り返し5期分を取得
            <tr class="partialSum">タグで囲まれた表をまずrevenue_sum_に入れる。
            revenueはそこからtd class="valueCell"で囲まれている売上数字を取得
            空のリストRevenue_listを作成し、for loop でそこにテキスト要素を抜き出したものを加えている。
            """
            revenue_sum = soup.find_all("tr", {"class": "partialSum"})[0]
            revenues = revenue_sum.find_all("td", {"class": "valueCell"})

            Revenue_list = [revenues[i].text]
            Total_revenue = unit_exchanger_fin(Revenue_list)
            """
            四半期データの取得ーーCost of Goods(COGS)販売経費の取得、繰り返し5期分を取得
            COGS（販売経費）は必ず最初のtr class=mainRowに格納されているからわかりやすい
            """
            main_rows = soup.find("tr", {"class": "mainRow"})
            cogs_all = main_rows.find_all("td", {"class": "valueCell"})

            cogs = [cogs_all[i].text]
            Total_cogs = unit_exchanger_fin(cogs)

            """
            四半期データの取得ー　一般管理経費金額(SG&A Expense)の取得、繰り返し5期分を取得
            SG&A Expense_はtr tag 13 番目ということで、tr[13]を指定
            その後のRowの名前を出力することで、間違っていないかを確認
            Expenseはそこからtd class="valueCell"で囲まれている売上数字を取得
            ただし、一部企業はSG&Aが無く、Total Expense項目しかないため、if で条件分岐している
            """
            Expense_row = soup.find_all("tr")[13]
            SGA_Row_name = Expense_row.find("td", {"class": "rowTitle"})
            Confirm_row_name = SGA_Row_name.text

            SGA = []
            if Confirm_row_name == " SG&A Expense":
                SGA_values = Expense_row.find_all("td", {"class": "valueCell"})
            else:
                Expense_row = soup.find("tr", {"class": "mainRow"})
                SGA_Row_name = Expense_row.find("td", {"class": "rowTitle"})
                SGA_values = Expense_row.find_all("td", {"class": "valueCell"})
            SGA.append(SGA_values[i].text)
            Total_SGA = unit_exchanger_fin(SGA)

            # 営業利益と営業利益率の計算
            Gross_sales_profit = []
            gs = 0
            if "NA" == Total_revenue[gs] or "NA" == Total_cogs[gs] or "NA" == Total_SGA[gs]:
                Gross_sales_profit.append("NA")
            elif Total_SGA[gs] == Total_cogs[gs]:
                Gross_sales_profit.append(Total_revenue[gs] - + Total_SGA[gs])

            else:
                Gross_sales_profit.append(Total_revenue[gs] - (Total_cogs[gs] + Total_SGA[gs]))

            Gross_sales_margin = []
            if "NA" == Gross_sales_profit[gs]:
                Gross_sales_margin.append("NA")
            else:
                Gross_sales_margin.append(round(Gross_sales_profit[gs] / Total_revenue[gs], 3))
                Gross_sales_margin[gs] = '{:.1%}'.format(Gross_sales_margin[gs])

            """
            Net Inc数字を取得
            totalRowのタグで最初に示されているため、取得しやすい
            その後のRowの名前を出力することで、間違っていないかを確認
            """
            netincome_row = soup.find_all("tr", {"class": "totalRow"})[0]
            NetIncome_Row_name = netincome_row.find("td", {"class": "rowTitle"})
            netIncome_all = netincome_row.find_all("td", {"class": "valueCell"})

            NetIncome = [netIncome_all[i].text]
            NetIncome_Value = unit_exchanger_fin(NetIncome)

            Zero_Total_revenue = na_judge(Total_revenue).copy()
            Zero_GSP = na_judge(Gross_sales_profit).copy()

            Gross_sales_margin_float = []
            if Total_revenue[gs] == 0:
                Gross_sales_margin_float.append(0)
            else:
                # Gross_sales_margin_float.append(round(Gross_sales_profit[gs] / Total_revenue[gs], 3))
                Gross_sales_margin_float.append(round(Zero_GSP[gs] / Total_revenue[gs], 3))

            PL = Period_list, Total_cogs, Total_SGA, Gross_sales_profit, Gross_sales_margin, NetIncome_Value
            print(PL)

            Net_OP_CF = [Net_OP_CF_Values[i].text]
            Net_OP_Cash_Flow_Value = unit_exchanger_fin(Net_OP_CF)

            Net_Inv_CF = [Net_Inv_CF_Values[i].text]
            Net_Inv_CF_Total = unit_exchanger_fin(Net_Inv_CF)

            Net_FS_CF = [Net_FS_CF_Values[i].text]
            Net_financial_CF = unit_exchanger_fin(Net_FS_CF)

            FCF = []

            if "NA" == Net_OP_Cash_Flow_Value[gs] or "NA" == Net_Inv_CF_Total[gs]:
                FCF.append("NA")
            else:
                FCF.append(Net_OP_Cash_Flow_Value[gs] + Net_Inv_CF_Total[gs])

            CF = Net_OP_Cash_Flow_Value, Net_Inv_CF_Total, Net_financial_CF, FCF
            print(CF)

            Total_Asset_Cash = [Total_Asset_Values[i].text]
            Total_Asset_Cash_Value = unit_exchanger_fin(Total_Asset_Cash)
            na_judge(Total_Asset_Cash_Value)
            # Total_Shareholder's Equity の取り込み
            try:
                Total_SH_Row = soup_bs.find_all("tr", {"class": "partialSum"})[2]
            except IndexError:
                Total_SH_Row = soup_bs.find_all("tr", {"class": "partialSum"})[0]

            Total_SH_Values = Total_SH_Row.find_all("td", {"class": "valueCell"})
            Total_SH_rowTitle = Total_SH_Row.find("td", {"class": "rowTitle"})
            Total_SH_Equity = [Total_SH_Values[i].text]
            Total_SH_Equity_Value = unit_exchanger_fin(Total_SH_Equity)

            """
            自己資本比率、ROA総資産利益率、ROE自己資本利益率の計算
            """
            # 自己資本比率=Shareholder's Equity / Total Asset
            gs = 0
            Capital_Ratio = []
            if "NA" == Total_SH_Equity_Value[gs]:
                Capital_Ratio.append("NA")
            else:
                Capital_Ratio.append(round(Total_SH_Equity_Value[gs] / Total_Asset_Cash_Value[gs], 3))
                Capital_Ratio[gs] = '{:.1%}'.format(Capital_Ratio[gs])

            # ROA総資産利益率（営業利益/ 資産Asset)
            ROA = []
            if "NA" == Gross_sales_profit[gs]:
                ROA.append("NA")
            elif Total_Asset_Cash_Value[gs] == 0:
                 ROA.append(0)
            else:
                ROA.append(round(Gross_sales_profit[gs] / Total_Asset_Cash_Value[gs], 3))

                ROA[gs] = '{:.1%}'.format(ROA[gs])

            # ROE自己資本利益率(純利Net Profit / 自己資本Shareholder's Equity)
            na_judge(NetIncome_Value)
            na_judge(Total_SH_Equity_Value)
            
            ROE = []
            if "NA" == Gross_sales_profit[gs]:
                ROE.append("NA")
            elif Total_SH_Equity_Value[gs] == 0:
                 ROE.append(round(NetIncome_Value[gs],3))
            else:
                ROE.append(round(NetIncome_Value[gs] / Total_SH_Equity_Value[gs], 3))
                ROE[gs] = '{:.1%}'.format(ROE[gs])

            ROA_float = []
            if ROA[gs] == 0:
                ROA_float.append(0)
            else:
                ROA_float.append(round(Zero_GSP[gs] / Total_Asset_Cash_Value[gs], 3))

            ROE_float = []

            if Total_SH_Equity_Value[gs] == 0:
                ROE_float.append(0)
            else:
                ROE_float.append(round(NetIncome_Value[gs] / Total_SH_Equity_Value[gs], 3))

            BS = Total_Asset_Cash_Value[0], Total_SH_Equity_Value, Capital_Ratio, ROA, ROE

            mySql.insertDataCF(Net_OP_Cash_Flow_Value[0], Net_Inv_CF_Total[0], Net_financial_CF[0], FCF[0],
                               company_id[0])

            mySql.insertDataBS(Total_Asset_Cash_Value[0], Total_SH_Equity_Value[0], Capital_Ratio[0], ROA[0], ROE[0],
                               ROA_float[0], ROE_float[0], company_id[0])

            mySql.insertDataPL(Period_list[0],
                               Total_revenue[0],
                               Total_cogs[0],
                               Total_SGA[0],
                               Gross_sales_profit[0],
                               Gross_sales_margin[0],
                               NetIncome_Value[0],
                               Gross_sales_margin_float[0],
                               company_id[0])

            print(BS)

            i += 1
            gs += 1
