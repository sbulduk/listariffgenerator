const apiBaseUrl="http://localhost:5000/api/tariff";

document.getElementById("runButton").addEventListener("click",async function(){
    const sourceFile=document.getElementById("sourceFile").files[0];
    const sourceSheet=document.getElementById("sourceSheet").value;
    const targetFile=document.getElementById("targetFile").value;

    // let now=new Date();
    // const timeStamp=now.getFullYear().toString()+
    //     (now.getMonth()+1).toString().padStart(2,"0")+
    //     now.getDate().toString().padStart(2,"0")+"_"+
    //     now.getHours().toString().padStart(2,"0")+
    //     now.getMinutes().toString().padStart(2,"0")+
    //     now.getSeconds().toString().padStart(2,"0");
    // if(targetFile==""){
    //     targetFile=targetFile+"_"+timeStamp;
    // }else{targetFile=timeStamp;}
    // let targetFilewithTimeStamp=targetFile.replace(/(\.[\w\d_-]+)$/i,`_${timeStamp}$1`);

    const targetSheet=document.getElementById("targetSheet").value;
    const resultArea=document.getElementById("resultArea");
    const loadingIcon=document.getElementById("loadingIcon");
    const runButton=document.getElementById("runButton");

    let formData=new FormData();
    formData.append("sourceFile",sourceFile);
    formData.append("sourceSheet",sourceSheet);
    formData.append("targetFile",targetFile);
    formData.append("targetSheet",targetSheet);

    loadingIcon.style.display="block";
    resultArea.innerHTML="";
    runButton.disabled=true;

    fetch(`${apiBaseUrl}/upload`,{
        method:"POST",
        body:formData
    })
    .then(response=>response.json())
    .then(data=>{
        if(data.success){
            fetch(`${apiBaseUrl}/generatetargetfile`,{
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({
                    sourceFile:data.fileName,
                    sourceSheet:sourceSheet,
                    targetFile:targetFile,
                    targetSheet:targetSheet
                })
            })
            .then(response=>response.json())
            .then(result=>{
                loadingIcon.style.display="none";
                runButton.disabled=false;
                resultArea.innerHTML=`<p class="text-success">File Uploaded Successfully</p>`;
                resultArea.innerHTML+=`<p class="text-success">Success: ${result.message}</p>`;
                resultArea.innerHTML+=`<p><a href="${result.url}" class="btn btn-primary" download>Download Generated File</a></p>`;
            });
        }else{
            loadingIcon.style.display="none";
            runButton.disabled=false;
            resultArea.innerHTML=`<p class="text-danger">An error occured</p>`;
            resultArea.innerHTML+=`<p class="text-danger">Success: ${result.message}</p>`;
        }
    })
    .catch(error=>{
        loadingIcon.style.display="none";
        runButton.disabled=false;
        resultArea.innerHTML=`<p class="text-danger">Error: ${error.message}</p>`;
        resultArea.innerHTML+=`<p class="text-danger">Success: ${result.message}</p>`;
    });
});