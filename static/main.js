const URL="http://localhost:5000";
const HOME= "http://localhost:8000";

async function service_status(){
    var url = URL+"/service-status";
    const response = await fetch(url).catch(function(){
        document.getElementById("login").innerHTML= "<h2> Service Unavailable. </h2><h3> Team is Working on it. Check again Soon !!</h3>";
    });
    document.getElementById("status").style.visibility=  "hidden";
    document.getElementById("login").style.visibility=  "visible";
    // setTimeout(500);
}

async function data(){
    var url = URL+"/get-data";
    const response = await fetch(url,{
        method: 'GET',
        credentials: 'include'
      }).catch( function(){  
            window.location.replace(HOME+"/retry"); 
        });
    var data = await response.json();
    if(response.status == 200 )
    {
        document.getElementById("username").innerHTML = data['data']['username'];
        document.getElementById("welcome").innerHTML = data['data']['name'];
        console.log("Authenticated")
    }
    if(response.status == 401 )
    {
        window.location.replace(HOME+"/retry.html"); 
    }

    html = "";
    for(i in data['data']['containers'])
    {
        html = html + '  <tr>    <td>'+ i +'</td> <td>'+ data['data']['containers'][i] +'</td>   <td>'+'  asd'+'</td><td>'+ "xyz" +'</td> <td><button onclick="delete_desklet('+i+')" > <i class="fa fa-trash" aria-hidden="true"></i></button></td>  </tr>'
    }
    document.getElementById("data").innerHTML=html;

    console.log(data);
}

function delete_desklet(uid){
    alert("Are you sure, You want to delete "+ uid + " ?");
    data();
}