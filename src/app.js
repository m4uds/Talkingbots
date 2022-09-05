function main(){

    setInterval(buildConvosation, 1000);
    console.log("=)")

}


async function LoadConversation() {
    //change back to [-5:]
    const response = await fetch("conversation.json");
    const json = await response.json();
    return json
}

async function buildConvosation (){
    var data = []
    await LoadConversation().then((Response => data = Response))
     console.log(data)
    
    for (const element of data) {
        console.log()
        $( "#text-cont" ).append( "<h1>"+Object.values(element)+"</h1>" );
      }
      


}

main()

