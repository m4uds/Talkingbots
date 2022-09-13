console.log("m4uds made this")

var options = {
    "animate": true,
    "patternWidth": 150,
    "patternHeight": 150,
    "grainOpacity": 0.2,
    "grainDensity": 1,
    "grainWidth": 1,
    "grainHeight": 1}

grained("#display-cont", options);



function main(){
        
    buildConvosation()
    
}
async function LoadConversation() {
    //change back to [-5:]
    const response = await fetch("conversation.json");
    const json = await response.json();
    return json
}

async function buildConvosation (){
    var data = []
    await LoadConversation().then((Response => data = Response));
     console.log(data);
    $("#text-cont").html("");
    for (const element of data) {
        var text = Object.values(element)[0]
        if (text.startsWith('Blender:')){
            text = text.replace('Blender:','');
            $( "#text-cont" ).append( "<div class = 'left'><h1>"+text+"</h1></div>" );}
        else if (text.startsWith('DialoGPT:')){
            text = text.replace('DialoGPT:','');
            $( "#text-cont" ).append( "<div class = 'right'> <h1>"+text+"</h1> </div>" )

        }
     
        } 
      


}

$( window).on("load", setInterval(function (){
    main()},
    4000));

