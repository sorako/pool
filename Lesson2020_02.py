import csv

import requests
from bokeh.io import output_file, show
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.transform import dodge
from bs4 import BeautifulSoup
from termcolor import colored


def unit_exchanger(s) :
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
    if s[0] == "("  and s[-1] == ")":
        s = (s[1:-1])
        if s[-1] == "M":
            s = float(s[:-1]) * 10 ** 6 * -1
        elif s[-1] == "B":
            s = float(s[:-1]) * 10 ** 9 * -1
        elif s[-1] == "T":
            s = float(s[:-1]) * 10 ** 12 * -1
        elif "," in s :
            s = s.replace ( ",","")
            s = float(s)*-1
        else :
            s = float(s) *10 ** 3 * -1

    elif s[-1] == "M":
        s = float(s[:-1]) * 10 ** 6
    elif s[-1] == "B":
        s = float(s[:-1]) * 10 ** 9
    elif s[-1] == "T":
        s = float(s[:-1]) * 10 ** 12
    elif "," in s :
        s = s.replace ( ",","")
        s = float(s)
    elif "-" in s :
        s = "NA"
    else :
        s = float(s) * 10 ** 3

    # float小数点を int整数 にする
    if s == "NA" :
        s = "NA"
    elif s.is_integer():
        s = int(s)
    elif s == int :
        s =int(s)

    else :
        s = int(s)

    return s

def unit_exchanger_fin (ll = None) :
    """
    unit_exchanger_fin is to exchange monetary unit in the scraped list by using unit_exchanger.
    ウェブから取得した四半期財務データを今後の利用のために整数にする関数、実際の関数計算はunit_exchangerで行っている。
    :param ll:
    list scraped from website

    :return:
    updated list with integers.

    """
    if ll is None :
         ll =[]

    return list(map(unit_exchanger, ll))




# ティッカーを入力し、アクセスするURLを生成
x = input('ティッカーを入力:')
url = "https://www.marketwatch.com/investing/stock/" + x + "/financials/income/quarter"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}
r = requests.get(url, headers=header)

# soup 変数にURLに含まれるhtmlをすべて打ち込んでパースにする。
soup = BeautifulSoup(r.content, "html.parser")

# 会社名取得
company_name = soup.find("h2").text.strip("Quarterly Financials for ")
print("企業名:", company_name)

# 本日の株価の抽出
print('現在の株価 $', soup.find("p", "data bgLast").text)

# 前日終値抽出
Laststockprice = soup.find("p", "lastcolumn data bgLast price")
Laststockprice.find("span", "currency").decompose()
LSP = Laststockprice.text
PreviousDay = LSP.strip()
print('前日終値　 $', PreviousDay)

# 前日比の抽出
PriceChange = soup.find("span", "bgChange").text
print('前日比 　 $', PriceChange)
PercentChange = soup.find("span", "bgPercentChange").text
print('前日比   　', PercentChange)

print("###########################")
print(colored("#####四半期データ  PL  ######","green"))

"""
四半期データの取得ーー決算期間の取得、thタグの費を取得
findAllで一旦thタグを全部取得してから、過去５期分の期間区分をperiod_rowとする
USダラーの会社の場合、注意必要かも！！（現在、USDもCanadaDも同じ値として扱っている。-為替が考慮されていない）
"""
th_row_ = soup.findAll("th")
period_row = th_row_[1:6]
currency = th_row_[0]
currency_text = currency.text
currency_in_short = currency_text.replace("millions.","")
print(currency_in_short)

Period_list = []
p = 0
for p in range(5):
    Period_list.append(period_row[p].text)
    p += 1
print("Period:", Period_list)

