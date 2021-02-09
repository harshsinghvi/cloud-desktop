const URL="https://stackapi.vercel.app";
// const URL="http://localhost:5000";
async function main(){
    var url = URL+"/stack";
    const response = await fetch(url);
    var data = await response.json();
    document.getElementById("size").innerHTML="size = "+data['size'];
    size=data['size'];
    var html = '<tr> <th>index</th> <th>data</th> <th>&nbsp;&nbsp;&nbsp;</th> <th>index</th> <th> data </th>  </tr>';
    for(i in data['data'])
    {
        html = html + '  <tr>    <td>'+ i +'</td> <td>'+ data['data'][i] +'</td>  <td></td> <td>'+(size-i-1)+'</td><td>'+ data['data'][(size-i-1)]+'</td>   </tr>'
    }
    document.getElementById("data").innerHTML=html;
    console.log(data);
    setTimeout(500);
}
main();
async function push(){
    var url = URL+"/push?data="+push_data.value;
    const response = await fetch(url);
    var data = await response.json();
    setTimeout(1500);
    document.getElementById("result").innerHTML= JSON.stringify(data) + " " + response.status;
    console.log(data);
    main();
}

async function pop(){
    var url = URL+"/pop";
    const response = await fetch(url);
    var data = await response.json();
    setTimeout(1500);
    document.getElementById("result").innerHTML= JSON.stringify(data) + " " + response.status;
    document.getElementById("push_data").value = "";
    console.log(data);
    main();
}

setInterval(main,2000)