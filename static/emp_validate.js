const insert_form = document.getElementById("insert_form");
const errorDiv = document.getElementById("Error_message");
const success_msg = document.getElementById("Success_message");
const edit_form = document.getElementById("edit_form");
const del_form = document.getElementById("del_form");

insert_form.addEventListener("submit", function(e) {
    e.preventDefault();
    const input_type = document.getElementById("Type");
    
    let errors = [];

    const inputData = new FormData(insert_form);

    if (inputData.get("fname").trim() == '') 
        errors.push("First name can't be empty.");
    if (inputData.get("m_i").trim() == '')
        errors.push("Middle initial can't be empty.");
    if (inputData.get("lname").trim() == '')
        errors.push("Last name can't be empty.");
    if (inputData.get("ssn").trim() == '')
        errors.push("ssn can't be empty.");
    if (inputData.get("address").trim() == '')
        errors.push("Address can't be empty.");
    if (inputData.get("salary").trim() == '')
        errors.push("Salary can't be empty.");
    if (inputData.get("dname").trim() == '')
        errors.push("Department can't be empty.");
    if (inputData.get("bdate").trim() == '')
        errors.push("birthday can't be empty.");

    if (errors.length > 0){
        errorDiv.innerHTML = errors.join("<br>");
              success_msg.innerHTML="";
    } else {
        errorDiv.innerHTML = "";
        // inputData.set("button", e.submitter.value);
        input_type.value = e.submitter.value;        
        insert_form.submit();

        // fetch("/emp_manage", {method: "POST", body: inputData})
        // .catch(err => {errorDiv.innerHTML = "Error sending data."})
    }


});

edit_form.addEventListener("submit", function(e) {
    e.preventDefault();

    let errors = [];

    const inputData = new FormData(edit_form);

    if (inputData.get("edit_add").trim() == '')
        errors.push("Address can't be empty.");
    if (inputData.get("edit_salary").trim() == '')
        errors.push("Salary can't be empty.");
    if (inputData.get("view_ssn").trim() == '')
        errors.push("employee can't be empty");
    if (inputData.get("edit_dep").trim() == '')
        errors.push("Department can't be empty");

    if (errors.length > 0){
        errorDiv.innerHTML = errors.join("<br>");
              success_msg.innerHTML="";
    } else {

        edit_form.submit();
    }

});

del_form.addEventListener("submit", function(e) {
    e.preventDefault(); 

    let errors = [];

    const inputData = new FormData(del_form);

    if (inputData.get("del_employee").trim() == '')
        errors.push("Can't delete empty employee.");

    if (errors.length > 0){
        errorDiv.innerHTML = errors.join("<br>");
              success_msg.innerHTML="";
    } else {

        del_form.submit();
    }

});