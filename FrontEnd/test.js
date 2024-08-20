const sourceFileInput = document.getElementById('sourceFile');
const sourceFile = sourceFileInput.files[0];  // Get the first file (if any)

document.getElementById("runButton").addEventListener("click",async function(){
    if (!sourceFile) {
        console.error("No file selected");
    } else {
        console.log("File selected:", sourceFile.name);
    }
});

