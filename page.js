let length = 5;
let currRow = 0;
let currCol = 0;
let currBlock = 0;
let thisRow;
function setGridLength(rows){
    let grid = document.getElementsByClassName("row");
    grid = grid[0];
    length = rows;
    grid.className = "gx-0 row row-cols-" + rows;
    grid.style.width = (50*length).toString() + "px";
    console.log(grid.style);
}
function addGridBlock(type, down=null, right=null) {
    if (currCol%length === 0){
        thisRow = document.createElement("div");
        thisRow.className = "gx-0 row";
        thisRow.style.width = (50*length).toString() + "px";
        thisRow.style.height = "50px";
    }
    let outside = document.createElement("div");
    outside.className = "card";
    if (type === "black"){
        createBlack(outside)
    } else if(type === "constraint") {
        createConstraint(down,right,outside);
    }else {
        createNormal(outside,type);
    }
    outside.style.height = "50px"
    let block = document.createElement("div");
    block.className = "col gx-0"
    block.id = "row" + currRow + "col" + currCol;
    block.appendChild(outside);
    block.style.height = "50px"
    thisRow.appendChild(block);
    currBlock++;
    currCol++;
    if(currBlock%length === 0){
        currCol = 0;
        currRow++;
        let grid = document.getElementsByClassName("row")[0];
        grid.appendChild(thisRow);
    }

}
function createNormal(block,type){
    block.innerText = type;
    block.className = "card normal"
}
function createBlack(block){
    block.className = "card bg-dark"
}
function createConstraint(down, right, block) {
    // Create a div for 'x'
    let xDiv = document.createElement("div");
    xDiv.className = "constraint-x text-end";
    xDiv.style.paddingRight = "20%";
    xDiv.innerText = down;
    let line = document.createElement("span");
    line.className = "line";
    // Create a div for 'y'
    let yDiv = document.createElement("div");
    yDiv.className = "constraint-y text-start";
    yDiv.style.paddingLeft = "20%";
    yDiv.innerText = right;

    // Append 'x' and 'y' divs to the block
    block.appendChild(xDiv);
    block.appendChild(yDiv);
    block.appendChild(line);

}

function solve(){
    // Calling the python solve code
}
function setBlock(x,y,value){
    let block = document.getElementById("row"+x+"col"+y);
    block.innerText = value;
}
window.addEventListener("load", function () {
    setGridLength(8);
    for(let i = 0; i < 64; i++){
        if (i%5 === 0) {
            addGridBlock("black");
        } else if(i%3 === 0){
            addGridBlock("constraint", 2,2);
        } else {
            addGridBlock("hi");
        }
    }
    let fileBox = document.getElementById("file");
    let reader = new FileReader();
    let boardText;
    reader.addEventListener('load', event => {
        boardText = event.target.result
        let arrayBoard = boardText.split('\n');
        setGridLength(arrayBoard[0]);
        for (let i = 1; i <= length*length; i++){
            let block = arrayBoard[i];
            if (block === "normal" || block === "black"){
                addGridBlock(block)
            } else {
                block = block.split(" ");
                addGridBlock(block[0], block[1], block[2]);
            }
        }
    })
    fileBox.addEventListener('change', event => {
        let file = event.target.files
        file = file[0];
        reader.readAsText(file);
    })
})
