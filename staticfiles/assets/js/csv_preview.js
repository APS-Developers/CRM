const fileInput = document.getElementById("aps_csv_upload");
const previewContainer = document.querySelector("#aps_csv_upload_preview table");

function CSVToArray(strData, strDelimiter) {
    strDelimiter = (strDelimiter || ",");
    let objPattern = new RegExp(
        (
            "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +
            "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +
            "([^\"\\" + strDelimiter + "\\r\\n]*))"
        ),
        "gi"
    );
    let arrData = [
        []
    ];
    let arrMatches = null;
    while (arrMatches = objPattern.exec(strData)) {
        let strMatchedDelimiter = arrMatches[1];
        let strMatchedValue = [];
        if (strMatchedDelimiter.length && (strMatchedDelimiter != strDelimiter)) {
            arrData.push([]);
        }
        if (arrMatches[2]) {
            strMatchedValue = arrMatches[2].replace(new RegExp("\"\"", "g"), "\"");
        } else {
            strMatchedValue = arrMatches[3];
        }
        arrData[arrData.length - 1].push(strMatchedValue);
    }
    return (arrData);
}
fileInput.addEventListener("change",(e)=>{
    var csvParsedArray = [];
    if(e.target.files.length<1) {
        alert("No file selected");
        return;
    }
    let fileToUpload= e.target.files[0];
    let reader = new FileReader();
    let bytes = 50000;
    reader.onloadend = function (evt) {
      let lines = evt.target.result;
      if (lines && lines.length > 0) {
        let line_array = CSVToArray(lines);
        if (lines.length == bytes) {
          line_array = line_array.splice(0, line_array.length - 1);
        }
        var columnArray = [];
        var stringHeader = "<thead class='aps_table_head'><tr class='align-middle'>";
        var stringBody = "<tbody>";
        for (let i = 0; i < line_array.length; i++) {
          let cellArr = line_array[i];
          stringBody += "<tr>";
          for (var j = 0; j < cellArr.length; j++) {
            if(i == 0) {
              columnArray.push(cellArr[j].replace('ï»¿', ''));
              stringHeader += "<th>" + columnArray[j] + "</th>";
            }
            else{
              stringBody += "<td>" + cellArr[j] + "</td>";
              csvParsedArray.push({
                "column" : columnArray[j],
                "value": cellArr[j]
              });
            }
          }
          stringBody += "</tr>";
        }
        stringBody += "</tbody>";
        stringHeader += "</tr></thead>";
        previewContainer.innerHTML+=stringHeader;
        previewContainer.innerHTML+=stringBody;

      }
    }
    let blob = fileToUpload.slice(0, bytes);
    reader.readAsBinaryString(blob);
})