"""
四半期データの取得ーー売上金額の取得、tdタグの費を取得、繰り返し5期分を取得
<tr class="partialSum">タグで囲まれた表をまずrevenue_sum_に入れる。
revenueはそこからtd class="valueCell"で囲まれている売上数字を取得
空のリストRevenue_listを作成し、for loop でそこにテキスト要素を抜き出したものを加えている。
"""
revenue_sum = soup.find_all("tr", {"class": "partialSum"})[0]
revenues = revenue_sum.find_all("td", {"class":"valueCell"})

Revenue_list = []
i = 0
for i in range(5) :
    Revenue_list.append(revenues[i].text)
    i += 1
print("Revenues:", unit_exchanger_fin(Revenue_list))
Total_revenue = unit_exchanger_fin(Revenue_list)
"""
四半期データの取得ーーCost of Goods(COGS)販売経費の取得、繰り返し5期分を取得
COGS（販売経費）は必ず最初のtr class=mainRowに格納されているからわかりやすい
"""
main_rows = soup.find("tr", {"class": "mainRow"})
cogs_all = main_rows.find_all("td", {"class": "valueCell"})

cogs = []
c = 0
for c in range(5):
    cogs.append(cogs_all[c].text)
    c += 1

Total_cogs = unit_exchanger_fin(cogs)

"""
四半期データの取得ー　一般管理経費金額(SG&A Expense)の取得、繰り返し5期分を取得
SG&A Expense_はtr tag 13 番目ということで、tr[13]を指定
その後のRowの名前を出力することで、間違っていないかを確認
Expenseはそこからtd class="valueCell"で囲まれている売上数字を取得
ただし、一部企業はSG&Aが無く、Total Expense項目しかないため、if で条件分岐している
"""
Expense_row = soup.find_all("tr")[13]
SGA_Row_name = Expense_row.find("td", {"class":"rowTitle"})
Confirm_row_name = SGA_Row_name.text

if Confirm_row_name == " SG&A Expense" :
    print("COGS:", unit_exchanger_fin(cogs))
    print("Row_name:", SGA_Row_name.text)
    SGA_values = Expense_row.find_all("td", {"class": "valueCell"})
else :
    Expense_row = soup.find("tr", {"class": "mainRow"})
    SGA_Row_name = Expense_row.find("td", {"class": "rowTitle"})
    SGA_values = Expense_row.find_all("td", {"class": "valueCell"})
    print("Row_name:", SGA_Row_name.text)

SGA = []
s = 0
for i in range(5) :
    SGA.append(SGA_values[s].text)
    s += 1
print("SGA:", unit_exchanger_fin(SGA))
Total_SGA = unit_exchanger_fin(SGA)

#営業利益と営業利益率の計算
Gross_sales_profit =[]
gs = 0
for gs in range(5) :
    if "NA" == Total_revenue[gs] or "NA" == Total_cogs[gs] or "NA" == Total_SGA[gs] :
        Gross_sales_profit.append("NA")
    elif Total_SGA == Total_cogs :
        Gross_sales_profit.append(Total_revenue[gs] - + Total_SGA[gs])
    else :
        Gross_sales_profit.append(Total_revenue[gs]-(Total_cogs[gs] + Total_SGA[gs]))
    gs += 1
print("営業利益(四半期)：", Gross_sales_profit)

Gross_sales_margin = []
for gs in range(5) :
    if "NA" == Gross_sales_profit[gs] :
        Gross_sales_margin.append("NA")
    else :
        Gross_sales_margin.append(round(Gross_sales_profit[gs]/Total_revenue[gs],3))
        Gross_sales_margin[gs] ='{:.1%}'.format(Gross_sales_margin[gs])

    gs += 1

print("営業利益率(四半期)：", Gross_sales_margin)


"""
Net Inc数字を取得
totalRowのタグで最初に示されているため、取得しやすい
その後のRowの名前を出力することで、間違っていないかを確認
"""
netincome_row = soup.find_all("tr", {"class": "totalRow"})[0]
NetIncome_Row_name = netincome_row.find("td", {"class":"rowTitle"})
print("Row_name:", NetIncome_Row_name.text)
netIncome_all = netincome_row.find_all("td", {"class": "valueCell"})

