token='?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6InNoYWZpbmhhc25hdCJ9.zl9PpQSrn6gKC8iGSoDYU-1v3Itj6UGia7ZuZ1_vM6Q';
var xmlhttp = new XMLHttpRequest();
var url = "http://127.0.0.1:5000/";
function show(search) {
   var search = document.getElementById('searchform').elements.namedItem("searchfield").value;
   s_url = url+'product/name/'+search+token;
   console.log(search);
   console.log(s_url);
   xmlhttp.open("GET", s_url, true);
   xmlhttp.send();
   if (search === ''){
      xmlhttp.open("GET", url, true);
      xmlhttp.send();
   }
}
xmlhttp.open("GET", url+token, true);
xmlhttp.send();

xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var myArr = JSON.parse(this.responseText);
   //  console.log(myArr);
    myFunction(myArr);
  }
};

function myFunction(arr) {
  var ser = "";
  var name = "";
  var desc = "";
  var price ="";
  var qty = "";
  var i;
//   console.log(arr.length);
   var outputHtml = "";
   outputHtml += "<table style='width:80%'>";
      for(i=0; i<=arr.length-1; i++) {
         outputHtml += "<tr>";
         outputHtml += "<td><center>"+(i+1)+"</center></td>";
         outputHtml += "<td><center>"+arr[i].name+"</center></td>";
         outputHtml += "<td><center>"+arr[i].description+"</center></td>";
         outputHtml += "<td><center>"+arr[i].price+"/-</center></td>";
         outputHtml += "<td><center>"+arr[i].qty+"</center></td>";
         outputHtml += "<td><center>"+`<button onclick=deleteEntry(${arr[i].id}) id='dlt-${arr[i].id}'>Delete</button>`+"</center></td>";
         // outputHtml += "<td><center>"+"<button id='adlt'>Delete</button>"+"</center></td>";
         outputHtml += "</tr>";
      }
   outputHtml += "</table>";
   document.getElementById("tablediv").innerHTML = outputHtml;
   
   document.getElementById("searchedNum").innerHTML = Object.values(arr).length + ' item(s)';
   console.log(Object.values(arr).length);
   if (Object.values(arr).length === 0){
       document.getElementById("tablediv").innerHTML = 'No match found';
      }
}
function deleteEntry(place) {
   var url = `http://127.0.0.1:5000/product/${place}`+token;
   console.log(url)   
   var xhr = new XMLHttpRequest();
   xhr.open('DELETE', url, true);
   xhr.send(null);
   location.reload()
}