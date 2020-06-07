window.onload = function() {
  document.getElementById('div1').style.display = 'none';
  document.getElementById('div2').style.display = 'none';
  document.getElementById('div3').style.display = 'none';
  document.getElementById('div4').style.display = 'none';
  document.getElementById('table').style.display = 'none';
};
var url = "http://54.213.65.49/api";
var ur1 = "http://54.213.65.49/api_pl";
var ur2 = "http://54.213.65.49/api_bs";
var ur3 = "http://54.213.65.49/api_cf";
var xhr;

if (window.XMLHttpRequest) {
    xhr = new XMLHttpRequest();
} else {
    xhr = new ActiveXObject("Microsoft.XMLHTTP");
}
xhr.onreadystatechange = function () {
  if (xhr.readyState == 4 && xhr.status == 200) {
    var res = JSON.parse(xhr.responseText),
      data = res.data;
    for(var i = 0; i < data.length; i++) {
      var ele = document.createElement("option");
      var value = data[i].id;
      var name = data[i].company_name;
      var symbol = data[i].symbol;
      $(".action").append("<option value="+value+">"+name+" "+symbol+"</option>"); 
    }
  }
}
xhr.open("GET", url, true);
xhr.send();

//id avaj company_name uzuuleh
function myFunction(id) {
  document.getElementById('div1').style.display = 'block';
  document.getElementById('div2').style.display = 'block';
  document.getElementById('div3').style.display = 'block';
  document.getElementById('div4').style.display = 'block';
  function na_judge(calc_list){
  // リスト内に'NA'があった場合に、０を代入することで、グラフ表示でエラーを出さなくする
  // :param calc_list: 売り上げなどのリスト
  // :return: NAの場合は0を代入したリストを返す
    for (nj = 0; nj < 5; nj++) {
      if (isNaN(calc_list[nj])) {
         calc_list[nj] = 0;
      }
    }  
     return calc_list; 
  }        
 
  function non_converter(percentage_list){
  // グラフ化にあたって、前段でNAを0に戻したものをグラフに表示させないためにnonに変換する
  // :param percentage_list:
  // :return:
    for (nzr = 0; nzr < 5; nzr++){
      if (0 == percentage_list[nzr]){

        percentage_list[nzr] = "non";
      }  
    }  
     return percentage_list ; 
  }     

  $.getJSON('http://54.213.65.49/api/'+id+'').done(function(datas) {
    var market = ["OTC","NAS","NYS","ASE"]
    var units = ['K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    var symbol = datas.data[0].symbol;
    document.getElementById("demo").innerHTML = datas.data[0].company_name;
    document.getElementById("tableNane").innerHTML = datas.data[0].company_name;
    document.getElementById("same").innerHTML = datas.data[0].stock_price +"ドル";
    for(i = 0; i < 3 ; i++){
      if(symbol.includes(units[i])){
        document.getElementById("market_cap").innerHTML = datas.data[0].market_cap.split(''+units[i]+'').join('');  
      } else {
         document.getElementById("market_cap").innerHTML = datas.data[0].market_cap.split(''+units[i]+'').join('');  
      }

    } 
    
    document.getElementById("priceChange").innerHTML = "前日比 :"+datas.data[0].priceChange +"ドル";
    document.getElementById("percentChange").innerHTML = datas.data[0].percentChange ;
    document.getElementById("percentChange1").innerHTML = datas.data[0].percentChange ;
    for(i = 0; i < 4 ; i++){
      if(symbol.includes(market[i])){
        document.getElementById("symbol").innerHTML = datas.data[0].symbol.split(''+market[i]+':').join('');  
      }
    }  
  })
  $.getJSON(ur1).done(function(datas) {
    var i = 0
    //New Array PL
    var arrPeriod = [];
    var arrRevenue = [];
    var arrCogs = [];
    var arrSga = [];
    var arr_Gross_sales_profit = [];
    var arr_Gross_sales_margin = [];
    var arr_Net_income = [];
    var arr_Gross_sales_margin_float = [];

    
    for (i = 0; i < datas.data.length; i++) {
      var company_id = datas.data[i].company_id;
      if(id == company_id){
        var pl = datas.data[i];
        //push array
        arrPeriod.push(pl.period.toString());
        arrRevenue.push(parseInt(pl.revenues));
        arrCogs.push(parseInt(pl.cogs))
        arrSga.push(parseInt(pl.sga));;
        arr_Gross_sales_profit.push(pl.sales_profit);
        arr_Gross_sales_margin.push(pl.sales_margin);
        arr_Net_income.push(parseInt(pl.net_income));
        arr_Gross_sales_margin_float.push(pl.Gross_sales_margin_float)
       
      } 
    }
    //data set
    var zero_Total_revenue = non_converter(arrRevenue);
    var zero_GSP = non_converter(arr_Gross_sales_profit);
    var netIncome_Value =  non_converter(arr_Net_income); 

    // barchart draw 売上/営業利益/純利益
    charts(arrPeriod,arrRevenue,arr_Gross_sales_profit,arr_Net_income);

    var y_min = Math.min.apply(Math, zero_GSP);
    if (Math.min.apply(Math, zero_GSP) <= 0 || Math.min.apply(Math, netIncome_Value)<= 0 ) {
      if(Math.min.apply(Math, zero_GSP) <= Math.min.apply(Math, netIncome_Value)){
        y_min = Math.min.apply(Math, zero_GSP);
      }else{
        y_min = Math.min.apply(Math, netIncome_Value);
      }
    }else{
      var y_max = Math.max.apply(Math, zero_GSP) ;
    }
    //New Array BS
    var arr_Total_Asset_Cash_Value = [];
    var arr_Total_SH_Equity_Value= [];
    var arr_Capital_Ratio= [];
    var arr_ROA = [];
    var arr_ROE = [];
    var arr_ROA_float = [];
    var arr_ROE_float = [];

    var arr_Net_OP_Cash_Flow_Value = [];
    var arr_Net_Inv_CF_Total = []; 
    var arr_Net_financial_CF = [];
    var arr_FCF = [];
    $.getJSON(ur3).done(function(datas) {
      for (i = 0; i < datas.data.length; i++) {
        var company_id = datas.data[i].company_id;
        if(id == company_id){
          var cf = datas.data[i];
          arr_Net_OP_Cash_Flow_Value.push(parseInt(cf.Net_Operating_Cash_Flow));
          arr_Net_Inv_CF_Total.push(parseInt(cf.Net_Financing_Cash_Flow));
          arr_Net_financial_CF.push(parseInt(cf.Net_Investing_Cash_Flow));
          arr_FCF.push(parseInt(cf.Quarterly_free_cash_flow))
        }
      }

      // barchart draw キャッシュフロー
      chart(
            arrPeriod,
            non_converter(arr_Net_OP_Cash_Flow_Value),
            non_converter(arr_Net_financial_CF),
            non_converter(arr_Net_Inv_CF_Total),
            non_converter(arr_FCF));
    })

    $.getJSON(ur2).done(function(datas) {
      for (i = 0; i < datas.data.length; i++) {
        var company_id = datas.data[i].company_id;
        if(id == company_id){
          var bs = datas.data[i];
           //push array
          arr_Total_Asset_Cash_Value.push(bs.Total_Asset_Cash_Value);
          arr_Total_SH_Equity_Value.push(bs.Total_SH_Equity_Value);
          arr_Capital_Ratio.push(bs.Capital_Ratio);
          arr_ROA.push(bs.ROA);
          arr_ROE.push(bs.ROE);
          arr_ROA_float.push(bs.ROA_float);
          arr_ROE_float.push(bs.ROE_float);
        }
      }

      // line chart draw
      chartLine(arrPeriod,
                arr_Gross_sales_margin_float,
                arr_ROA_float,
                arr_ROE_float);

      // line chart draw 収益性
      chartLine2(arrPeriod,
                arr_Gross_sales_margin_float,
                arr_ROA_float,
                arr_ROE_float);

      tableDraw(arrPeriod,
                arrRevenue,
                arrCogs,
                arrSga,
                arr_Gross_sales_profit,
                arr_Gross_sales_margin,
                arr_Net_income,
                arr_Net_OP_Cash_Flow_Value,
                arr_Net_Inv_CF_Total,
                arr_Net_financial_CF,
                arr_FCF,
                arr_Total_Asset_Cash_Value,
                arr_Total_SH_Equity_Value,
                arr_Capital_Ratio,
                arr_ROA,
                arr_ROE); 
    })   
  })  
} 
function showStuff(id, text, btn) {
    document.getElementById(id).style.display = 'block';
    // hide the lorem ipsum text
    document.getElementById(text).style.display = 'none';
    // hide the link
    btn.style.display = 'none';
}
function chartLine(dataPeriod,data4,data5,data6){
    new Chart(document.getElementById("line-chart"), {
    type: 'line',
    scaleStartValue: 0,    
    data: {
      labels: dataPeriod,
      datasets: [{ 
          data: data4,
          label: "営業利益率",
          borderColor: "#F0BE2C",
          lineTension: 0,
          fill: false

        }, { 
          data: data5,
          label: "ROA",
          borderColor: "#4331F5",
          lineTension: 0,
          fill: false
        }, { 
          data: data6,
          label: "ROE",
          borderColor: "#e84d60",
          lineTension: 0,
          fill: false
        }
      ]
    },
    options: {

    title: {
      display: true,
      text: '収益性'
    },
    legend: {
        position: "bottom",
        align: "end",
        labels: {}
    },
    
      tooltips: {
      mode: 'label',
      callbacks: {
        label: function(tooltipItem, data) {
          var title = data.datasets[tooltipItem.datasetIndex].label;
          function shortenLargeNumber(num, digits) {
            var units = ['k', 'm', 'b', 't', 'p', 'e', 'z', 'y'],
            decimal;
            for(var i=units.length-1; i>=0; i--) {
                decimal = Math.pow(1000, i+1);
                if(num <= -decimal || num >= decimal) {
                  return +(num / decimal).toFixed(digits) + units[i];
                }
            }
            return num;
          }  
          var value = shortenLargeNumber(tooltipItem.yLabel, 3);
        return  title + ":  $ " + value; }, },
      },
      scales: {
        yAxes: [{
          ticks: {
            callback: function(label, index, labels) {
              function shortenLargeNumber(num, digits) {
                var units = ['k', 'm', 'b', 't', 'p', 'e', 'z', 'y'],
                decimal;
                for(var i=units.length-1; i>=0; i--) {
                  decimal = Math.pow(1000, i+1);

                  if(num <= -decimal || num >= decimal) {
                      return +(num / decimal).toFixed(digits) + units[i];
                  }
                }
                return num;
              }
              return  shortenLargeNumber(label, 3);
            }
          }
        }]
      }
    }   
  });
}

function chartLine2(dataPeriod,data4,data5,data6){
    new Chart(document.getElementById("line-chart2"), {
    type: 'line',
    scaleStartValue: 0,    
    data: {
      labels: dataPeriod,
      datasets: [{ 
          data: data4,
          label: "営業利益率",
          borderColor: "#F0BE2C",
          lineTension: 0,
          fill: false

        }, { 
          data: data5,
          label: "ROA",
          borderColor: "#4331F5",
          lineTension: 0,
          fill: false
        }, { 
          data: data6,
          label: "ROE",
          borderColor: "#e84d60",
          lineTension: 0,
          fill: false
        }
      ]
    },
    options: {

    title: {
      display: true,
      text: '収益性'
    },
    legend: {
        position: "bottom",
        align: "end",
        labels: {}
    },
    
      tooltips: {
      mode: 'label',
      callbacks: {
        label: function(tooltipItem, data) {
          var title = data.datasets[tooltipItem.datasetIndex].label;
          function shortenLargeNumber(num, digits) {
            var units = ['k', 'm', 'b', 't', 'p', 'e', 'z', 'y'],
            decimal;
            for(var i=units.length-1; i>=0; i--) {
                decimal = Math.pow(1000, i+1);
                if(num <= -decimal || num >= decimal) {
                  return +(num / decimal).toFixed(digits) + units[i];
                }
            }
            return num;
          }  
          var value = shortenLargeNumber(tooltipItem.yLabel, 3);
        return  title + ":  $ " + value; }, },
      },
      scales: {
        yAxes: [{
          ticks: {
            callback: function(label, index, labels) {
              function shortenLargeNumber(num, digits) {
                var units = ['k', 'm', 'b', 't', 'p', 'e', 'z', 'y'],
                decimal;
                for(var i=units.length-1; i>=0; i--) {
                  decimal = Math.pow(1000, i+1);

                  if(num <= -decimal || num >= decimal) {
                      return +(num / decimal).toFixed(digits) + units[i];
                  }
                }
                return num;
              }
              return  shortenLargeNumber(label, 3);
            }
          }
        }]
      }
    }   
  });
}

function charts(dataPeriod,data1,data2,data3){
  var barChartData = {
    labels: dataPeriod,
    datasets: [{
      label: '売上',
      backgroundColor: '#3366ff',
      data: data1
    }, {
      label: '営業利益',
      backgroundColor: "#ff9900",
      data: data2
    }, {
      label: '純利益',
      backgroundColor: "#ff6666",
      data: data3
    }]
  };
  var ctxBar = document.getElementById("chart-bars");
  if(window.bar != undefined) 
  window.bar.destroy(); 
  window.bar = new Chart(ctxBar, {
    type: 'bar',
    data: barChartData,
    options:{
      title: {
        display: true,
        fontStyle: 'bold',
        align: "start",
        text: "売上/営業利益/純利益"
      },
      legend: {
        position: "bottom",
        align: "end",
        labels: {}
      },

      tooltips: {
        mode: 'label',
        callbacks: {
          label: function(tooltipItem, data) {
            var title = data.datasets[tooltipItem.datasetIndex].label;
            function shortenLargeNumber(num, digits) {
              var units = ['k', 'm', 'b', 't', 'p', 'e', 'z', 'y'],
              decimal;
              for(var i=units.length-1; i>=0; i--) {
                  decimal = Math.pow(1000, i+1);
                  if(num <= -decimal || num >= decimal) {
                    return +(num / decimal).toFixed(digits) + units[i];
                  }
              }
              return num;
            }  
            var value = shortenLargeNumber(tooltipItem.yLabel, 3);
          return  title + ":  $ " + value; }, },
      },
      scales: {
      yAxes: [
          {
            ticks: {
              callback: function(label, index, labels) {
                function shortenLargeNumber(num, digits) {
                  var units = ['k', 'm', 'b', 't', 'p', 'e', 'z', 'y'],
                  decimal;
                  for(var i=units.length-1; i>=0; i--) {
                    decimal = Math.pow(1000, i+1);

                    if(num <= -decimal || num >= decimal) {
                        return +(num / decimal).toFixed(digits) + units[i];
                    }
                  }
                  return num;
                }
                return  shortenLargeNumber(label, 3);
              }
            }
          }
        ]
      }
    }   
  });
}

function chart(dataPeriod,data1,data2,data3,data4){
  var barChartData = {
    labels: dataPeriod,
    datasets: [{
      label: '営業CF',
      backgroundColor: '#3366ff',
      data: data1
    }, {
      label: '投資CF',
      backgroundColor: "#ff9900",
      data: data2
    }, {
      label: '財務CF',
      backgroundColor: "#ff6666",
      data: data3
    },{
      label: 'フリーCF',
      backgroundColor: "#33cc33",
      data: data4
    }]
  };
  var ctx = document.getElementById("barChart");
  var barChart =
   new Chart(ctx, {
    type: 'bar',
    data: barChartData,
    options:{
      title: {
        display: true,
        fontStyle: 'bold',
        text: "キャッシュフロー"
      },
      legend: {
        position: "bottom",
        align: "end",
        labels: {}
      },
      tooltips: {
        mode: 'label',
        callbacks: {
          label: function(tooltipItem, data) {
            var title = data.datasets[tooltipItem.datasetIndex].label;
            function shortenLargeNumber(num, digits) {
              var units = ['k', 'm', 'b', 't', 'p', 'e', 'z', 'y'],
              decimal;
              for(var i=units.length-1; i>=0; i--) {
                  decimal = Math.pow(1000, i+1);
                  if(num <= -decimal || num >= decimal) {
                    return +(num / decimal).toFixed(digits) + units[i];
                  }
              }
              return num;
            }  
            var value = shortenLargeNumber(tooltipItem.yLabel, 3);
          return  title + ":  $ " + value; }, },
      },
      scales: {
      yAxes: [
          {
            ticks: {
              callback: function(label, index, labels) {
                function shortenLargeNumber(num, digits) {
                  var units = ['k', 'm', 'b', 't', 'p', 'e', 'z', 'y'],
                  decimal;
                  for(var i=units.length-1; i>=0; i--) {
                    decimal = Math.pow(1000, i+1);

                    if(num <= -decimal || num >= decimal) {
                        return +(num / decimal).toFixed(digits) + units[i];
                    }
                  }
                  return num;
                }
                return  shortenLargeNumber(label, 3);
              }
            }
          }
        ]
      }
    }   
  });
}

function showOrHide(rowNumber) { 
  

    var div = document.getElementById("links_"+ rowNumber);
    if (div.style.display == "block") 
    {
        div.style.display = "none";
    }
    else 
    {
        div.style.display = "block";
    }
                             
}

function tableDraw( arrPeriod,
                    arrRevenue,
                    arrCogs,
                    arrSga,
                    arr_Gross_sales_profit,
                    arr_Gross_sales_margin,
                    arr_Net_income,
                    arr_Net_OP_Cash_Flow_Value,
                    arr_Net_Inv_CF_Total,
                    arr_Net_financial_CF,
                    arr_FCF,
                    arr_Total_Asset_Cash_Value,
                    arr_Total_SH_Equity_Value,
                    arr_Capital_Ratio,
                    arr_ROA,
                    arr_ROE){

  var Table = document.getElementById("table-body");
  Table.innerHTML = "";



  var date = arrPeriod; 
  date.unshift("期間");
  arrRevenue.unshift("売上");
  arrCogs.unshift('販売経費');
  arrSga.unshift('一般経費');
  arr_Gross_sales_profit.unshift('営業利益');
  arr_Gross_sales_margin.unshift('営業利益率');
  arr_Net_income.unshift("純利益");
  arr_Net_OP_Cash_Flow_Value.unshift("営業CF");
  arr_Net_Inv_CF_Total.unshift("投資CF");
  arr_Net_financial_CF.unshift("財務CF");
  arr_FCF.unshift("フリーCF");
  arr_Total_Asset_Cash_Value.unshift("総資産");
  arr_Total_SH_Equity_Value.unshift("自己資本");
  arr_Capital_Ratio.unshift("自己資本比率");
  arr_ROA.unshift("ROA");
  arr_ROE.unshift("ROE");

  if(arr_Total_Asset_Cash_Value.constructor === Object || arr_Net_OP_Cash_Flow_Value.constructor === Object ){
    document.getElementById('table').style.display = 'none';
  }else{
    document.getElementById('table').style.display = 'block';
  }
  let data = [arrPeriod,
  arrRevenue,
  arrCogs,
  arrSga,
  arr_Gross_sales_profit,
  arr_Gross_sales_margin,
  arr_Net_income,
  arr_Net_OP_Cash_Flow_Value,
  arr_Net_Inv_CF_Total,
  arr_Net_financial_CF,
  arr_FCF,
  arr_Total_Asset_Cash_Value,
  arr_Total_SH_Equity_Value,
  arr_Capital_Ratio,
  arr_ROA,
  arr_ROE];
  
  let tbody = document.getElementById('table-body');
  let tr, td;

  data.forEach((element) => {
      tr = document.createElement('tr');
      for (let key in element) {
          if (element.hasOwnProperty(key)) {
              td = document.createElement('td');
              td.innerHTML = element[key];
              tr.appendChild(td);
          }
      }
      tbody.appendChild(tr);
  });
}  