NetIncome = []
n = 0
for n in range(5):
    NetIncome.append(netIncome_all[n].text)
    n += 1
print("Net_income:",unit_exchanger_fin(NetIncome))
NetIncome_Value = unit_exchanger_fin(NetIncome)


#Diluted EPSの取得(later)
print("###########################")

"""
CFの四半期データを変数にsoup_csに代入
soup_cs 変数にURLに含まれるhtmlをすべて打ち込んでパースにする。
"""
print(colored("#####四半期データ  CF  ######","green"))

url_cs = "https://www.marketwatch.com/investing/stock/" + x + "/financials/cash-flow/quarter"
cs = requests.get(url_cs)
soup_cs = BeautifulSoup(cs.content, "html.parser")

#Net Operating Cash Flowの取り込み
Net_OP_CF_row = soup_cs.find_all("tr", {"class": "totalRow"})[0]
Net_OP_CF_Values = Net_OP_CF_row.find_all("td",{"class": "valueCell"})
Net_OP_CF_rowTitle = Net_OP_CF_row.find("td",{"class":"rowTitle"})
print("Row_name:", Net_OP_CF_rowTitle.text)

Net_OP_CF =[]
o = 0
for z in range(5):
    Net_OP_CF.append(Net_OP_CF_Values[o].text)
    o += 1

print("Net_Operating_Cash_Flow:", unit_exchanger_fin(Net_OP_CF))
Net_OP_Cash_Flow_Value =unit_exchanger_fin(Net_OP_CF)

#Net investing Cash Flowの取り込み
Net_Inv_CF_row = soup_cs.find_all("tr", {"class": "totalRow"})[1]
Net_Inv_CF_Values = Net_Inv_CF_row.find_all("td",{"class": "valueCell"})
Net_Inv_CF_rowTitle = Net_Inv_CF_row.find("td",{"class":"rowTitle"})
print("Row_name:", Net_Inv_CF_rowTitle.text)

Net_Inv_CF =[]
b = 0
for b in range(5):
    Net_Inv_CF.append(Net_Inv_CF_Values[b].text)
    b += 1

print("Net_Investing_Cash_Flow:", unit_exchanger_fin(Net_Inv_CF))
Net_Inv_CF_Total = unit_exchanger_fin(Net_Inv_CF)

#Net Financing Cash Flowの取り込み
Net_FS_CF_row = soup_cs.find_all("tr", {"class": "totalRow"})[2]
Net_FS_CF_Values = Net_FS_CF_row.find_all("td",{"class": "valueCell"})
Net_FS_CF_rowTitle = Net_FS_CF_row.find("td",{"class":"rowTitle"})
print("Row_name:", Net_FS_CF_rowTitle.text)

Net_FS_CF =[]
c = 0
for c in range(5):
    Net_FS_CF.append(Net_FS_CF_Values[c].text)
    c += 1

print("Net_Financing_Cash_Flow:", unit_exchanger_fin(Net_FS_CF))
Net_financial_CF = unit_exchanger_fin(Net_FS_CF)

#FCF フリーキャッシュフローの計算（営業キャッシュフロー +　投資キャッシュフロー
FCF =[]
gs = 0
for gs in range(5) :
    if "NA" == Net_OP_Cash_Flow_Value[gs] or "NA" == Net_Inv_CF_Total[gs] :
        FCF.append("NA")
    else :
        FCF.append(Net_OP_Cash_Flow_Value[gs] + Net_Inv_CF_Total[gs])
    gs += 1
print("四半期フリーキャッシュフロー：", FCF)
print("###########################")


"""
BSからは総資産、自己資本を抽出
#BSの四半期データを変数にsoup_bsに代入
# soup_bs 変数にURLに含まれるhtmlをすべて打ち込んでパースにする。
"""

