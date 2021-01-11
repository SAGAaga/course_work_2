let contracts_section = document.getElementById("contracts");
let payments_section = document.getElementById("payments");
let discounts_section = document.getElementById("discounts");
let accomodation_section = document.getElementById("accomodation");

let select_contracts_row = document.getElementById("select_contracts");
let select_payments_row = document.getElementById("select_payments");
let select_discounts_row = document.getElementById("select_discounts");
let select_accomodation_row = document.getElementById("select_accomodation");


function all_contracts_get(){
    let arr=[];
    let contract_rows=contracts_section.lastElementChild.firstElementChild.firstElementChild.children
    for (let i=0;i<contract_rows.length;i++){
        let temp_data=contract_rows[i].children;
        let temp={};
        temp["contract_number"]=temp_data[0].textContent;
        temp["address"]=temp_data[1].textContent;
        temp["term"]=new Date(temp_data[2].textContent);
        temp['row']=contract_rows[i];

        arr.push(temp);
    }
    return arr
}
const all_contracts=all_contracts_get();

function all_payments_get(){
    let arr=[];
    let payment_rows=payments_section.lastElementChild.firstElementChild.firstElementChild.children
    for (let i=0;i<payment_rows.length;i++){
        let temp_data=payment_rows[i].children;
        let temp={};
        temp["contract_number_id"]=temp_data[0].textContent;
        temp["payment_id"]=parseInt(temp_data[1].textContent);
        temp["summ"]=parseInt(temp_data[2].textContent);
        let m = moment(temp_data[3].textContent, "lll");
        temp["pay_datetime"] = m.toDate();
        temp['row']=payment_rows[i];

        arr.push(temp);
    }
    return arr;
}
const all_payments=all_payments_get();


function all_discounts_get(){
    let arr=[];
    let discounts_rows=discounts_section.lastElementChild.firstElementChild.firstElementChild.children
    for (let i=0;i<discounts_rows.length;i++){
        let temp_data=discounts_rows[i].children;
        let temp={};
        temp["name"]=temp_data[0].textContent;
        temp["pecent"]=parseInt(temp_data[1].textContent);
        temp['row']=discounts_rows[i];

        arr.push(temp);
    }
    return arr;
}
const all_discounts=all_discounts_get();



function all_accomodation_get(){
    let arr=[];
    let accomodation_rows=accomodation_section.lastElementChild.firstElementChild.firstElementChild.children
    for (let i=0;i<accomodation_rows.length;i++){
        let temp_data=accomodation_rows[i].children;
        let temp={};
        temp["address"]=temp_data[0].textContent;
        temp["squeare"]=parseInt(temp_data[1].textContent);
        temp["consumed"]=parseInt(temp_data[2].textContent);
        let m = moment(temp_data[3].textContent, "lll");
        temp["date_in"] = m.toDate();
        temp["debt"]=parseInt(temp_data[4].textContent);
        temp["prepayment"]=parseInt(temp_data[5].textContent);
        temp['row']=accomodation_rows[i];

        if(temp["date_in"]=="Invalid Date"){
            let t=new Date(-1);
            temp["date_in"]=t;
        }

        arr.push(temp);
    }
    return arr;
}
const all_accomodation=all_accomodation_get();



let sort_by=function(arr,key){
    for(let i=0;i<arr.length-1;++i){
        for(let j=0;j<arr.length-1-i;++j){
            if(arr[j][key]>arr[j+1][key]){
                let temp=arr[j];
                arr[j]=arr[j+1];
                arr[j+1]=temp;
            }
        }
    }
    return arr;
}

//cheks event click on th
let sort_click=function(elem, table, key){
    let section;
    let data;
    if(table=="contracts"){
        section=contracts_section;
        data=all_contracts_get();
    }
    else if(table=="payments"){
        section=payments_section;
        data=all_payments_get();
    }
    else if(table=="discounts"){
        section=discounts_section;
        data=all_discounts_get();
    }
    else if(table=="accomodation"){
        section=accomodation_section;
        data=all_accomodation_get();
    }
    section.lastElementChild.firstElementChild.firstElementChild.remove();
    data=sort_by(data,key);
    let tbody=document.createElement("tbody");

    if(elem.name){
        if(elem.name=="ASC"){
            elem.name="DESC";
        }
        else{
            elem.name="ASC";
        }
    }
    else{
        elem.name="ASC"
    }
    if(elem.name=="ASC"){
        for(let i=0;i<data.length;++i){
            tbody.appendChild(data[i]["row"]);
        }
    }
    else{
        for(let i=data.length-1;i>=0;i--){
            tbody.appendChild(data[i]["row"]);
        }
    }
    section.lastElementChild.firstElementChild.appendChild(tbody);
}


