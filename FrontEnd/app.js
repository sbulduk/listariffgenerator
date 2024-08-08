const apiBaseUrl="http://localhost:5000/api/tariff";

document.getElementById("runButton").addEventListener("click",async function(){
    const sourceFile=document.getElementById("sourceFile").value;
    const sourceSheet=document.getElementById("sourceSheet").value;
    const targetFile=document.getElementById("targetFile").value;
    const targetSheet=document.getElementById("targetSheet").value;
    const resultArea=document.getElementById("resultArea");
    const loadingIcon=document.getElementById("loadingIcon");

    const requestData={
        sourceFileName:sourceFile,
        sourceSheetName:sourceSheet,
        targetFileName:targetFile,
        targetSheetName:targetSheet
    };

    loadingIcon.style.display="block";
    resultArea.innerHTML="";

    try{
        const response=await fetch(`${apiBaseUrl}/generatetargetfile`,{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify(requestData)
        });

        const data=await response.json();
        loadingIcon.style.display="none";

        if (response.ok){
            resultArea.innerHTML=`<p class="text-success">Success:${data.message}</p>`;
            if (data.url){
                resultArea.innerHTML+=`<p><a href="${data.url}" class="btn btn-primary" download>Download Generated File</a></p>`;
            }
        }else{
            resultArea.innerHTML=`<p class="text-danger">Error:${data.message}</p>`;
        }
    }catch (error){
        loadingIcon.style.display="none";
        resultArea.innerHTML=`<p class="text-danger">Error:${error.message}</p>`;
    }
});