print(colored("#####四半期データ  BS  ######","green"))
url_bs = "https://www.marketwatch.com/investing/stock/" + x + "/financials/balance-sheet/quarter"
bs = requests.get(url_bs)
soup_bs = BeautifulSoup(bs.content, "html.parser")

#Total_Asset の取り込み
Total_Asset_Row = soup_bs.find_all("tr", {"class": "totalRow"})[0]
Total_Asset_Values = Total_Asset_Row.find_all("td",{"class": "valueCell"})
Total_Asset_rowTitle = Total_Asset_Row.find("td",{"class": "rowTitle"})
print("Row_name:", Total_Asset_rowTitle.text)

Total_Asset_Cash =[]
d = 0
for d in range(5):
    Total_Asset_Cash.append(Total_Asset_Values[d].text)
    d += 1

print("Total Asset:", unit_exchanger_fin(Total_Asset_Cash))
Total_Asset_Cash_Value = unit_exchanger_fin(Total_Asset_Cash)

#Total_Shareholder's Equity の取り込み
try :
    Total_SH_Row = soup_bs.find_all("tr", {"class": "partialSum"})[2]
except IndexError:
    Total_SH_Row = soup_bs.find_all("tr", {"class": "partialSum"})[0]

Total_SH_Values = Total_SH_Row.find_all("td",{"class": "valueCell"})
Total_SH_rowTitle = Total_SH_Row.find("td",{"class": "rowTitle"})

print("Row_name:", Total_SH_rowTitle.text)
Total_SH_Equity =[]
d = 0
for d in range(5):
    Total_SH_Equity.append(Total_SH_Values[d].text)
    d += 1

print("Total Shareholder's Equity:", unit_exchanger_fin(Total_SH_Equity))
Total_SH_Equity_Value =unit_exchanger_fin(Total_SH_Equity)

"""
自己資本比率、ROA総資産利益率、ROE自己資本利益率の計算

"""
#自己資本比率=Shareholder's Equity / Total Asset
gs = 0
Capital_Ratio = []
for gs in range(5) :
    if "NA" == Total_SH_Equity_Value[gs] :
        Capital_Ratio.append("NA")
    else :
        Capital_Ratio.append(round(Total_SH_Equity_Value[gs]/Total_Asset_Cash_Value[gs],3))
        Capital_Ratio[gs] ='{:.1%}'.format(Capital_Ratio[gs])

    gs += 1

print("四半期での自己資本比率：",Capital_Ratio)

#ROA総資産利益率（営業利益/ 資産Asset)
gs = 0
ROA = []
for gs in range(5) :
    if "NA" == Gross_sales_profit[gs] :
        ROA.append("NA")
    else :
        ROA.append(round(Gross_sales_profit[gs]/Total_Asset_Cash_Value[gs],3))
        ROA[gs] ='{:.1%}'.format(ROA[gs])

    gs += 1

print("ROA 四半期での総資産利益率：",ROA)

#ROE自己資本利益率(純利Net Profit / 自己資本Shareholder's Equity)
gs = 0
ROE = []
for gs in range(5) :
    if "NA" == Gross_sales_profit[gs] :
        ROE.append("NA")
    else :
        ROE.append(round(NetIncome_Value[gs]/Total_SH_Equity_Value[gs],3))
        ROE[gs] ='{:.1%}'.format(ROE[gs])

    gs += 1

print("ROE 四半期での自己資本利益率：",ROE)


#グラフをBokehライブラリを使って描画し、htmlファイルを出力する
#売上高、営業利益、純利益のグラフをまず作成する。

output_file(company_name + ".html")

periods = Period_list
g_title = ['売上', '営業利益', '純利益']


def na_judge (calc_list = None) :
    """
    リスト内に'NA'があった場合に、０を代入することで、グラフ表示でエラーを出さなくする
    :param calc_list: 売り上げなどのリスト
    :return: NAの場合は0を代入したリストを返す
    """
    for nj in range(5) :
        if 'NA' == calc_list[nj] :
            calc_list[nj]= 0
            nj += 1

    return calc_list

