const sourceFileInput = document.getElementById('sourceFile');
const sourceFile = sourceFileInput.files[0];  // Get the first file (if any)

const formData=new FormData();
formData.add("name","srdr");


document.getElementById("runButton").addEventListener("click",async function(){
    fetch("http://localhost:5000/api/tariff/generatetargetfile",{
        method:"POST",
        body:formData
    })
    .then(result=>{
        document.getElementById("lblResult").innerHTML=result.returnedName;
    })
});

