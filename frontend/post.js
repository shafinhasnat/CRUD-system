token='?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6InNoYWZpbmhhc25hdCJ9.zl9PpQSrn6gKC8iGSoDYU-1v3Itj6UGia7ZuZ1_vM6Q'
function loadBtn() {
    var name = document.getElementById("postform").elements.namedItem("name").value;
    var description = document.getElementById("postform").elements.namedItem("description").value;
    var price = document.getElementById("postform").elements.namedItem("price").value;
    var qty = document.getElementById("postform").elements.namedItem("qty").value;

    var url = "http://127.0.0.1:5000/product"+token;
    const toSend = {
    "description": `${description}`,
    "name": `${name}`,
    "price": `${price}`,
    "qty": `${qty}`
  }
  const jsonString = JSON.stringify(toSend);
  const xhr = new XMLHttpRequest();
  xhr.open("POST", url);
  xhr.setRequestHeader('content-Type', 'application/json');
  xhr.send(jsonString);
  location.reload();

}