def non_converter (percentage_list =None) :
    """
    グラフ化にあたって、前段でNAを0に戻したものをグラフに表示させないためにnonに変換する
    :param percentage_list:
    :return:
    """
    for nzr in range(5) :
        if 0 == percentage_list[nzr] :
            percentage_list[nzr]= 'non'
            nzr += 1

    return percentage_list



Zero_Total_revenue = na_judge(Total_revenue).copy()
Zero_GSP = na_judge(Gross_sales_profit).copy()
na_judge(NetIncome_Value)

y_min = min(Zero_GSP)
if min(Zero_GSP) <= 0 or min(NetIncome_Value) <= 0 :
    if min(Zero_GSP) <= min(NetIncome_Value) :
        y_min = min(Zero_GSP)
    else :
        y_min = min(NetIncome_Value)
else :
    y_min =0
y_max = max(Zero_Total_revenue)

na_judge(Gross_sales_profit)
non_converter(Total_revenue)
non_converter(Gross_sales_profit)
non_converter(NetIncome_Value)

data = {'Quarter' : periods,
        'Revenue':Total_revenue,
        'GSP': Gross_sales_profit,
        'NetProfit': NetIncome_Value}
source = ColumnDataSource(data= data)



p = figure(x_range=periods, y_range=((y_min*1.1), (y_max*1.2)),sizing_mode="scale_width", plot_height=400, title=company_name +" 売上/営業利益/純利益",
           toolbar_location=None, tools="")

p.vbar(x=dodge('Quarter', -0.25, range=p.x_range), top='Revenue', width=0.2, source=source,
       color="#4331F5", legend_label="売上")

p.vbar(x=dodge('Quarter',  0.0,  range=p.x_range), top='GSP', width=0.2, source=source,
       color="#F0BE2C", legend_label="営業利益")

p.vbar(x=dodge('Quarter',  0.25, range=p.x_range), top='NetProfit', width=0.2, source=source,
       color="#e84d60", legend_label="純利益")

TOOLTIPS1 = [
    ('期間', '@Quarter'),
    ('売上', '@Revenue{($ 0.00 a)}'),
    ('営業利益', '@GSP{($ 0.00 a)}'),
    ('純利益', '@NetProfit{($ 0.00 a)}')
]

p.add_tools(HoverTool(tooltips=TOOLTIPS1))

p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.add_layout(p.legend[0], "below")
p.legend.orientation = "horizontal"

#show(p)

#収益性の営業利益率、ROA,ROEをグラフ化する
#’NA'を数字の０に変換
na_judge(Gross_sales_margin)
na_judge(ROA)
na_judge(ROE)

#各リストのfloat化
Gross_sales_margin_float = []
for gs in range(5) :
    if Zero_Total_revenue[gs] == 0:
        Gross_sales_margin_float.append(0)
    else :
        Gross_sales_margin_float.append(round(Zero_GSP[gs]/Total_revenue[gs],3))
    gs += 1


ROA_float =[]
for gs in range(5) :
    if Total_Asset_Cash_Value[gs] == 0:
        ROA_float.append(0)
    else :
        ROA_float.append(round(Zero_GSP[gs]/Total_Asset_Cash_Value[gs],3))
    gs += 1


ROE_float =[]
for gs in range(5) :
    if Total_SH_Equity_Value[gs] == 0:
        ROE_float.append(0)
    else :
        ROE_float.append(round(NetIncome_Value[gs]/Total_SH_Equity_Value[gs],3))
    gs += 1


#グラフの上下マージンを決めるためにyの値の最大値や最小値を取得
y_min2 = min(Gross_sales_margin_float)
if min(Gross_sales_margin_float) <= 0 or min(ROA_float) <= 0 or min(ROE_float) <= 0:
    if min(Gross_sales_margin_float) <= min(ROA_float) and min(Gross_sales_margin_float) <= min(ROE_float) :
        y_min2 = min(Gross_sales_margin_float)
    elif min(ROA_float) <= min(ROE_float) and min(ROA_float) <= min(Gross_sales_margin_float) :
        y_min2 = min(ROA_float)
    else :
        y_min2 = min(ROE_float)
