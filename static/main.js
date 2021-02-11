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
    var count = 1;
    html = "";
    for(i in data['data']['containers'])
    {
        html = html + '  <tr>    <td>'+ count++ +'</td><td>'+i +'</td> <td><a onclick="delete_desklet('+i+')" > <i class="fa fa-trash" aria-hidden="true"></i></a> | <a onclick="connect_desklet()" > Connect <i class="fa fa-plug" aria-hidden="true"></i></a></td>  </tr>'
    }
    document.getElementById("data").innerHTML=html;
    if(data['data']['maxAllowed'] == 0 || data['data']['maxAllowed'] == '0')
    {
        document.getElementById("intro").innerHTML="You have no Free Desklets left. Contact <a target='_blank'> Admin </a> for More Desklets ";
    }
    else
    {
        document.getElementById("intro").innerHTML="You have "+data['data']['maxAllowed']+" Desklets left. <a onclick='new_desklet_show()' >Click "+'<i class="fa fa-plus-circle" aria-hidden="true"></i></a> ' + "to make a new Desklet. Contact <a target='_blank'> Admin <a> for More Desklets ";
    }

    console.log(data);
    document.getElementById("images").innerHTML= ' <option value="Internet Explorer (default)">  <option value="Firefox">  <option value="Chrome">';
}

function delete_desklet(uid){
    alert("Are you sure, You want to delete "+ uid + " ?");
    data();
}

function new_desklet(){
    
    data();
    desklet_name.value = '';
    desklet_password.value='';
    desklet_image.value='';
}

function new_desklet_show(){
    document.getElementById("intro").style.visibility="hidden"; 
    document.getElementById("new_desklet_form").style.visibility="visible";
    setTimeout(500);
}

function new_desklet_hide()
{
    document.getElementById("intro").style.visibility="visible"; 
    document.getElementById("new_desklet_form").style.visibility="hidden"; 
}
function connect_desklet(uid){

}