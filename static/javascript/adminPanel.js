// Ajax function to change User Role
function changeUserRole(select_role_element){
    row_data = select_role_element.parentElement.parentElement.querySelector("#userID").textContent
    role = select_role_element.value
    change_role_confirmation = confirm("Are you sure ?")
    token = document.getElementById("token").value; 
    if(change_role_confirmation == true){

            try {
                var xhttp = new XMLHttpRequest();
        
                // console.log("ajax request state: "+xhttp.readyState);
        
                xhttp.onreadystatechange = function() {
        
                    if(this.readyState == 4 && this.status == 200){
                            console.log("User changed to", role)
                    }             
                }
        
                file_url = '/changeRole?user_id='+row_data+"&role="+role
                
                
                xhttp.open('POST',file_url,true);
                
                xhttp.setRequestHeader("X-CSRFToken",token)
                
                xhttp.send();
            } 
            catch (err) {
                console.log("Error: " + err)
            }
        
        }
    }





let searchInput = document.getElementById("searchTable");
let rows = document.querySelectorAll("tbody tr");
searchInput.addEventListener("keyup",
    function(event){
        let q = event.target.value.toLowerCase();
        rows.forEach((row)=>{
                row.querySelector("#username").textContent.toLowerCase().startsWith(q)?(row.style.display=""):(row.style.display="none");
        })
    })

  /**
* Sorts a HTML table.
* 
* @param {HTMLTableElement} table The table to sort
* @param {number} column The index of the column to sort
* @param {boolean} asc Determines if the sorting will be in ascending
*/
function sortTableByColumn(table, column, asc = true) {
const dirModifier = asc ? 1 : -1;
const tBody = table.tBodies[0];
const rows = Array.from(tBody.querySelectorAll("tr"));

// Sort each row
const sortedRows = rows.sort((a, b) => {
    const aColText = a.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
    const bColText = b.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();

    return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
});

// Remove all existing TRs from the table
while (tBody.firstChild) {
    tBody.removeChild(tBody.firstChild);
}

// Re-add the newly sorted rows
tBody.append(...sortedRows);

// Remember how the column is currently sorted
table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-asc", asc);
table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".table .sort").forEach(headerCell => {
headerCell.addEventListener("click", () => {
    const tableElement = headerCell.parentElement.parentElement.parentElement;
    const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
    const currentIsAscending = headerCell.classList.contains("th-sort-asc");

    sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
});
});