else :
    y_min2 =0

y_max=0.5
if max(Gross_sales_margin_float) >= max(ROA_float) and max(Gross_sales_margin_float) >= max(ROE_float):
    if max(Gross_sales_margin_float) >= 0 :
        y_max = max(Gross_sales_margin_float)
    else :
        y_max = 0.5
elif max(ROA_float) >= max(ROE_float):
    if max(ROA_float) >= 0 :
        y_max = max(ROA_float)
    else :
        y_max = 0.5
elif max(ROE_float) <= 0 :
    y_max = 0.5
else :
    y_max = max(ROE_float)


non_converter(Gross_sales_margin_float)
non_converter(ROA_float)
non_converter(ROE_float)

#グラフ化
#output_file(company_name + "profitability.html")

data2 = {'Quarter' : periods,
        'Sales_margin':Gross_sales_margin_float,
        'ROA': ROA_float,
        'ROE': ROE_float}
source2 = ColumnDataSource(data= data2)

#グラフの描画
p2 = figure(x_range=periods, y_range=((y_min2*1.1), (y_max*1.2)),sizing_mode="scale_width", plot_height=400, title="収益性",
           toolbar_location=None, tools="")
p2.line(x='Quarter', y='Sales_margin', line_width=2, source=source2, line_color="#F0BE2C", legend_label="営業利益率")
p2.circle(x='Quarter', y='Sales_margin', line_width=1, source=source2, fill_color="#F0BE2C", size=8)
p2.line(x='Quarter', y ='ROA', line_width=2, source=source2, line_color="#4331F5", legend_label="ROA")
p2.circle(x='Quarter', y='ROA', line_width=1, source=source2, fill_color="#4331F5", size=8)

p2.line(x='Quarter', y ='ROE', line_width=2, source=source2, line_color="#e84d60", legend_label="ROE")
p2.circle(x='Quarter', y='ROE', line_width=1, source=source2, fill_color="#e84d60", size=8)

#p2 = figure(plot_width=600, plot_height=400)
#p2.vline_stack(['営業利益率', 'ROA', 'ROE'], x='x', source=source2)
p2.add_layout(p2.legend[0], "below")
p2.legend.orientation = "horizontal"

TOOLTIPS2 = [
    ('期間', '@Quarter'),
    ('営業利益率', '@Sales_margin{:.1%}'),
    ('ROA', '@ROA{:.1%}'),
    ('ROE', '@ROE{:.1%}')
]

p2.add_tools(HoverTool(tooltips=TOOLTIPS2))


#キャッシュフローのグラフ
na_judge(Net_OP_Cash_Flow_Value)
na_judge(Net_Inv_CF_Total)
na_judge(Net_financial_CF)
na_judge(FCF)


y3_min = []
y3_min.append(min(Net_OP_Cash_Flow_Value))
y3_min.append(min(Net_financial_CF))
y3_min.append(min(Net_Inv_CF_Total))
y3_min.append(min(FCF))
minifig = min(y3_min)

y3_max =[]
y3_max.append(max(Net_OP_Cash_Flow_Value))
y3_max.append(max(Net_financial_CF))
y3_max.append(max(Net_Inv_CF_Total))
y3_max.append(max(FCF))
maxfig = max(y3_max)

non_converter(Net_OP_Cash_Flow_Value)
non_converter(Net_Inv_CF_Total)
non_converter(Net_financial_CF)
non_converter(FCF)

data3 = {'Quarter' : periods,
        'OP_CF':Net_OP_Cash_Flow_Value,
        'Inv_CF': Net_Inv_CF_Total,
        'FIn_CF': Net_financial_CF,
        'Free_CF': FCF}

