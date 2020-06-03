
var url = "http://54.213.65.49/api";
var ur1 = "http://54.213.65.49/api_pl";
var ur2 = "http://54.213.65.49/api_bs";
var ur3 = "http://54.213.65.49/api_cf";
var id = 0
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
    var substring = "OTC";
    var substring1 = "NAS";
    var substring2 = "NYS";
    var substring3 = "ASE";
    var market = ["OTC","NAS","NYS","ASE"]
    var symbol = datas.data[0].symbol
    document.getElementById("demo").innerHTML = datas.data[0].company_name;
    document.getElementById("same").innerHTML = datas.data[0].stock_price +"ドル";
    document.getElementById("priceChange").innerHTML = "前日比 :"+datas.data[0].priceChange +"ドル";
    document.getElementById("percentChange").innerHTML = datas.data[0].percentChange ;
    document.getElementById("percentChange1").innerHTML = datas.data[0].percentChange ;
    for(i = 0; i < 5 ; i++){
      if(symbol.includes(market[i])){
        document.getElementById("symbol").innerHTML = datas.data[0].symbol.split(''+market[i]+':').join('');  
      }
    }  
  })
  $.getJSON(ur1).done(function(datas) {
    var i = 0
    arrPeriod = []
    arrRevenue = []
    arr_Gross_sales_profit = []
    arr_Net_income = []
    testPeriod = []
    for (i = 0; i < datas.data.length; i++) {
      var company_id = datas.data[i].company_id;
      if(id == company_id){
        var company = datas.data[i];
        var period = company.period.toString();
        var revenue = parseInt(company.revenues);
        var sales_profit = parseInt(company.operating_income);
        var net_income = parseInt(company.net_income);
        arrPeriod.push(period);
        arrRevenue.push(revenue);
        arr_Gross_sales_profit.push(sales_profit);
        arr_Net_income.push(net_income);
      } 
    }
    var zero_Total_revenue = non_converter(arrRevenue);
    var zero_GSP = non_converter(arr_Gross_sales_profit);
    var netIncome_Value =  non_converter(arr_Net_income); 
    var arrayLabel = arrPeriod;
    var data1 = arrRevenue;
    var data2 = arr_Gross_sales_profit;
    var data3 = arr_Net_income;
    charts(arrayLabel,data1,data2,data3);
   
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
   
    total_assets = [];
    adequacy_ratios = [];
    roas = [];
    roes = [];
    $.getJSON(ur2).done(function(datas) {
      for (i = 0; i < datas.data.length; i++) {
        var company_id = datas.data[i].company_id;
        if(id == company_id){
          var bs = datas.data[i];
          var total_asset = parseInt(bs.total_asset);
          total_assets.push(total_asset);
          var adequacy_ratio =  parseInt(bs.tot_shareholder_equity);
          adequacy_ratios.push(adequacy_ratio);
          var roa =  parseInt(bs.ROA);
          roas.push(roa);
          var roe =  parseInt(bs.ROE);
          roes.push(roe);
        }
      }
     
      var gross_sales_margin_float = [] 
      for (gs = 0; gs < 5; gs++){
         if( zero_Total_revenue[gs] == 0){
            gross_sales_margin_float.push(0);
         }else{
            gross_sales_margin_float.push(Math.round(zero_GSP[gs] / arrRevenue[gs], 3));
         }
      }
      var  roa_float = []
      for (gs = 0; gs < 5; gs++){
        if(total_assets[gs] == 0){
          roa_float.push(0);
        }else{
          roa_float.push(Math.round(zero_GSP[gs] / total_assets[gs], 3));
        }
      }
      var roe_float = []
      for (gs = 0; gs < 5; gs++){
        if(adequacy_ratios[gs] == 0){   
          roe_float.push(0) 
        }else{
          roe_float.push(Math.round(netIncome_Value[gs] / adequacy_ratios[gs], 3))
        }
      }

      var y_min2 = Math.min.apply(Math, gross_sales_margin_float);
      if(Math.min.apply(Math, gross_sales_margin_float) <= Math.min.apply(Math, roa_float) || Math.min.apply(Math, gross_sales_margin_float) <= Math.min.apply(Math, roe_float)){
        if(Math.min.apply(Math, gross_sales_margin_float) <= Math.min.apply(Math, roa_float) && Math.min.apply(Math, gross_sales_margin_float) <= Math.min.apply(Math, roe_float)){
            y_min2 = Math.min.apply(Math, gross_sales_margin_float);
        }else if( Math.min.apply(Math, roa_float)<= Math.min.apply(Math, gross_sales_margin_float)){
            y_min2 = Math.min.apply(Math, roa_float);
        }else{
             y_min2 = Math.min.apply(Math,roe_float);
        }
      } else{
        y_min2 = 0;
      }
     
      var y_max = 0.5;
      if(Math.max.apply(Math, gross_sales_margin_float) >= Math.max.apply(Math, roa_float) && Math.max.apply(Math, gross_sales_margin_float) >= Math.max.apply(Math, roe_float)){
        if(Math.max.apply(Math, gross_sales_margin_float) >= 0){
          y_max = Math.max.apply(Math, gross_sales_margin_float);
        } else if( Math.max.apply(Math, roa_float) >= Math.max.apply(Math, roe_float)){
          if(Math.max.apply(Math, roa_float) <= 0){
              y_max = max(roa_float);
            }else{
              y_max = 0.5;
          }
        } else if( Math.max.apply(Math, roe_float) <= 0){
            y_max = 0.5;
        }else{
          y_max = 0.5;
        }
      }else{
        y_max = Math.max.apply(Math,roe_float);
      }   
      var data4 = non_converter(gross_sales_margin_float);
      var data5 = non_converter(roa_float);
      var data6 = non_converter(roe_float);
      console.log("data4 "+data4)
      console.log("data5 "+data5)
      console.log("data6 "+data6)
      chartLine(arrayLabel,data4,data5,data6);
    })  
    var net_OP_Cash_Flow_Value =[];
    var net_financial_CF = [];
    var net_Inv_CF_Total =[];
    var fcf =[]
    // Net_Operating_Cash_Flow, Net_Investing_Cash_Flow, Net_Financing_Cash_Flow, Quarterly_free_cash_flow,
    $.getJSON(ur3).done(function(datas) {
      for (i = 0; i < datas.data.length; i++) {
        var company_id = datas.data[i].company_id;
        if(id == company_id){
          var bs = datas.data[i];
          var total_asset = parseInt(bs.Net_Operating_Cash_Flow);
          net_OP_Cash_Flow_Value.push(total_asset);
          var adequacy_ratio =  parseInt(bs.Net_Financing_Cash_Flow);
          net_financial_CF.push(adequacy_ratio);
          var roa =  parseInt(bs.Net_Investing_Cash_Flow);
          net_Inv_CF_Total.push(roa);
          var roe =  parseInt(bs.Quarterly_free_cash_flow);
          fcf.push(roe);
        }
      }

      var y3_min = [];
      y3_min.push(Math.min.apply(Math,net_OP_Cash_Flow_Value));
      y3_min.push(Math.min.apply(Math,net_financial_CF));
      y3_min.push(Math.min.apply(Math,net_Inv_CF_Total));
      y3_min.push(Math.min.apply(Math,fcf));
      minifig = Math.min.apply(Math,y3_min);

      var y3_max = [];
      y3_max.push(Math.max.apply(Math,net_OP_Cash_Flow_Value));
      y3_max.push(Math.max.apply(Math,net_financial_CF));
      y3_max.push(Math.max.apply(Math,net_Inv_CF_Total));
      y3_max.push(Math.max.apply(Math,fcf));
      maxfig = Math.max.apply(Math,y3_max);

      var data6 = non_converter(net_OP_Cash_Flow_Value);
      var data7 =  non_converter(net_Inv_CF_Total);
      var data8 =  non_converter(net_financial_CF);
      var data9 =  non_converter(fcf);
      chart(arrayLabel,data6,data7,data8,data9);  
    })  
  })  
} 