//cheks input changed
let filtering=function(elem,table){
    let section;
    let data;
    if(table=="contracts"){
        section=contracts_section;
        data=all_contracts;
    }
    else if(table=="payments"){
        section=payments_section;
        data=all_payments;
    }
    else if(table=="discounts"){
        section=discounts_section;
        data=all_discounts;
    }
    else if(table=="accomodation"){
        section=accomodation_section;
        data=all_accomodation;
    }
    section.lastElementChild.firstElementChild.firstElementChild.remove();
    let filtered_data=[]
    for(let i=0;i<data.length;++i){
        let keys=Object.keys(data[i]);
        for(let j=0;j<keys.length-1;++j){
            if(String(data[i][keys[j]]).includes(elem.value)){
                filtered_data.push(data[i][keys[keys.length-1]]);
                break;
            }
        }
    }

    let tbody=document.createElement("tbody");

    for(let i=0;i<filtered_data.length;i++){
        tbody.appendChild(filtered_data[i]);
    }
    section.lastElementChild.firstElementChild.appendChild(tbody);
}

let clear_input=function(elem){
    elem=elem.parentElement.firstElementChild;
    elem.value="";
    elem.onkeyup();
    let row=elem.parentElement.parentElement.parentElement;
    let table=row.id.split("_")[1];
    row=row.children;
    for(let i=0;i<row.length-1;++i){
        let element=row[i].firstElementChild;
        if(element.tagName=="SELECT"){
            element.selectedIndex=0;
            element.onchange(table)
        }
        else if(element.classList[0]=="date"){
            element.firstElementChild.value="";
            element.lastElementChild.value="";
            element.lastElementChild.onchange(table)
        }
        else{
            element.firstElementChild.value="";
            element.lastElementChild.value="";
            element.lastElementChild.onkeyup(table);
        }
    }
}



let select_text_fields=function(elem,data,key){
    let value=elem.options[elem.selectedIndex].text;
    if(value=="ALL"){
        return data;
    }
    let res_data=[]
    for(let i=0;i<data.length;++i){
        if(data[i][key]==value){
            res_data.push(data[i]);
        }
    }
    return res_data;
}

let select_date=function(from,to,data,key){    
    if(from==""&&to==""){
        return data;
    }
    if(from==""){
        //from= moment(-1).format('YYYY-MM-DD');
        from=new Date(-1);
    }
    if(to==""){
        //to= moment().add(100,"year").format('YYYY-MM-DD');
        to=new Date(3000,1,1);
    }
    from=new Date(from);
    to=new Date(to);
    if(from>=to){
        let temp=to;
        to=from;
        from=temp;
    }
    let res_data=[]
    for(let i=0;i<data.length;++i){
        if(data[i][key]>=from && data[i][key]<=to){
            res_data.push(data[i]);
        }
    }
    return res_data;
}

let select_number=function(from,to,data,key){    
    if(from=="" && to==""){
        return data;
    }
    if(from==""){
        from=0;
    }
    if(to==""){
        to=1000000;
    }
    from=parseInt(from);
    to=parseInt(to);
    if(from>=to){
        let temp=to;
        to=from;
        from=temp;
    }
    let res_data=[]
    for(let i=0;i<data.length;++i){
        if(data[i][key]>=from && data[i][key]<=to){
            res_data.push(data[i]);
        }
    }
    return res_data;
}

let select_check=function(table){
    let section,data,row;
    if(table=="contracts"){
        section=contracts_section;
        data=all_contracts;
        row=select_contracts_row;
    }
    else if(table=="payments"){
        section=payments_section;
        data=all_payments;
        row=select_payments_row;
    }
    else if(table=="discounts"){
        section=discounts_section;
        data=all_discounts;
        row=select_discounts_row;
    }
    else if(table=="accomodation"){
        section=accomodation_section;
        data=all_accomodation;
        row=select_accomodation_row;
    }
    section.lastElementChild.firstElementChild.firstElementChild.remove();
    row=row.children;
    for(let i=0;i<row.length-1;++i){
        let elem=row[i].firstElementChild;
        if(elem.tagName=="SELECT"){
            data=select_text_fields(elem,data,elem.name);
        }
        else if(elem.classList[0]=="date"){
            let from=elem.firstElementChild.value;
            let to=elem.lastElementChild.value;
            data=select_date(from,to,data,elem.classList[1])
        }
        else{
            let from=elem.firstElementChild.value;
            let to=elem.lastElementChild.value;
            data=select_number(from,to,data,elem.classList[0]);
        }
    }

    let filtered_data=data
    let tbody=document.createElement("tbody");

    for(let i=0;i<filtered_data.length;i++){
        tbody.appendChild(filtered_data[i]["row"]);
    }
    section.lastElementChild.firstElementChild.appendChild(tbody);
}

