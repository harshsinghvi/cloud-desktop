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
        console.log("Authenticated")
    }
    
    console.log(data);
}