function chartLine(arrayLabel,data4,data5,data6){
  new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels: arrayLabel,
    datasets: [{ 
        data: data4,
        label: "営業利益率",
        borderColor: "#F0BE2C",
        fill: false
      }, { 
        data: data5,
        label: "ROA",
        borderColor: "#4331F5",
        fill: false
      }, { 
        data: data6,
        label: "ROE",
        borderColor: "#e84d60",
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
      labels: {}
  },
  
    tooltips: {
      mode: 'label',
      callbacks: {
        title :function(tooltipItem, data){
          console.log("::::::::"+tooltipItem.labes);
          return "期間"+ tooltipItem.yLabel;
        },
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

function charts(arrayLabel,data1,data2,data3){
  var barChartData = {
    labels: arrayLabel,
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
        text: "売上/営業利益/純利益"
      },
      legend: {
        position: "bottom",
        labels: {}
      },

      tooltips: {
        mode: 'label',
        callbacks: {
          title :function(tooltipItem, data){
            return "期間"+ tooltipItem.yLabel;
          },
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

function chart(arrayLabel,data1,data2,data3,data4){
  var barChartData = {
    labels: arrayLabel,
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
  var barChart = new Chart(ctx, {
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
        labels: {}
      },
      tooltips: {
        mode: 'label',
        callbacks: {
          title :function(tooltipItem, data){
            console.log("::::::::"+tooltipItem.labes);
            return "期間"+ tooltipItem.yLabel;
          },
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