source3 = ColumnDataSource(data= data3)

p3 = figure(x_range=periods, y_range=((minifig*1.1), (maxfig*1.1)),sizing_mode="scale_width", plot_height=400, title="キャッシュフロー",
           toolbar_location=None, tools="")

p3.vbar(x=dodge('Quarter', -0.21, range=p.x_range), top='OP_CF', width=0.10, source=source3,
       color="#4331F5", legend_label="営業CF")

p3.vbar(x=dodge('Quarter',  -0.07,  range=p.x_range), top='Inv_CF', width=0.10, source=source3,
       color="#F0BE2C", legend_label="投資CF")

p3.vbar(x=dodge('Quarter',  0.07, range=p.x_range), top='FIn_CF', width=0.10, source=source3,
       color="#e84d60", legend_label="財務CF")

p3.vbar(x=dodge('Quarter',  0.21, range=p.x_range), top='Free_CF', width=0.10, source=source3,
       color="#249b00", legend_label="フリーCF")

p3.add_layout(p3.legend[0], "below")
p3.legend.orientation = "horizontal"

TOOLTIPS3 = [
    ('Quarter', '@Quarter'),
    ('営業CF', '@OP_CF{($ 0.00 a)}'),
    ('投資CF', '@Inv_CF{($ 0.00 a)}'),
    ('財務CF', '@FIn_CF{($ 0.00 a)}'),
    ('フリーCF','@Free_CF{($ 0.00 a)}')
]

p3.add_tools(HoverTool(tooltips=TOOLTIPS3))

show(column(p,p2,p3, sizing_mode="scale_width"))

#csvへの書き込み
Period_list.insert(0,"期間")
Total_revenue.insert(0,"売上")
Total_cogs.insert(0,"販売経費")
Total_SGA.insert(0,"一般経費")
Gross_sales_profit.insert(0,"営業利益")
Gross_sales_margin.insert(0,"営業利益率")
NetIncome_Value.insert(0,"純利益")
Net_OP_Cash_Flow_Value.insert(0,"営業CF")
Net_Inv_CF_Total.insert(0,"投資CF")
Net_financial_CF.insert(0,"財務CF")
FCF.insert(0,"フリーCF")
Total_Asset_Cash_Value.insert(0,"総資産")
Total_SH_Equity_Value.insert(0,"自己資本")
Capital_Ratio.insert(0,"自己資本比率")
ROA.insert(0,"ROA")
ROE.insert(0,"ROE")

#CSV生成にあたり、会社名からピリオドを除去したい(例):"Apple inc."→"Apple inc"
#if "\." in company_name :
#    company_name.rstrip("")
#print(company_name)

with open("/Users/yoshi_mbp2017/Documents/GitHub/site_pool/"+ company_name + ".csv", 'w', encoding="utf_8_sig") as f:
    writer = csv.writer(f)
    writer.writerow(["企業名:", company_name, currency_in_short])
    writer.writerow(Period_list)
    writer.writerow(Total_revenue)
    if Confirm_row_name == " SG&A Expense":
        writer.writerow(Total_cogs)
        writer.writerow(Total_SGA)
    else:
        Total_SGA.pop(0)
        Total_SGA.insert(0,"総経費")
        writer.writerow(["販売経費"])
        writer.writerow(Total_SGA)
    writer.writerow(Gross_sales_profit)
    writer.writerow(Gross_sales_margin)
    writer.writerow(NetIncome_Value)
    writer.writerow(Net_OP_Cash_Flow_Value)
    writer.writerow(Net_Inv_CF_Total)
    writer.writerow(Net_financial_CF)
    writer.writerow(FCF)
    writer.writerow(Total_Asset_Cash_Value)
    writer.writerow(Total_SH_Equity_Value)
    writer.writerow(Capital_Ratio)
    writer.writerow(ROA)
    writer.writerow(ROE)
