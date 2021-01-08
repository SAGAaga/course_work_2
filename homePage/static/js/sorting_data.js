let contracts_section = document.getElementById("contracts");
let payments_section = document.getElementById("payments");
let discounts_section = document.getElementById("discounts");
let accomodation_section = document.getElementById("accomodation");

let all_contracts=[];
let contract_rows=contracts_section.lastElementChild.firstElementChild.firstElementChild.children
for (let i=0;i<contract_rows.length;i++){
    let temp_data=contract_rows[i].children;
    let temp={};
    temp["contract_number"]=temp_data[0].textContent;
    temp["address"]=temp_data[1].textContent;
    temp["term"]=new Date(temp_data[2].textContent);
    temp['row']=contract_rows[i];

    all_contracts.push(temp);
}

let all_payments=[];
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

    all_payments.push(temp);
}

let all_discounts=[];
let discounts_rows=discounts_section.lastElementChild.firstElementChild.firstElementChild.children
for (let i=0;i<discounts_rows.length;i++){
    let temp_data=discounts_rows[i].children;
    let temp={};
    temp["name"]=temp_data[0].textContent;
    temp["pecent"]=parseInt(temp_data[1].textContent);
    temp['row']=discounts_rows[i];

    all_discounts.push(temp);
}

let all_accomodation=[];
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

    all_accomodation.push(temp);
}


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

let sort_click=function(elem, table, key){
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

