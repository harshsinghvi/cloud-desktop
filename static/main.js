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
    images_html=''
    for(i in data['images'])
    {
        images_html += '<option value="' + data['images'][i] + '">';
    }
    document.getElementById("images").innerHTML=images_html;
    console.log(data);
}

function delete_desklet(uid){
    alert("Are you sure, You want to delete "+ uid + " ?");
    data();
}

async function new_desklet(){
    var data = {};
    post_data = {
        "name" : desklet_name.value,
        "password" : desklet_password.value,
        "image" : desklet_image.value
    };
    var url = URL+"/get-desklet";
    const response = await fetch(url, {
        method: 'POST',
        credentials: 'include',
        mode: 'no-cors',
        body: JSON.stringify(post_data)
      }).then(function() {    
            data = response.json();
            console.log(data);
            data();
            desklet_name.value = '';
            desklet_password.value='';
            desklet_image.value='';
    
        }).catch( function(){
        alert("Problem in creating Desklet, Please Try again !");
    });

    
    
    // data();
    // desklet_name.value = '';
    // desklet_password.value='';
    // desklet_image.value='';
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